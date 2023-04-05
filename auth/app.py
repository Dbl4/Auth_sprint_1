from flask import Flask
from flask_jwt_extended import JWTManager

from api import v1
from sqlalchemy.engine import URL
from flask_cors import CORS

from commands import register_commands
from settings import settings, config, auth_postgres_url
from db import db, migrate


def create_app(config):
    app = Flask(__name__)
    CORS(app)
    app.config.update(**config)
    jwt = JWTManager(app)

    register_commands(app)

    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(v1)

    return app


config["SQLALCHEMY_DATABASE_URI"] = auth_postgres_url
config["JWT_SECRET_KEY"] = settings.jwt_secret_key
app = create_app(config)


@app.route("/hello")
def hello_world():
    return "Hello, World!"


def main():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
