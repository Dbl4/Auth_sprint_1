from flask import Flask
from db import db, init_db

from models import User
from flask import Flask

from settings import settings

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://"
    + settings.auth_postgres_user
    + ":"
    + settings.auth_postgres_password
    + "@"
    + settings.auth_postgres_host
    + ":"
    + str(settings.auth_postgres_port)
    + "/"
    + settings.auth_postgres_db
)

app.app_context().push()
init_db(app)


@app.route("/hello")
def hello_world():
    return "Hello, World!"


def main():
    # admin = User(password='admin', email='admin@example.com', is_admin=False)
    # db.session.add(admin)
    # db.session.commit()
    app.run(host='0.0.0.0')


if __name__ == "__main__":
    main()
