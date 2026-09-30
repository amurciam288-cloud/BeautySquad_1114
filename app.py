import os

import click
from flask import Flask
from models import db
from models import User

from routes.auth import auth_bp
from routes.users import users_bp
from routes.services import services_bp
from routes.appointments import appointments_bp


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "development-change-me"),
        SQLALCHEMY_DATABASE_URI="sqlite:///beautysquad.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

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

    @app.cli.command("create-admin")
    @click.option("--name", prompt=True)
    @click.option("--email", prompt=True)
    @click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
    def create_admin(name, email, password):
        email = email.strip().lower()
        if User.query.filter_by(email=email).first():
            raise click.ClickException("Ese correo ya está registrado")

        admin = User(name=name.strip(), email=email, role="admin")
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        click.echo("Administrador creado correctamente")

    @app.get("/")
    def inicio():
        return {
            "mensaje": "BeautySquad API funcionando correctamente"
        }

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
