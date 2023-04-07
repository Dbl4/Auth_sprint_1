from flask import Flask
from flask_jwt_extended import JWTManager

from api import v1
from flask_cors import CORS

from commands import register_commands
from settings import config
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


app = create_app(config)


@app.route("/hello")
def hello_world():
    return "Hello, World!"


def main():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
