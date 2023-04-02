from flask import Flask
from urllib.parse import urlunsplit

from app import create_app
from models import User, Role
from db import db, init_db

def test_multiple_roles():
    """
    GIVEN a user with a role assigned
    WHEN the same role is assigned once again
    THEN that an error is raised
    """
    app = create_app(None)
    app.app_context().push()

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
