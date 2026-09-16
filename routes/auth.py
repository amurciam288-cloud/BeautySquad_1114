from flask import Blueprint, request

from models import db
from models import User


auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.post("/register")
def register():

    data = request.get_json() or {}

    name = data.get(
        "name",
        ""
    ).strip()

    email = data.get(
        "email",
        ""
    ).strip().lower()

    password = data.get(
        "password",
        ""
    )

    role = data.get(
        "role",
        "client"
    )

    # Validaciones

    if not name or not email or not password:

        return {
            "error": "Nombre, correo y contraseña son obligatorios"
        }, 400

    if "@" not in email:

        return {
            "error": "El correo no es válido"
        }, 400

    if len(password) < 6:

        return {
            "error": "La contraseña debe tener mínimo 6 caracteres"
        }, 400

    if role not in ("client", "admin"):

        return {
            "error": "Rol no válido"
        }, 400

    # Comprobar usuario existente

    existing_user = User.query.filter_by(
        email=email
    ).first()

    if existing_user:

        return {
            "error": "El correo ya está registrado"
        }, 409

    # Crear usuario

    user = User(
        name=name,
        email=email,
        role=role
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return {

        "mensaje": "Usuario registrado correctamente",

        "usuario": {

            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role

        }

    }, 201


@auth_bp.post("/login")
def login():

    data = request.get_json() or {}

    email = data.get(
        "email",
        ""
    ).strip().lower()

    password = data.get(
        "password",
        ""
    )

    user = User.query.filter_by(
        email=email
    ).first()

    if not user or not user.check_password(password):

        return {
            "error": "Correo o contraseña incorrectos"
        }, 401

    return {

        "mensaje": "Inicio de sesión correcto",

        "usuario": {

            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role

        }

    }


@auth_bp.post("/logout")
def logout():

    return {
        "mensaje": "Sesión cerrada correctamente"
    }