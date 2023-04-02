from flask import Flask
from urllib.parse import urlunsplit

from app import create_app
from models import User, Role
from db import db, migrate

def test_multiple_roles(session):
    """
    GIVEN a user with a role assigned
    WHEN the same role is assigned once again
    THEN that an error is raised
    """
    role1 = Role(name="actor")
    role2 = Role(name="actor")
    session.add(role1)
    # session.add(role2)
    session.commit()

    # user = User(password="admin", email="admin@example.com", is_admin=False)
    # user.roles.append(role1)
    # user.roles.append(role1)
    # user.roles.append(role2)
    # db.session.add(user)

    # db.session.commit()

    # user = User('patkennedy79@gmail.com', 'FlaskIsAwesome')
    # assert user.email == 'patkennedy79@gmail.com'
    # assert user.hashed_password != 'FlaskIsAwesome'
    # assert user.role == 'user'
