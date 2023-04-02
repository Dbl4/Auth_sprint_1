from flask import Flask
from sqlalchemy.engine import URL

from commands import register_commands
from settings import settings
from db import db, migrate


def create_app(config):
    app = Flask(__name__)
    app.config.update(**config)

    register_commands(app)

    from models import User, Role
    db.init_app(app)
    migrate.init_app(app, db)
    from api.v1.users import auth
    from api.v1.roles import roles
    app.register_blueprint(auth)
    app.register_blueprint(roles)

    return app

config = {}
config["SQLALCHEMY_DATABASE_URI"] = URL.create(
    drivername="postgresql",
    username=settings.auth_postgres_user,
    password=settings.auth_postgres_password,
    host=settings.auth_postgres_host,
    port=settings.auth_postgres_port,
    database=settings.auth_postgres_db
)
config["JWT_SECRET_KEY"] = settings.jwt_secret_key
app = create_app(config)

@app.route("/hello")
def hello_world():
    return "Hello, World!"


def main():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
