from functools import wraps

from flask import g, session

from models import db
from models import User


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        user_id = session.get("user_id")
        user = db.session.get(User, user_id) if user_id else None

        if not user:
            session.clear()
            return {"error": "Debes iniciar sesión"}, 401

        g.current_user = user
        return view(*args, **kwargs)

    return wrapped_view


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped_view(*args, **kwargs):
        if g.current_user.role != "admin":
            return {"error": "No tienes permisos de administrador"}, 403

        return view(*args, **kwargs)

    return wrapped_view
