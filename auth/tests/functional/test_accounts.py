from http import HTTPStatus

from faker import Faker
from flask_sqlalchemy.session import Session
from settings import settings
from werkzeug.test import Client

from tests.settings import create_user, login_user


def test_get(test_client: Client, session: Session) -> None:
    """
    GIVEN User exists and authrized
    WHEN GET request is sent
    THEN HTTP code 401 UNAUTHORIZED is returned

    Args:
        test_client: клиент для выполнения HTTP запросов
        session: сессия базы данных
    """
    create_user(session=session)
    access_token, _ = login_user(test_client)
    response = test_client.get(
        "/v1/accounts/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json["email"] == settings.test_user_email
    history_len = len(response.json["history"])
    assert history_len > 0

    another_access_token, _ = login_user(test_client)
    response = test_client.get(
        "/v1/accounts/",
        headers={"Authorization": f"Bearer {another_access_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json["history"]) == history_len + 1


def test_post(test_client: Client, faker: Faker) -> None:
    """
    GIVEN User is not logged in
    WHEN POST request is sent
    THEN User record added to DB (200 OK), user can't sign up
      with same credentials second time (409 CONFLICT)

    Args:
        test_client: клиент для выполнения HTTP запросов
        faker: библиотека Faker
    """
    email = faker.email("test", "example123.com")
    response = test_client.post(
        "/v1/accounts/",
        json={"email": email, "password": faker.password()},
    )
    assert response.status_code == HTTPStatus.OK
    response = test_client.post(
        "/v1/accounts/",
        json={"email": email, "password": faker.password()},
    )
    assert response.status_code == HTTPStatus.CONFLICT


def test_patch(test_client: Client, session: Session, faker: Faker) -> None:
    """
    GIVEN User exists and authorized
    WHEN PATCH request is sent
    THEN Email and/or password is changed (200 OK),
      user able to login with new credentials after that (200 OK),
      and make some other requests (200 OK)

    Args:
        test_client: клиент для выполнения HTTP запросов
        session: сессия базы данных
        faker: библиотека Faker
    """
    create_user(session=session)
    access_token, _ = login_user(test_client)
    new_password = faker.password()
    response = test_client.patch(
        "/v1/accounts/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"password": new_password},
    )
    assert response.status_code == HTTPStatus.OK
    response = test_client.get(
        "/v1/accounts/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    new_email = faker.email("test", "example123.com")
    response = test_client.patch(
        "/v1/accounts/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"email": new_email},
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
    access_token = response.json["access"]
    response = test_client.get(
        "/v1/accounts/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == HTTPStatus.OK


def test_delete(test_client: Client, session: Session) -> None:
    """
    GIVEN User exists and authorized
    WHEN DELETE request is sent
    THEN User record deleted from DB (200 OK)
      and can't sign in second time (403 FORBIDDEN)

    Args:
        test_client: клиент для выполнения HTTP запросов
        session: сессия базы данных
    """
    create_user(session=session)
    access_token, _ = login_user(test_client)
    response = test_client.delete(
        "/v1/accounts/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    try:
        login_user(test_client)
    except KeyError:
        assert True
    else:
        assert False


def test_unauthorized_permissions(test_client: Client):
    """
    GIVEN User is not logged in
    WHEN User makes any request to any endpoint under /accounts/ (except POST)
    THEN Request declined (401 UNAUTHORIZED)

    Args:
        test_client: клиент для выполнения HTTP запросов
    """
    response = test_client.get("/v1/accounts/")
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    response = test_client.patch("/v1/accounts/")
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    response = test_client.delete("/v1/accounts/")
    assert response.status_code == HTTPStatus.UNAUTHORIZED
