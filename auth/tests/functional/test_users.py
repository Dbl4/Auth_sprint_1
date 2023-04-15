from http import HTTPStatus

import faker
from faker import Faker
from flask_sqlalchemy.session import Session
from werkzeug.test import Client

from settings import settings
from tests.settings import login_user, create_user


def test_get_users(test_client: Client, session: Session, faker: Faker) -> None:
    """
    GIVEN admin user is logged in
    WHEN GET request is sent
    THEN HTTP code 200 is returned
    """
    create_user(
        session=session,
        email=faker.email('test', 'example123.com'),
        password=faker.password()
    )
    create_user(session=session, admin=True)
    access_token, _ = login_user(test_client)
    response = test_client.get(
        "/v1/users/",
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json) == 2


def test_get_user_detail(test_client: Client, session: Session) -> None:
    """
    GIVEN admin user is logged in
    WHEN GET request is sent
    THEN HTTP code 200 is returned
    """
    create_user(session=session, admin=True)
    access_token, _ = login_user(test_client)
    response = test_client.get(
        "/v1/users/",
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.status_code == HTTPStatus.OK


