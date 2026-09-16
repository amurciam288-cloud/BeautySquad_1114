from flask import Flask
from models import db

from routes.auth import auth_bp
from routes.users import users_bp
from routes.services import services_bp
from routes.appointments import appointments_bp


def create_app():

    app = Flask(__name__)

    # Configuración de la base de datos
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///beautysquad.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Conectar base de datos
    db.init_app(app)

    # Registrar rutas
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(services_bp, url_prefix="/api/services")
    app.register_blueprint(
        appointments_bp,
        url_prefix="/api/appointments"
    )

    # Crear las tablas
    with app.app_context():
        db.create_all()

    @app.get("/")
    def inicio():
        return {
            "mensaje": "BeautySquad API funcionando correctamente"
        }

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)