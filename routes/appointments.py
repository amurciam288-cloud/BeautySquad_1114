from flask import Blueprint
from flask import request

from models import db
from models import User
from models import Service
from models import Appointment


appointments_bp = Blueprint(
    "appointments",
    __name__
)


@appointments_bp.get("/")
def list_appointments():

    appointments = Appointment.query.all()

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

    user_id = data.get(
        "user_id"
    )

    service_id = data.get(
        "service_id"
    )

    # Validaciones

    if not date or not time or not user_id or not service_id:

        return {
            "error": "Fecha, hora, usuario y servicio son obligatorios"
        }, 400

    user = db.session.get(
        User,
        user_id
    )

    if not user:

        return {
            "error": "El usuario no existe"
        }, 404

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
        user_id=user_id,
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