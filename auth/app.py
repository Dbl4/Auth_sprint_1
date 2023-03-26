from db import db, init_db
from flask import Flask
from settings import auth_postgres_url

from models import Role, User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = auth_postgres_url

app.app_context().push()
init_db(app)


@app.route("/hello")
def hello_world():
    return "Hello, World!"


def main():
    role = Role(name="actor")
    db.session.add(role)

    user = User(password="admin", email="admin@example.com", is_admin=False)
    user.roles.append(role)
    db.session.add(user)

    db.session.commit()

    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
