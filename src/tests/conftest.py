import pytest

from src import create_app
from src.settings.extensions import db


@pytest.fixture()
def app(tmp_path):
    config = {
        "TESTING": True,
        "SECRET_KEY": "test-secret",
        "JWT_SECRET_KEY": "test-jwt-secret-with-at-least-32-bytes",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
        "UPLOAD_FOLDER": str(tmp_path / "uploads"),
    }
    app = create_app(config)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()
