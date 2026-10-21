from flask import Blueprint, render_template

from models import Service
from models import TeamMember


web_bp = Blueprint("web", __name__)


@web_bp.get("/")
def home():
    return render_template(
        "index.html",
        services=Service.query.all(),
        team_members=TeamMember.query.all(),
        current_page="home",
    )


@web_bp.get("/login")
def login_page():
    return render_template("auth.html", mode="login", current_page="auth")


@web_bp.get("/register")
def register_page():
    return render_template("auth.html", mode="register", current_page="auth")


@web_bp.get("/bookings")
def bookings_page():
    return render_template("bookings.html", current_page="bookings")


@web_bp.get("/admin")
def admin_page():
    return render_template("admin.html", current_page="admin")
