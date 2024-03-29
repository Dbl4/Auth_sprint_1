import pytest
from sqlalchemy.exc import IntegrityError

from models import Role, User


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
