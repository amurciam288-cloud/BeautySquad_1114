from flask import Blueprint
from flask import request

from models import db
from models import Service


services_bp = Blueprint(
    "services",
    __name__
)


@services_bp.get("/")
def list_services():

    services = Service.query.all()

    return {

        "servicios": [

            {
                "id": service.id,
                "name": service.name,
                "description": service.description,
                "price": service.price
            }

            for service in services

        ]

    }


@services_bp.post("/")
def create_service():

    data = request.get_json() or {}

    name = data.get(
        "name",
        ""
    ).strip()

    description = data.get(
        "description",
        ""
    ).strip()

    price = data.get("price")

    # Validaciones

    if not name or price is None:

        return {
            "error": "Nombre y precio son obligatorios"
        }, 400

    try:

        price = float(price)

    except (TypeError, ValueError):

        return {
            "error": "El precio debe ser numérico"
        }, 400

    if price < 0:

        return {
            "error": "El precio no puede ser negativo"
        }, 400

    # Crear servicio

    service = Service(
        name=name,
        description=description,
        price=price
    )

    db.session.add(service)
    db.session.commit()

    return {

        "mensaje": "Servicio creado correctamente",

        "servicio": {

            "id": service.id,
            "name": service.name,
            "description": service.description,
            "price": service.price

        }

    }, 201
