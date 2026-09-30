from flask import Blueprint
from flask import request

from models import db
from models import Service
from routes.security import admin_required


services_bp = Blueprint(
    "services",
    __name__
)


def serialize_service(service):
    return {
        "id": service.id,
        "name": service.name,
        "description": service.description,
        "price": format(service.price, ".2f")
    }


@services_bp.get("/")
def list_services():

    services = Service.query.all()

    return {

        "servicios": [

            serialize_service(service)

            for service in services

        ]

    }


@services_bp.post("/")
@admin_required
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

        "servicio": serialize_service(service)

    }, 201


@services_bp.patch("/<int:service_id>")
@admin_required
def update_service(service_id):
    service = db.session.get(Service, service_id)

    if not service:
        return {"error": "El servicio no existe"}, 404

    data = request.get_json() or {}

    if "name" in data:
        name = str(data["name"]).strip()
        if not name:
            return {"error": "El nombre no puede estar vacío"}, 400
        service.name = name

    if "description" in data:
        service.description = str(data["description"]).strip()

    if "price" in data:
        try:
            price = float(data["price"])
        except (TypeError, ValueError):
            return {"error": "El precio debe ser numérico"}, 400

        if price < 0:
            return {"error": "El precio no puede ser negativo"}, 400
        service.price = price

    db.session.commit()
    return {
        "mensaje": "Servicio actualizado correctamente",
        "servicio": serialize_service(service)
    }


@services_bp.delete("/<int:service_id>")
@admin_required
def delete_service(service_id):
    service = db.session.get(Service, service_id)

    if not service:
        return {"error": "El servicio no existe"}, 404

    if service.appointments:
        return {
            "error": "No puedes eliminar un servicio con citas asociadas"
        }, 409

    db.session.delete(service)
    db.session.commit()
    return "", 204
