from http import HTTPStatus

from flask_sqlalchemy.session import Session
from werkzeug.test import Client

from settings import settings
from tests.settings import login_user, create_user


def test_get(test_client: Client, session: Session) -> None:
    create_user(session=session)
    access_token, _ = login_user(test_client)
    response = test_client.get(
        "/v1/accounts/",
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json["email"] == settings.test_user_email
    history_len = len(response.json["history"])
    assert history_len > 0

    another_access_token, _ = login_user(test_client)
    response = test_client.get(
        "/v1/accounts/",
        headers={"Authorization": "Bearer {}".format(another_access_token)},
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json["history"]) == history_len + 1


def test_delete(test_client: Client, session: Session) -> None:
    create_user(session=session)
    access_token, _ = login_user(test_client)
    response = test_client.delete(
        "/v1/accounts/",
        headers={"Authorization": "Bearer {}".format(access_token)},
    )
    assert response.status_code == HTTPStatus.OK
    try:
        login_user(test_client)
    except KeyError:
        assert True
    else:
        assert False
    