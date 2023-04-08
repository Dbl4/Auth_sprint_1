from faker import Faker
from settings import settings
from tests.conftest import login_admin


def test_login(test_client, session, faker):
    """
    GIVEN 
    WHEN 
    THEN 
    """
    response = test_client.post(
        "/v1/sessions/",
        json={
            "email": settings.auth_admin_email,
            "password": settings.auth_admin_password,
            "user-agent": faker.user_agent(),
            "user-ip": faker.ipv4(),
        },
    )
    assert response.status_code == 200


def test_check(test_client, session, faker):
    """
    GIVEN admin user is logged in
    WHEN GET /sessions/ request with access-token comes
    THEN HTTP code 200 is returned
    """
    access_token, refresh_token = login_admin(test_client)
    response = test_client.get(
        "/v1/sessions/",
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.status_code == 200
