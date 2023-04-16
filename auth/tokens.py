from flask import jsonify, abort
from flask_jwt_extended import (
    JWTManager,
    verify_jwt_in_request,
    get_jwt,
    create_access_token,
)
from functools import wraps
from uuid import uuid4, UUID
from datetime import timedelta
from email_validator import validate_email, EmailNotValidError
import db
from settings import settings
from http import HTTPStatus


def is_valid_email(email: str) -> str:
    try:
        return validate_email(email).email
    except EmailNotValidError as err:
        abort(
            HTTPStatus.UNPROCESSABLE_ENTITY, # 422
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
    """
    db.redis.set(
        str(user_id) + ":" + str(jti),
        refresh_token,
        ex=timedelta(minutes=settings.auth_refresh_token_minutes),
    )


def get_token(user_id: UUID, jti: UUID) -> str:
    """
    Gets refresh token for given access token from Redis.
    """
    return db.redis.get(str(user_id) + ":" + str(jti))


def count_tokens(user_id: UUID) -> int:
    """
    Gets number of refresh tokens for given user from Redis.
    """
    count = 0
    for key in db.redis.scan_iter(f"{user_id}:*"):
        count += 1
    return count


def delete_token(user_id: UUID, jti: str) -> None:
    """
    Delete given refresh token from Redis.
    """
    db.redis.delete(
        str(user_id) + ":" + str(jti)
    )


def delete_all_tokens(user_id: UUID) -> None:
    """
    Deletes all refresh tokens for given user from Redis.
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
            if claims["admin"] == True:
                return fn(*args, **kwargs)
            else:
                return (
                    jsonify(message="Действие разрешено только администратору"),
                    HTTPStatus.FORBIDDEN, # 403
                )

        return decorator

    return wrapper
