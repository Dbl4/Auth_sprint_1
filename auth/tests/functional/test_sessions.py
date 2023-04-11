from http import HTTPStatus

from settings import settings
from tests.settings import login_user, create_user


def test_login(test_client, session, faker):
    """
    GIVEN 
    WHEN 
    THEN 
    """
    create_user(session=session, admin=True)

    response = test_client.post(
        "/v1/sessions/",
        json={
            "email": settings.test_user_email,
            "password": settings.test_user_password,
            "user-agent": faker.user_agent(),
            "user-ip": faker.ipv4(),
        },
    )
    assert response.status_code == HTTPStatus.OK


def test_check(test_client, session, faker):
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
    response = test_client.get("/v1/sessions/")
    assert response.status_code == HTTPStatus.UNAUTHORIZED
