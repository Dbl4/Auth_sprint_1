from app import create_app

<<<<<<< HEAD
def test_home_page_post_with_fixture(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is is posted to (POST)
    THEN check that a '405' status code is returned
    """
    response = test_client.post('/')
    assert response.status_code == 404
    assert b"Flask User Management Example!" not in response.data
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
