from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


db = SQLAlchemy()


class User(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(30),
        nullable=False,
        default="client"
    )

    appointments = db.relationship(
        "Appointment",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def set_password(self, password):

        self.password_hash = generate_password_hash(
            password
        )

    def check_password(self, password):

        return check_password_hash(
            self.password_hash,
            password
        )


class Service(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.String(255)
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    appointments = db.relationship(
        "Appointment",
        back_populates="service"
    )


class Appointment(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    date = db.Column(
        db.String(20),
        nullable=False
    )

    time = db.Column(
        db.String(10),
        nullable=False
    )

    status = db.Column(
        db.String(30),
        default="pending"
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    service_id = db.Column(
        db.Integer,
        db.ForeignKey("service.id"),
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="appointments"
    )

    service = db.relationship(
        "Service",
        back_populates="appointments"
    )