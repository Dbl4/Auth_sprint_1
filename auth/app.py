import db
from api import v1
from cli import register_cli
from flask import Flask
from flask_cors import CORS
from redis import StrictRedis
from settings import config
from tokens import register_tokens


def create_app(config):
    app = Flask(__name__)
    CORS(app)
    app.config.update(**config)

    register_cli(app)
    register_tokens(app)

    db.sql.init_app(app)
    db.migrate.init_app(app, db.sql)
    app.register_blueprint(v1)

    db.redis = StrictRedis(
        host=config["REDIS_HOST"],
        port=config["REDIS_PORT"],
        decode_responses=True,
    )
    return app


app = create_app(config)


def main():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
