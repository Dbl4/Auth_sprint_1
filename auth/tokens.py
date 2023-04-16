from datetime import timedelta
from functools import wraps
from http import HTTPStatus
from uuid import UUID, uuid4

import db
from email_validator import EmailNotValidError, validate_email
from flask import abort, jsonify
from flask_jwt_extended import JWTManager, create_access_token, get_jwt
from flask_jwt_extended import verify_jwt_in_request
from settings import settings


def is_valid_email(email: str) -> str:
    try:
        return validate_email(email).email
    except EmailNotValidError:
        abort(
            HTTPStatus.UNPROCESSABLE_ENTITY,  # 422
            description="Email is not valid.",
        )


def create_tokens(identity: str, additional_claims: dict) -> tuple[str, str]:
    access_token = create_access_token(
        identity=identity,
        additional_claims=additional_claims,
        expires_delta=timedelta(minutes=settings.auth_access_token_minutes),
    )
    refresh_token = uuid4()
    return str(access_token), str(refresh_token)


def put_token(user_id: UUID, jti: UUID, refresh_token: str) -> None:
    """
    Puts refresh token into Redis.

    Args:
        user_id: Идентификатор пользователя
        jti: Идентификатор токена
        refresh_token: refresh-токен
    """
    db.redis.set(
        str(user_id) + ":" + str(jti),
        refresh_token,
        ex=timedelta(minutes=settings.auth_refresh_token_minutes),
    )


def get_token(user_id: UUID, jti: UUID) -> str:
    """
    Gets refresh token for given access token from Redis.

    Args:
        user_id: Идентификатор пользователя
        jti: Идентификатор токена

    Returns:
        refresh-токен
    """
    return db.redis.get(str(user_id) + ":" + str(jti))


def count_tokens(user_id: UUID) -> int:
    """
    Gets number of refresh tokens for given user from Redis.

    Args:
        user_id: Идентификатор пользователя

    Returns:
        Количество refresh-токенов пользователя
    """
    return len(db.redis.keys(pattern=f"{user_id}:*"))


def delete_token(user_id: UUID, jti: str) -> None:
    """
    Delete given refresh token from Redis.

    Args:
        user_id: Идентификатор пользователя
        jti: Идентификатор токена
    """
    db.redis.delete(str(user_id) + ":" + str(jti))


def delete_all_tokens(user_id: UUID) -> None:
    """
    Deletes all refresh tokens for given user from Redis.

    Args:
        user_id: Идентификатор пользователя
    """
    for key in db.redis.scan_iter(f"{user_id}:*"):
        db.redis.delete(key)


def register_tokens(app):
    jwt = JWTManager(app)

    @jwt.unauthorized_loader
    def my_unauthorized_loader(reason):
        """
        Изменяет возвращаемый HTTP код при отсутствии access-токена.
        https://flask-jwt-extended.readthedocs.io/en/stable/changing_default_behavior/

        Args:
            reason: текст сообщения о необходимости авторизации
        """
        return jsonify(message=reason), HTTPStatus.UNAUTHORIZED  # 401


def admin_required():
    """
    Decorator function for endpoints that allow only admins.
    """

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["admin"]:
                return fn(*args, **kwargs)
            return (
                jsonify(
                    message="Действие разрешено только администратору",
                ),
                HTTPStatus.FORBIDDEN,  # 403
            )

        return decorator

    return wrapper
