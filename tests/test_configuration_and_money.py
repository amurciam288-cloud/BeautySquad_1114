from decimal import Decimal

from app import create_app
from models import Service, db


def test_environment_values_configure_the_application(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "environment-secret")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///environment.db")

    app = create_app()

    assert app.config["SECRET_KEY"] == "environment-secret"
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///environment.db"


def test_service_prices_are_stored_as_decimal_values(app):
    with app.app_context():
        service = Service(name="Brows", price=Decimal("19.99"))
        db.session.add(service)
        db.session.commit()
        db.session.refresh(service)

        assert isinstance(service.price, Decimal)
        assert service.price == Decimal("19.99")
