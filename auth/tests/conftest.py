import pytest
from app import create_app
from settings import settings
from sqlalchemy.engine import URL
from db import db as _db
from flask_migrate import upgrade as flask_migrate_upgrade
from flask_migrate import downgrade as flask_migrate_downgrade
from password import hash_password
from models import User
from faker import Faker


TEST_CONFIG = {
    "TESTING": True,
    "DEBUG": True,
    "SQLALCHEMY_DATABASE_URI": URL.create(
        drivername="postgresql",
        username=settings.auth_postgres_user,
        password=settings.auth_postgres_password,
        host=settings.auth_postgres_host,
        port=settings.auth_postgres_port_test,
        database=settings.auth_postgres_db,
    ),
    "JWT_SECRET_KEY": settings.jwt_secret_key,
}


@pytest.fixture(scope="session")
def app():
    app = create_app(TEST_CONFIG)
    with app.app_context():
        yield app


@pytest.fixture(scope="function")
def test_client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def db(app, request):
    """Session-wide test database."""

    def teardown():
        flask_migrate_downgrade(directory="migrations")

    _db.app = app

    flask_migrate_upgrade(directory="migrations")
    admin = User(
        password=hash_password(settings.auth_admin_password),
        email=settings.auth_admin_email,
        is_admin=True,
    )
    _db.session.add(admin)
    _db.session.commit()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope="function")
def session(db, request):
    db.session.begin_nested()

    def commit():
        db.session.flush()

    # patch commit method
    old_commit = db.session.commit
    db.session.commit = commit

    def teardown():
        db.session.rollback()
        db.session.close()
        db.session.commit = old_commit

    request.addfinalizer(teardown)
    return db.session


def login_admin(test_client):
    faker = Faker()
    response = test_client.post(
        "/v1/sessions/",
        json={
            "email": settings.auth_admin_email,
            "password": settings.auth_admin_password,
            "user-agent": faker.user_agent(),
            "user-ip": faker.ipv4(),
        },
    )
    return response.json['access_token'], response.json['refresh_token']
