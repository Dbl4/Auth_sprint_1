from http import HTTPStatus

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt,
    decode_token,
)

import db
from models import User, AuthHistory, Role
from tokens import create_tokens, is_valid_email, put_token, delete_token, get_token, delete_all_tokens
from password import is_correct_password

sessions = Blueprint("sessions", __name__, url_prefix="/sessions")


@sessions.post("/")
def login():
    email = is_valid_email(request.json.get("email"))
    password = request.json.get("password")
    user_agent = request.json.get("user-agent")
    user_ip = request.json.get("user-ip")
    user = User.query.filter_by(email=email).first()
    if not user or not is_correct_password(user.password, password):
        return (
            jsonify(message="Login or password is incorrect"),
            HTTPStatus.FORBIDDEN,
        )
    auth_history = AuthHistory(
        user_id=user.id, user_agent=user_agent, user_ip=user_ip
    )
    db.sql.session.add(auth_history)
    try:
        db.sql.session.commit()
    except SQLAlchemyError as err:
        return (
            jsonify(message=err),
            HTTPStatus.CONFLICT,
        )
    roles = (
        db.sql.session.query(Role).join(User.roles).filter(User.id == user.id).all()
    )
    role_names = [role.name for role in roles]
    additional_claims = {
        "email": email,
        "roles": role_names,
        "admin": user.is_admin,
        "userAgent": user_agent,
        "userIP": user_ip,
    }
    access_token, refresh_token = create_tokens(user.id, additional_claims)
    claims = decode_token(access_token)
    put_token(user.id, claims["jti"], refresh_token)
    return jsonify(access=access_token, refresh=refresh_token)


@sessions.get("/")
@jwt_required()
def check():
    claims = get_jwt()
    return (
        jsonify(
            {
                "email": claims["email"],
                "user-agent": claims["userAgent"],
                "user-ip": claims["userIP"],
                "roles": claims["roles"],
            }
        ),
        HTTPStatus.OK,
    )


@sessions.delete("/")
@jwt_required()
def logout():
    claims = get_jwt()
    delete_token(claims["sub"], claims["jti"])
    return (
        jsonify(message="Successful logout"),
        HTTPStatus.OK,
    )


@sessions.delete("/all/")
@jwt_required()
def logout_all():
    claims = get_jwt()
    delete_all_tokens(claims["sub"])
    return (
        jsonify(message="Successful logout from all devices"),
        HTTPStatus.OK,
    )


@sessions.put("/")
def refresh():
    """
    1. Достать access токен из заголовка
    2. Достать из Redis refresh токен по полям sub и jti из access токена
    3. Сравнить refresh токен из Redis и из тела запроса
    4. Прочитать данные о пользователе из Postgres
    5. Создать новые access и refresh токены
    6. Записать новый refresh токен в Redis
    7. Удалить старый refresh токен из Redis
    8. Вернуть новые access и refresh токены
    """
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(" ")[1]
    claims = decode_token(access_token, allow_expired=True)
    refresh_token_redis = get_token(claims["sub"], claims["jti"])
    refresh_token_json = request.json.get("refresh_token")
    if refresh_token_redis != refresh_token_json:
        return (
            jsonify(message="Refresh токен не найден"),
            HTTPStatus.UNAUTHORIZED,
        )
    user = User.query.get(claims["sub"])
    roles = (
        db.sql.session.query(Role).join(User.roles).filter(User.id == user.id).all()
    )
    role_names = [role.name for role in roles]
    additional_claims = {
        "email": user.email,
        "roles": role_names,
        "admin": user.is_admin,
        "userAgent": claims["userAgent"],
        "userIP": claims["userIP"],
    }
    new_access_token, new_refresh_token = create_tokens(user.id, additional_claims)
    new_claims = decode_token(new_access_token)
    put_token(user.id, new_claims["jti"], new_refresh_token)
    delete_token(access_token)
    return (
        jsonify(access=new_access_token, refresh=new_refresh_token),
        HTTPStatus.OK,
    )
