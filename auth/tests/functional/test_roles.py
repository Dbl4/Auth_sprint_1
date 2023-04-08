from tests.conftest import login_admin

def test_create_role(test_client, session, faker):
    """
    GIVEN 
    WHEN POST request is sent
    THEN HTTP code 200 is received, role exists in the list of roles
    """
    access_token, refresh_token = login_admin(test_client)
    name = faker.sentence(nb_words=3)
    response = test_client.post(
        "/v1/roles/",
        json={"name": name},
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.status_code == 200
    response = test_client.get(
        "/v1/roles/",
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.status_code == 200
    assert response.json[0]["name"] == name


def test_validation(test_client, session):
    """
    GIVEN 
    WHEN A request without the name field is received
    THEN HTTP code 422 is returned
    """
    access_token, refresh_token = login_admin(test_client)
    response = test_client.post(
        "/v1/roles/",
        json={"not_valid": "actor"},
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.status_code == 422
    response = test_client.post(
        "/v1/roles/",
        json={"name": "actor"},
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    response = test_client.put(
        f"/v1/roles/{response.json['id']}/",
        json={"not_valid": "actor"},
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.status_code == 422


def test_rename_role(test_client, session, faker):
    """
    GIVEN A role exists
    WHEN PUT requiest is sent
    THEN HTTP code 204 is received
    """
    access_token, refresh_token = login_admin(test_client)
    name = faker.sentence(nb_words=3)
    response = test_client.post(
        "/v1/roles/",
        json={"name": name},
        headers={"Authorization": "Bearer {}".format(access_token)},
    )    
    id = response.json["id"]

    new_name = faker.word()
    response = test_client.put(
        f"/v1/roles/{id}/",
        json={"name": new_name},
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.status_code == 204

    response = test_client.get(
        "/v1/roles/",
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.status_code == 200
    assert response.json[0]["name"] == new_name


def test_delete_role(test_client, session, faker):
    """
    GIVEN A role exists
    WHEN DELETE requiest is sent
    THEN HTTP code 204 is received
    """
    access_token, refresh_token = login_admin(test_client)
    name = faker.sentence(nb_words=3)
    response = test_client.post(
        "/v1/roles/",
        json={"name": name},
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    id = response.json["id"]

    response = test_client.delete(
        f"/v1/roles/{id}/",
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.status_code == 204

    response = test_client.get(
        "/v1/roles/",
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.json == []
