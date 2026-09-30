from datetime import date as date_type
from datetime import datetime

from flask import Blueprint, g
from flask import request

from models import db
from models import Service
from models import Appointment
from models import Availability
from routes.security import admin_required, login_required


appointments_bp = Blueprint(
    "appointments",
    __name__
)


def validate_slot(data):
    raw_date = data.get("date", "").strip()
    raw_time = data.get("time", "").strip()

    try:
        selected_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
        datetime.strptime(raw_time, "%H:%M")
    except ValueError:
        return None, None, ("La fecha debe usar YYYY-MM-DD y la hora HH:MM", 400)

    if selected_date < date_type.today():
        return None, None, ("No puedes crear horarios en el pasado", 400)

    return raw_date, raw_time, None


def serialize_appointment(appointment, include_context=False):
    result = {
        "id": appointment.id,
        "date": appointment.date,
        "time": appointment.time,
        "status": appointment.status,
    }

    if include_context:
        result["user"] = {
            "id": appointment.user.id,
            "name": appointment.user.name,
            "email": appointment.user.email,
        }
        result["service"] = {
            "id": appointment.service.id,
            "name": appointment.service.name,
            "price": appointment.service.price,
        }

    return result


@appointments_bp.post("/availability")
@admin_required
def create_availability():
    data = request.get_json() or {}
    selected_date, selected_time, error = validate_slot(data)

    if error:
        message, status_code = error
        return {"error": message}, status_code

    if Availability.query.filter_by(
        date=selected_date,
        time=selected_time
    ).first():
        return {"error": "Ese horario ya existe"}, 409

    availability = Availability(date=selected_date, time=selected_time)
    db.session.add(availability)
    db.session.commit()

    return {
        "mensaje": "Horario disponible creado correctamente",
        "horario": {
            "id": availability.id,
            "date": availability.date,
            "time": availability.time,
            "is_available": availability.is_available
        }
    }, 201


@appointments_bp.get("/availability")
def list_availability():
    availability = Availability.query.filter_by(
        is_available=True
    ).order_by(Availability.date, Availability.time).all()

    return {
        "horarios": [
            {
                "id": slot.id,
                "date": slot.date,
                "time": slot.time,
            }
            for slot in availability
        ]
    }


@appointments_bp.get("/")
@login_required
def list_appointments():

    if g.current_user.role == "admin":
        query = Appointment.query
    else:
        query = Appointment.query.filter_by(
            user_id=g.current_user.id
        )

    requested_status = request.args.get("status")
    requested_date = request.args.get("date")

    if requested_status:
        if requested_status not in {"pending", "confirmed", "cancelled", "completed"}:
            return {"error": "Estado de cita no válido"}, 400
        query = query.filter_by(status=requested_status)

    if requested_date:
        try:
            datetime.strptime(requested_date, "%Y-%m-%d")
        except ValueError:
            return {"error": "La fecha debe usar YYYY-MM-DD"}, 400
        query = query.filter_by(date=requested_date)

    appointments = query.order_by(Appointment.date, Appointment.time).all()

    return {

        "citas": [

            serialize_appointment(
                appointment,
                include_context=g.current_user.role == "admin"
            )

            for appointment in appointments

        ]

    }


@appointments_bp.post("/")
@login_required
def create_appointment():

    data = request.get_json() or {}

    selected_date, selected_time, error = validate_slot(data)

    if error:
        message, status_code = error
        return {"error": message}, status_code

    service_id = data.get(
        "service_id"
    )

    # Validaciones

    if not selected_date or not selected_time or not service_id:

        return {
            "error": "Fecha, hora y servicio son obligatorios"
        }, 400

    service = db.session.get(
        Service,
        service_id
    )

    if not service:

        return {
            "error": "El servicio no existe"
        }, 404

    availability = Availability.query.filter_by(
        date=selected_date,
        time=selected_time
    ).first()

    if not availability or not availability.is_available:
        return {
            "error": "El horario no está disponible"
        }, 409

    # Crear cita

    appointment = Appointment(

        date=selected_date,
        time=selected_time,
        user_id=g.current_user.id,
        service_id=service_id

    )

    availability.is_available = False
    db.session.add(appointment)
    db.session.commit()

    return {

        "mensaje": "Cita creada correctamente",

        "cita": serialize_appointment(appointment)

    }, 201


@appointments_bp.patch("/<int:appointment_id>/status")
@admin_required
def update_appointment_status(appointment_id):
    data = request.get_json() or {}
    new_status = data.get("status", "").strip().lower()
    appointment = db.session.get(Appointment, appointment_id)

    if not appointment:
        return {"error": "La cita no existe"}, 404

    transitions = {
        "pending": {"confirmed", "cancelled"},
        "confirmed": {"completed", "cancelled"},
    }

    if new_status not in transitions.get(appointment.status, set()):
        return {"error": "Cambio de estado no permitido"}, 400

    appointment.status = new_status

    if new_status == "cancelled":
        availability = Availability.query.filter_by(
            date=appointment.date,
            time=appointment.time
        ).first()
        if availability:
            availability.is_available = True

    db.session.commit()

    return {
        "mensaje": "Estado de cita actualizado correctamente",
        "cita": {
            "id": appointment.id,
            "status": appointment.status
        }
    }
