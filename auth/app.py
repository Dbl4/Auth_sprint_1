from flask import Flask
from urllib.parse import urlunsplit

from commands import register_commands
from settings import settings


def create_app(config_filename):
    app = Flask(__name__)
    # app.config.from_pyfile(config_filename)
    app.config["SQLALCHEMY_DATABASE_URI"] = urlunsplit(
        (
            "postgresql",
            (
                f"{settings.auth_postgres_user}"
                f":{settings.auth_postgres_password}"
                f"@{settings.auth_postgres_host}"
                f":{settings.auth_postgres_port}"
            ),
            settings.auth_postgres_db,
            "",
            "",
        ),
    )
    app.config["JWT_SECRET_KEY"] = settings.jwt_secret_key

    register_commands(app)

    from db import init_db
    init_db(app)

    from api.v1.users import auth
    from api.v1.roles import roles
    app.register_blueprint(auth)
    app.register_blueprint(roles)

    return app

app = create_app(None)

@app.route("/hello")
def hello_world():
    return "Hello, World!"


def main():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
