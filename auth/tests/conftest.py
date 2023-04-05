import pytest
from app import create_app
from settings import settings
from sqlalchemy.engine import URL
from db import db as _db
from flask_migrate import upgrade as flask_migrate_upgrade
from flask_migrate import downgrade as flask_migrate_downgrade


TEST_CONFIG = {
    'TESTING': True,
    'DEBUG': True,
    'SQLALCHEMY_DATABASE_URI': URL.create(
        drivername="postgresql",
        username=settings.auth_postgres_user,
        password=settings.auth_postgres_password,
        host=settings.auth_postgres_host,
        port=settings.auth_postgres_port,
        database=settings.auth_postgres_db,
    ),
    "JWT_SECRET_KEY": settings.jwt_secret_key,
}

@pytest.fixture(scope="session")
def app():    
    app = create_app(config=TEST_CONFIG)    
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
