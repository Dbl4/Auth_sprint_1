from flask_jwt_extended import JWTManager

from api.v1.users import auth
from db import init_db
from flask import Flask
from urllib.parse import urlunsplit

from settings import auth_postgres_url, settings

from commands import register_commands
from models import User, Role
from api.v1.users import auth
from api.v1.roles import roles
from db import init_db
from flask import Flask

from settings import settings

app = Flask(__name__)
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
app.register_blueprint(auth)
app.register_blueprint(roles)

app.config["JWT_SECRET_KEY"] = settings.jwt_secret_key
jwt = JWTManager(app)
app.register_blueprint(auth)
app.register_blueprint(roles)

app.app_context().push()
init_db(app)
register_commands(app)

@app.route("/hello")
def hello_world():
    return "Hello, World!"


def main():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
