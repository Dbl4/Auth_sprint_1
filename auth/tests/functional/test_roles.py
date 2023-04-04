from app import create_app

<<<<<<< HEAD
<<<<<<< HEAD
def test_home_page_post_with_fixture(test_client):
=======
def test_create_role(test_client):
>>>>>>> 526a2c5 (Prepare tests for usage)
    """
    GIVEN 
    WHEN 
    THEN 
    """
    response = test_client.post('/roles/')
    assert response.status_code == 200
    assert b"Flask User Management Example!" not in response.data
<<<<<<< HEAD
=======
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
>>>>>>> cd0c6dc (02 tests (#11))
=======

    response = test_client.get('/roles/')
    assert response.status_code == 200
>>>>>>> 526a2c5 (Prepare tests for usage)
