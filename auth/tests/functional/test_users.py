from http import HTTPStatus

from faker import Faker
from flask_sqlalchemy.session import Session
from werkzeug.test import Client

from settings import settings
from tests.settings import login_user, create_user


def test_get_users(test_client: Client, session: Session) -> None:
    create_user(session=session, admin=True)
    access_token, _ = login_user(test_client)
    response = test_client.get(
        "/v1/users/",
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.status_code == HTTPStatus.OK
