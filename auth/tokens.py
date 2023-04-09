from flask import jsonify, abort
from flask_jwt_extended import (
    JWTManager,
    verify_jwt_in_request,
    get_jwt,
    create_access_token,
    decode_token,
)
from functools import wraps
from uuid import uuid4, UUID
from datetime import timedelta
from email_validator import validate_email, EmailNotValidError


def is_valid_email(email: str) -> str:
    try:
        return validate_email(email).email
    except EmailNotValidError as err:
        abort(422, description="Email is not valid.")



def create_tokens(identity: str, additional_claims: dict) -> tuple[str, str]:
    access_token = create_access_token(
        identity=identity,
        additional_claims=additional_claims,
        expires_delta=timedelta(minutes=5),
    )
    refresh_token = uuid4()
    return str(access_token), str(refresh_token)


def put_rftoken_db(user_id: UUID, access_token: str, refresh_token: str) -> None:
    decoded_token = decode_token(access_token)
    jti = decoded_token["jti"]
    rftoken_to_redis = f"{user_id}:{jti} {refresh_token}"
    ## save redis rftoken_to_redis


def is_correct_token():
    # в базе будут храниться токены, будем проверять,
    # есть ли приходящий рефреш токен в базе.
    pass


def register_tokens(app):
    jwt = JWTManager(app)

    @jwt.unauthorized_loader
    def my_unauthorized_loader(reason):
        """
        Изменяет возвращаемый HTTP код при отсутствии access-токена.
        https://flask-jwt-extended.readthedocs.io/en/stable/changing_default_behavior/
        """
        return jsonify(message=reason), 401


def admin_required():
    """
    Decorator function for endpoints that allow only admins.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            print(claims)
            if claims["admin"] == True:
                return fn(*args, **kwargs)
            else:
                return jsonify(message="Действие разрешено только администратору"), 403

        return decorator

    return wrapper
