from flask import Blueprint, g
from flask import request

from models import db
from models import User
from models import Service
from models import Appointment
from routes.security import login_required


appointments_bp = Blueprint(
    "appointments",
    __name__
)


@appointments_bp.get("/")
@login_required
def list_appointments():

    if g.current_user.role == "admin":
        appointments = Appointment.query.all()
    else:
        appointments = Appointment.query.filter_by(
            user_id=g.current_user.id
        ).all()

    return {

        "citas": [

            {
                "id": appointment.id,
                "date": appointment.date,
                "time": appointment.time,
                "status": appointment.status,
                "user_id": appointment.user_id,
                "service_id": appointment.service_id
            }

            for appointment in appointments

        ]

    }


@appointments_bp.post("/")
@login_required
def create_appointment():

    data = request.get_json() or {}

    date = data.get(
        "date",
        ""
    ).strip()

    time = data.get(
        "time",
        ""
    ).strip()

    service_id = data.get(
        "service_id"
    )

    # Validaciones

    if not date or not time or not service_id:

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

    # Crear cita

    appointment = Appointment(

        date=date,
        time=time,
        user_id=g.current_user.id,
        service_id=service_id

    )

    db.session.add(appointment)
    db.session.commit()

    return {

        "mensaje": "Cita creada correctamente",

        "cita": {

            "id": appointment.id,
            "date": appointment.date,
            "time": appointment.time,
            "status": appointment.status,
            "user_id": appointment.user_id,
            "service_id": appointment.service_id

        }

    }, 201
