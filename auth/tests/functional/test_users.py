from http import HTTPStatus

import pytest
from faker import Faker
from flask_sqlalchemy.session import Session
from settings import settings
from werkzeug.test import Client

from tests.settings import create_user, login_user


def test_get_users(
    test_client: Client,
    session: Session,
    faker: Faker,
) -> None:
    """
    GIVEN admin user is logged in
    WHEN GET request is sent
    THEN HTTP code 200 is returned

    Args:
        test_client: клиент для выполнения HTTP запросов
        session: сессия базы данных
        faker: библиотека Faker
    """
    create_user(
        session=session,
        email=faker.email("test", "example123.com"),
        password=faker.password(),
    )
    create_user(session=session, admin=True)
    access_token, _ = login_user(test_client)
    response = test_client.get(
        "/v1/users/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json) == 2


def test_get_user_detail(test_client: Client, session: Session) -> None:
    """
    GIVEN admin user is logged in
    WHEN GET request is sent
    THEN HTTP code 200 is returned

    Args:
        test_client: клиент для выполнения HTTP запросов
        session: сессия базы данных
    """
    user_id = create_user(session=session, admin=True)
    access_token, _ = login_user(test_client)
    response = test_client.get(
        f"/v1/users/{user_id}/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json["email"] == settings.test_user_email
    history_len = len(response.json["history"])
    assert history_len > 0

    another_access_token, _ = login_user(test_client)
    response = test_client.get(
        f"/v1/users/{user_id}/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json["history"]) == history_len + 1


@pytest.mark.parametrize(
    "new_email, new_password, expected_code",
    [
        (
            settings.test_user_email,
            settings.test_user_password,
            HTTPStatus.CONFLICT,
        ),
        ("test@gmail.com", settings.test_user_password, HTTPStatus.OK),
        (settings.test_user_email, "test-password", HTTPStatus.OK),
        (
            "not-valid-email",
            settings.test_user_password,
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
    ],
)
def test_change(
    test_client: Client,
    session: Session,
    new_email,
    new_password,
    expected_code,
) -> None:
    """
    GIVEN admin user is logged in
    WHEN PATCH request is sent
    THEN Email and/or password is changed (200 OK)

    Args:
        test_client: клиент для выполнения HTTP запросов
        session: сессия базы данных
    """
    user_id = create_user(session=session, admin=True)
    access_token, _ = login_user(test_client)
    response = test_client.patch(
        f"/v1/users/{user_id}/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "email": new_email,
            "password": new_password,
        },
    )
    assert response.status_code == expected_code


def test_delete_user(test_client: Client, session: Session) -> None:
    """
    GIVEN admin user is logged in
    WHEN DELETE request is sent
    THEN User record deleted from DB (200 OK)
      and can't sign in second time (403 FORBIDDEN)

    Args:
        test_client: клиент для выполнения HTTP запросов
        session: сессия базы данных
    """
    user_id = create_user(session=session, admin=True)
    access_token, _ = login_user(test_client)
    response = test_client.delete(
        f"/v1/users/{user_id}/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    try:
        login_user(test_client)
    except KeyError:
        assert True
    else:
        assert False


def test_unauthorized_permissions(
    test_client: Client,
    session: Session,
):
    """
    GIVEN Admin is not logged in
    WHEN Admin makes any request to any endpoint under /users/ (except POST)
    THEN Request declined (401 UNAUTHORIZED)

    Args:
        test_client: клиент для выполнения HTTP запросов
        session: сессия базы данных
    """
    user_id = create_user(session=session, admin=True)
    response = test_client.get("/v1/users/")
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    response = test_client.get(f"/v1/users/{user_id}/")
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    response = test_client.patch(f"/v1/users/{user_id}/")
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    response = test_client.delete(f"/v1/users/{user_id}/")
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    response = test_client.put(
        f"/v1/users/{user_id}/roles/008ba9ea-4613-4466-a666-bc4a6617397f/",
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    response = test_client.delete(
        f"/v1/users/{user_id}/roles/008ba9ea-4613-4466-a666-bc4a6617397f/",
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_for_forbidden_permissions(
    test_client: Client,
    session: Session,
):
    """
    GIVEN Admin is not logged in
    WHEN Admin makes any request to any endpoint under /accounts/ (except POST)
    THEN Request declined FORBIDDEN

    Args:
        test_client: клиент для выполнения HTTP запросов
        session: сессия базы данных
    """
    user_id = create_user(session=session)
    access_token, _ = login_user(test_client)
    response = test_client.get(
        "/v1/users/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    response = test_client.get(
        f"/v1/users/{user_id}/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    response = test_client.patch(
        f"/v1/users/{user_id}/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    response = test_client.delete(
        f"/v1/users/{user_id}/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    response = test_client.put(
        f"/v1/users/{user_id}/roles/008ba9ea-4613-4466-a666-bc4a6617397f/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    response = test_client.delete(
        f"/v1/users/{user_id}/roles/008ba9ea-4613-4466-a666-bc4a6617397f/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_get_user_roles(test_client: Client, session: Session) -> None:
    """
    GIVEN admin user is logged in
    WHEN DELETE request is sent
    THEN HTTP code 200 is returned

    Args:
        test_client: клиент для выполнения HTTP запросов
        session: сессия базы данных
    """
    user_id = create_user(session=session, admin=True)
    access_token, _ = login_user(test_client)
    response = test_client.get(
        f"/v1/users/{user_id}/roles/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == HTTPStatus.OK


def test_put_user_roles(
    test_client: Client,
    session: Session,
    faker: Faker,
) -> None:
    """
    GIVEN admin user is logged in
    WHEN DELETE request is sent
    THEN HTTP code 200 is returned

    Args:
        test_client: клиент для выполнения HTTP запросов
        session: сессия базы данных
        faker: библиотека Faker
    """
    user_id = create_user(session=session, admin=True)
    access_token, _ = login_user(test_client)
    name = faker.sentence(nb_words=3)
    test_client.post(
        "/v1/roles/",
        json={"name": name},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response = test_client.get(
        "/v1/roles/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    role_id = response.json[0]["id"]

    response = test_client.put(
        f"/v1/users/{user_id}/roles/{role_id}/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == HTTPStatus.OK


def test_delete_user_roles(
    test_client: Client,
    session: Session,
    faker: Faker,
) -> None:
    """
    GIVEN admin user is logged in
    WHEN DELETE request is sent
    THEN HTTP code 200 is returned

    Args:
        test_client: клиент для выполнения HTTP запросов
        session: сессия базы данных
        faker: библиотека Faker
    """
    user_id = create_user(session=session, admin=True)
    access_token, _ = login_user(test_client)
    name = faker.sentence(nb_words=3)
    test_client.post(
        "/v1/roles/",
        json={"name": name},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response = test_client.get(
        "/v1/roles/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    role_id = response.json[0]["id"]

    test_client.put(
        f"/v1/users/{user_id}/roles/{role_id}/",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    response = test_client.delete(
        f"/v1/users/{user_id}/roles/{role_id}/",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == HTTPStatus.OK
