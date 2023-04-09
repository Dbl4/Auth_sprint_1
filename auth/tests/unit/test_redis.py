from tokens import (
    put_token,
    get_token,
    count_tokens,
    delete_token,
    delete_all_tokens,
)
from tests.settings import login_user, create_user


def test_tokens(test_client, session):
    user_id = create_user(session=session, admin=True)
    for _ in range(3):
        access_token, refresh_token = login_user(test_client)
        put_token(
            user_id=user_id,
            access_token=access_token,
            refresh_token=refresh_token,
        )
    assert refresh_token == get_token(user_id, access_token)
    assert 3 == count_tokens(user_id=user_id)
    delete_token(user_id=user_id, access_token=access_token)
    assert 2 == count_tokens(user_id=user_id)
    delete_all_tokens(user_id=user_id)
    assert 0 == count_tokens(user_id=user_id)
