from flask import Blueprint, render_template

from models import Service


web_bp = Blueprint("web", __name__)


@web_bp.get("/")
def home():
    return render_template("index.html", services=Service.query.all())


@web_bp.get("/login")
def login_page():
    return render_template("auth.html", mode="login")


@web_bp.get("/register")
def register_page():
    return render_template("auth.html", mode="register")


@web_bp.get("/bookings")
def bookings_page():
    return render_template("bookings.html")


@web_bp.get("/admin")
def admin_page():
    return render_template("admin.html")
