from flask import Flask
from urllib.parse import urlunsplit
<<<<<<< HEAD
<<<<<<< HEAD
=======
import pytest
>>>>>>> cd0c6dc (02 tests (#11))
=======
import pytest
>>>>>>> 526a2c5 (Prepare tests for usage)

from app import create_app
from models import User, Role
from db import db, migrate

<<<<<<< HEAD
<<<<<<< HEAD
def test_multiple_roles(session):
=======
from sqlalchemy.exc import IntegrityError

def test_duplicate_roles(session):
>>>>>>> 526a2c5 (Prepare tests for usage)
    """
    GIVEN a role with a certain name exists
    WHEN a role with the same name is added
    THEN an exception is raised
    """
    role = Role(name="actor")
    session.add(role)
    session.commit()

    with pytest.raises(IntegrityError) as excinfo:
        role2 = Role(name="actor")
        session.add(role2)
        session.commit()
    assert "duplicate key" in str(excinfo.value)


<<<<<<< HEAD
    # user = User('patkennedy79@gmail.com', 'FlaskIsAwesome')
    # assert user.email == 'patkennedy79@gmail.com'
    # assert user.hashed_password != 'FlaskIsAwesome'
    # assert user.role == 'user'
=======
from sqlalchemy.exc import IntegrityError

def test_duplicate_roles(session):
    """
    GIVEN a role with a certain name exists
    WHEN a role with the same name is added
    THEN an exception is raised
    """
    role = Role(name="actor")
    session.add(role)
    session.commit()

    with pytest.raises(IntegrityError) as excinfo:
        role2 = Role(name="actor")
        session.add(role2)
        session.commit()
    assert "duplicate key" in str(excinfo.value)


=======
>>>>>>> 526a2c5 (Prepare tests for usage)
def test_assign_role_twice(session):
    """
    GIVEN user has a certain role
    WHEN the role is assigned once again
    THEN an exception is raised
    """
    role = Role(name="actor")
    session.add(role)
    user = User(password="admin", email="admin@example.com", is_admin=False)
    session.add(user)
    user.roles.append(role)
    session.commit()

    user.roles.append(role)
    session.commit()

    # print(user.roles)
    # assert(False)

    # with pytest.raises(IntegrityError) as excinfo:
    #     user.roles.append(role)
    #     session.commit()
    # assert "duplicate key" in str(excinfo.value)
<<<<<<< HEAD
>>>>>>> cd0c6dc (02 tests (#11))
=======
>>>>>>> 526a2c5 (Prepare tests for usage)
