from faker import Faker


def test_create_role(test_client, session, faker):
    """
    GIVEN 
    WHEN POST request is sent
    THEN HTTP code 200 is received, role exists in the list of roles
    """
    name = faker.sentence(nb_words=3)
    response = test_client.post("/roles/", json={"name": name})
    assert response.status_code == 200

    response = test_client.get("/roles/")
    assert response.status_code == 200
    assert response.json[0]["name"] == name


def test_request_validation(test_client, session):
    """
    GIVEN 
    WHEN A request without the name field is received
    THEN HTTP code 422 is returned
    """
    response = test_client.post('/roles/', json={"not_valid": "actor"})
    assert response.status_code == 422

    response = test_client.post('/roles/', json={"name": "actor"})
    response = test_client.put(f"/roles/{response.json['id']}/", json={"not_valid": "actor"})
    assert response.status_code == 422


def test_rename_role(test_client, session, faker):
    """
    GIVEN A role exists
    WHEN PUT requiest is sent
    THEN HTTP code 204 is received
    """
    name = faker.sentence(nb_words=3)
    response = test_client.post("/roles/", json={"name": name})
    id = response.json["id"]

    new_name = faker.word()
    response = test_client.put(f"/roles/{id}/", json={"name": new_name})
    assert response.status_code == 204

    response = test_client.get("/roles/")
    assert response.status_code == 200
    assert response.json[0]["name"] == new_name


def test_delete_role(test_client, session, faker):
    """
    GIVEN A role exists
    WHEN DELETE requiest is sent
    THEN HTTP code 204 is received
    """
    name = faker.sentence(nb_words=3)
    response = test_client.post("/roles/", json={"name": name})
    id = response.json["id"]

    response = test_client.delete(f"/roles/{id}/")
    assert response.status_code == 204

    response = test_client.get("/roles/")
    assert response.json == []
