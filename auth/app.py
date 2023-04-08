from flask import Flask

from api import v1
from flask_cors import CORS

from cli import register_cli
from settings import config
from db import db, migrate
from tokens import register_tokens


def create_app(config):
    app = Flask(__name__)
    CORS(app)
    app.config.update(**config)

    register_cli(app)
    register_tokens(app)

    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(v1)

    return app


app = create_app(config)


def main():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
