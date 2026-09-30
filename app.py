import os

import click
from flask import Flask
from config import Config
from models import db
from models import migrate
from models import User

from routes.auth import auth_bp
from routes.users import users_bp
from routes.services import services_bp
from routes.appointments import appointments_bp
from routes.web import web_bp


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_mapping(Config.values())

    if test_config:
        app.config.update(test_config)

    # Conectar base de datos
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar rutas
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(services_bp, url_prefix="/api/services")
    app.register_blueprint(
        appointments_bp,
        url_prefix="/api/appointments"
    )
    app.register_blueprint(web_bp)

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

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
