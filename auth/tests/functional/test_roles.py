from uuid import uuid4

from tests.settings import create_user, login_user


def test_create_role(test_client, session, faker):
    """
    GIVEN
    WHEN POST request is sent
    THEN HTTP code 200 is received, role exists in the list of roles

    Args:
        test_client: клиент для выполнения HTTP запросов
        session: сессия базы данных
        faker: библиотека Faker
    """
    create_user(session=session, admin=True)
    access_token, refresh_token = login_user(test_client)
    name = faker.sentence(nb_words=3)
    response = test_client.post(
        "/v1/roles/",
        json={"name": name},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response = test_client.get(
        "/v1/roles/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert response.json[0]["name"] == name


def test_validation(test_client, session):
    """
    GIVEN
    WHEN A request without the name field is received
    THEN HTTP code 422 is returned

    Args:
        test_client: клиент для выполнения HTTP запросов
        session: сессия базы данных
    """
    create_user(session=session, admin=True)
    access_token, refresh_token = login_user(test_client)
    response = test_client.post(
        "/v1/roles/",
        json={"not_valid": "actor"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 422
    response = test_client.post(
        "/v1/roles/",
        json={"name": "actor"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response = test_client.put(
        f"/v1/roles/{response.json['id']}/",
        json={"not_valid": "actor"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 422


def test_rename_role(test_client, session, faker):
    """
    GIVEN A role exists
    WHEN PUT requiest is sent
    THEN HTTP code 204 is received

    Args:
        test_client: клиент для выполнения HTTP запросов
        session: сессия базы данных
        faker: библиотека Faker
    """
    create_user(session=session, admin=True)
    access_token, refresh_token = login_user(test_client)
    name = faker.sentence(nb_words=3)
    response = test_client.post(
        "/v1/roles/",
        json={"name": name},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    role_id = response.json["id"]

    new_name = faker.word()
    response = test_client.put(
        f"/v1/roles/{role_id}/",
        json={"name": new_name},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204

    response = test_client.get(
        "/v1/roles/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert response.json[0]["name"] == new_name


def test_delete_role(test_client, session, faker):
    """
    GIVEN A role exists
    WHEN DELETE requiest is sent
    THEN HTTP code 204 is received

    Args:
        test_client: клиент для выполнения HTTP запросов
        session: сессия базы данных
        faker: библиотека Faker
    """
    user_id = create_user(session=session, admin=True)
    access_token, _ = login_user(test_client)
    name = faker.sentence(nb_words=3)
    response = test_client.post(
        "/v1/roles/",
        json={"name": name},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    role_id = response.json["id"]

    test_client.put(
        f"/v1/users/{user_id}/roles/{role_id}/",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    response = test_client.delete(
        f"/v1/roles/{role_id}/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204

    response = test_client.get(
        "/v1/roles/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.json == []


def test_unauthorized_permissions(test_client):
    """
    GIVEN User is not logged in
    WHEN User makes any request to any endpoint under /roles/
    THEN HTTP code 401 is returned

    Args:
        test_client: клиент для выполнения HTTP запросов
    """
    response = test_client.get("/v1/roles/")
    assert response.status_code == 401
    response = test_client.post("/v1/roles/")
    assert response.status_code == 401
    response = test_client.put(f"/v1/roles/{uuid4()}/")
    assert response.status_code == 401
    response = test_client.delete(f"/v1/roles/{uuid4()}/")
    assert response.status_code == 401


def test_user_permissions(test_client, session):
    """
    Args:
        test_client: клиент для выполнения HTTP запросов
        session: сессия базы данных
    """
    create_user(session=session, admin=False)
    access_token, refresh_token = login_user(test_client)
    response = test_client.get(
        "/v1/roles/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response = test_client.post(
        "/v1/roles/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response = test_client.put(
        f"/v1/roles/{uuid4()}/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response = test_client.delete(
        f"/v1/roles/{uuid4()}/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 403
