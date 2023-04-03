from app import create_app


def test_create_role(test_client):
    """
    GIVEN 
    WHEN 
    THEN 
    """
    response = test_client.post('/roles/')
    assert response.status_code == 200
    assert b"Flask User Management Example!" not in response.data

    response = test_client.get('/roles/')
    assert response.status_code == 200
