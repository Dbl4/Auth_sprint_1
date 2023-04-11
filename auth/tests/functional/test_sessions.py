from http import HTTPStatus
from uuid import uuid4

import pytest

from settings import settings
from tests.settings import login_user, create_user


@pytest.mark.parametrize(
    "email, password, expected_code",
    [
        (settings.test_user_email, settings.test_user_password, HTTPStatus.OK),
        ("incorrect@gmail.com", settings.test_user_password, HTTPStatus.FORBIDDEN),
        (settings.test_user_email, "incorrect-password", HTTPStatus.FORBIDDEN),
        (
            "not-valid-email",
            settings.test_user_password,
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
    ],
)
def test_login(
    test_client,
    session,
    faker,
    email,
    password,
    expected_code,
):
    """
    GIVEN
    WHEN
    THEN
    """
    create_user(session=session, admin=True)

    response = test_client.post(
        "/v1/sessions/",
        json={
            "email": email,
            "password": password,
            "user-agent": faker.user_agent(),
            "user-ip": faker.ipv4(),
        },
    )
    assert response.status_code == expected_code


def test_check(test_client, session):
    """
    GIVEN admin user is logged in
    WHEN GET /sessions/ request with access-token comes
    THEN HTTP code 200 is returned
    """
    create_user(session=session, admin=True)
    access_token, refresh_token = login_user(test_client)
    response = test_client.get(
        "/v1/sessions/",
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.status_code == HTTPStatus.OK


def test_unauthorized_permissions(test_client, session):
    """
    GIVEN User is not logged in
    WHEN User makes any request to any endpoint under /sessions/,
      except POST /sessions/
    THEN HTTP code 401 is returned
    """
    create_user(session=session, admin=True)
    access_token, refresh_token = login_user(test_client)

    response = test_client.get("/v1/sessions/")
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    response = test_client.delete("/v1/sessions/")
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    response = test_client.put(
        "/v1/sessions/",
        headers={"Authorization": "Bearer {}".format(access_token)},
        json={"refresh_token": uuid4()},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_logout(test_client, session):
    create_user(session=session, admin=True)
    access_token, refresh_token = login_user(test_client)
    response = test_client.delete(
        "/v1/sessions/",
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.status_code == HTTPStatus.OK


def test_logout_all(test_client, session):
    create_user(session=session, admin=True)
    access_token, refresh_token = login_user(test_client)
    response = test_client.delete(
        "/v1/sessions/all/",
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.status_code == HTTPStatus.OK


def test_refresh(test_client, session):
    create_user(session=session, admin=True)
    access_token, refresh_token = login_user(test_client)
    response = test_client.put(
        "/v1/sessions/",
        headers={"Authorization": "Bearer {}".format(access_token)},
        json={"refresh_token": refresh_token},
    )
    assert response.status_code == HTTPStatus.OK


def test_refresh_not_equal(test_client, session):
    create_user(session=session, admin=True)
    access_token, refresh_token = login_user(test_client)
    response = test_client.put(
        "/v1/sessions/",
        headers={"Authorization": "Bearer {}".format(access_token)},
        json={"refresh_token": refresh_token},
    )
    access = response.json["access"]
    refresh = response.json["refresh"]
    if access and refresh:
        assert access != access_token
        assert refresh != refresh_token
