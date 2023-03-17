from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from settings import settings

db = SQLAlchemy()


def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.auth_postgres_url
    db.init_app(app)
