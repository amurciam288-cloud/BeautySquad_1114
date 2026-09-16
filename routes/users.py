from flask import Blueprint

from models import User


users_bp = Blueprint(
    "users",
    __name__
)


@users_bp.get("/")
def list_users():

    users = User.query.all()

    return {

        "usuarios": [

            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            }

            for user in users

        ]

    }