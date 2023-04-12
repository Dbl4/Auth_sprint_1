from http import HTTPStatus

from faker import Faker
from flask_sqlalchemy.session import Session
from werkzeug.test import Client

from settings import settings
from tests.settings import login_user, create_user


def test_get(test_client: Client, session: Session) -> None:
    create_user(session=session)
    access_token, _ = login_user(test_client)
    response = test_client.get(
        "/v1/accounts/",
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json["email"] == settings.test_user_email
    history_len = len(response.json["history"])
    assert history_len > 0

    another_access_token, _ = login_user(test_client)
    response = test_client.get(
        "/v1/accounts/",
        headers={"Authorization": "Bearer {}".format(another_access_token)},
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json["history"]) == history_len + 1


def test_post(test_client: Client, faker: Faker) -> None:
    email = faker.email('test', 'example123.com')
    response = test_client.post(
        "/v1/accounts/",
        json={'email': email, 'password': faker.password()},
    )
    assert response.status_code == HTTPStatus.OK
    response = test_client.post(
        "/v1/accounts/",
        json={'email': email, 'password': faker.password()},
    )
    assert response.status_code == HTTPStatus.CONFLICT


def test_patch(test_client: Client, session: Session, faker: Faker) -> None:
    create_user(session=session)
    access_token, _ = login_user(test_client)
    new_password = faker.password()
    response = test_client.patch(
        "/v1/accounts/",
        headers={"Authorization": "Bearer {}".format(access_token)},
        json={'password': new_password},
    )
    assert response.status_code == HTTPStatus.OK
    response = test_client.get(
        "/v1/accounts/",
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.status_code == HTTPStatus.OK
    new_email = faker.email('test', 'example123.com')
    response = test_client.patch(
        "/v1/accounts/",
        headers={"Authorization": "Bearer {}".format(access_token)},
        json={'email': new_email},
    )
    assert response.status_code == HTTPStatus.OK
    response = test_client.post(
        "/v1/sessions/",
        json={
            "email": new_email,
            "password": new_password,
            "user-agent": faker.user_agent(),
            "user-ip": faker.ipv4(),
        },
    )
    assert response.status_code == HTTPStatus.OK
    response = test_client.get(
        "/v1/accounts/",
        headers={"Authorization": "Bearer {}".format(response.json["access"])},
    )
    assert response.status_code == HTTPStatus.OK




def test_delete(test_client: Client, session: Session) -> None:
    create_user(session=session)
    access_token, _ = login_user(test_client)
    response = test_client.delete(
        "/v1/accounts/",
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.status_code == HTTPStatus.OK
    try:
        login_user(test_client)
    except KeyError:
        assert True
    else:
        assert False


def test_unauthorized_permissions(test_client: Client):
    response = test_client.get("/v1/accounts/")
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    response = test_client.patch("/v1/accounts/")
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    response = test_client.delete("/v1/accounts/")
    assert response.status_code == HTTPStatus.UNAUTHORIZED
