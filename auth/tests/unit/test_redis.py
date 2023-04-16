from flask_jwt_extended import decode_token
from tokens import count_tokens, delete_all_tokens, delete_token, get_token
from tokens import put_token

from tests.settings import create_user, login_user


def test_get_token(test_client, session):
    """
    GIVEN A User exists
    WHEN User logs in
    THEN get_token() returns correct refresh token
        and count_tokens() returns 1

    Args:
        test_client: клиент для выполнения HTTP запросов
        session: сессия базы данных
    """
    user_id = create_user(session=session, admin=True)
    access_token, refresh_token = login_user(test_client)
    jti = str(decode_token(access_token)["jti"])
    assert refresh_token == get_token(user_id=user_id, jti=jti)
    assert count_tokens(user_id=user_id) == 1


def test_delete_token(test_client, session):
    """
    GIVEN User has 3 active sessions
    WHEN delete_token() is called
    THEN 2 sessions left

    Args:
        test_client: клиент для выполнения HTTP запросов
        session: сессия базы данных
    """
    user_id = create_user(session=session, admin=True)
    for _ in range(3):
        access_token, refresh_token = login_user(test_client)
    jti = str(decode_token(access_token)["jti"])
    delete_token(user_id=user_id, jti=jti)
    assert count_tokens(user_id=user_id) == 2


def test_delete_all_tokens(test_client, session):
    """
    GIVEN User has 3 active sessions
    WHEN delete_all_tokens() is called
    THEN No sessions left

    Args:
        test_client: клиент для выполнения HTTP запросов
        session: сессия базы данных
    """
    user_id = create_user(session=session, admin=True)
    for _ in range(3):
        login_user(test_client)
    delete_all_tokens(user_id=user_id)
    assert count_tokens(user_id=user_id) == 0
