import pytest
from app import create_app
from db import sql
from flask_migrate import downgrade as flask_migrate_downgrade
from flask_migrate import upgrade as flask_migrate_upgrade
from settings import settings
from sqlalchemy.engine import URL

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
    "JWT_ENCODE_NBF": False,
    "REDIS_HOST": settings.auth_redis_host,
    "REDIS_PORT": settings.auth_redis_port,
    "ACCESS_TOKEN_MINUTES": settings.auth_access_token_minutes,
    "REFRESH_TOKEN_MINUTES": settings.auth_refresh_token_minutes,
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

    sql.app = app
    flask_migrate_upgrade(directory="migrations")
    request.addfinalizer(teardown)
    return sql


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
