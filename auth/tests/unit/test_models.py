from flask import Flask
from urllib.parse import urlunsplit

from auth.models import User, Role
from auth.db import db, init_db

def test_multiple_roles():
    """
    GIVEN a user with a role assigned
    WHEN the same role is assigned once again
    THEN that an error is raised
    """
    # app = Flask(__name__)
    # app.config["SQLALCHEMY_DATABASE_URI"] = urlunsplit(
    #     (
    #         "postgresql",
    #         (
    #             f"{settings.auth_postgres_user}"
    #             f":{settings.auth_postgres_password}"
    #             f"@{settings.auth_postgres_host}"
    #             f":{settings.auth_postgres_port}"
    #         ),
    #         settings.auth_postgres_db,
    #         "",
    #         "",
    #     ),
    # )

    # app.app_context().push()
    # init_db(app)

    role = Role(name='actor')
    db.session.add(role)

    user = User(password='admin', email='admin@example.com', is_admin=False)
    user.roles.append(role)
    db.session.add(user)

    db.session.commit()

    # user = User('patkennedy79@gmail.com', 'FlaskIsAwesome')
    # assert user.email == 'patkennedy79@gmail.com'
    # assert user.hashed_password != 'FlaskIsAwesome'
    # assert user.role == 'user'
