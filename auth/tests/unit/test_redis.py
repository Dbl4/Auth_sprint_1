from tokens import put_token
from tests.settings import login_user, create_user


def test_put_token(test_client, session):
    """
    GIVEN 
    WHEN 
    THEN 
    """
    create_user(session=session, admin=True)
    access_token, refresh_token = login_user(test_client)
    # put_token()
    print(access_token)
    # assert False
