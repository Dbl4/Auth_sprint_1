from flask_jwt_extended import JWTManager

from db import db, init_db
from flask import Flask
from settings import auth_postgres_url

from models import Role, User
from utils import hash_password, is_correct_password, create_tokens

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = auth_postgres_url

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "fd08b18e863a9635534b297cc39efe99a6f49cfae6a1f33eb21f9c3dc97c0466"
jwt = JWTManager(app)

app.app_context().push()
init_db(app)


@app.route("/hello")
def hello_world():
    return "Hello, World!"


def main():
    # role = Role(name="actor")
    # db.session.add(role)
    #
    # user = User(password="admin", email="admin@example.com", is_admin=False)
    # user.roles.append(role)
    # db.session.add(user)
    #
    # db.session.commit()
    print(hash_password('123456'))
    print(is_correct_password(hash_password('123456'), '123476'))
    print(create_tokens('test'))

    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
