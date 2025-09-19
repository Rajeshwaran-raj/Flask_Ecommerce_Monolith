import pytest
from app import create_app
from app.extensions import db

@pytest.fixture
def app_context():
    app = create_app()
    app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite:///:memory:")
    with app.app_context():
        db.create_all()
        yield app
