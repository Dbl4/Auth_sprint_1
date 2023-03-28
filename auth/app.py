from flask_jwt_extended import JWTManager

from db import init_db
from flask import Flask
from settings import auth_postgres_url, settings

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = auth_postgres_url
app.config["JWT_SECRET_KEY"] = settings.jwt_secret_key

jwt = JWTManager(app)

app.app_context().push()
init_db(app)


@app.route("/hello")
def hello_world():
    return "Hello, World!"


def main():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
