import pytest
from app import create_app, db
import os

@pytest.fixture(scope="module")
def client():
    os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    flask_app = create_app()
    flask_app.config["TESTING"] = True

    with flask_app.app_context():
        db.create_all()
        yield flask_app.test_client()
        db.drop_all()
