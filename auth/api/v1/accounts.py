from datetime import datetime
from http import HTTPStatus

from api.v1.api_models import Signup, spectree
from db import sql
from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required
from password import hash_password, is_correct_password
from sqlalchemy.exc import SQLAlchemyError
from tokens import count_tokens, delete_all_tokens, is_valid_email

from models import AuthHistory, User

accounts = Blueprint("accounts", __name__, url_prefix="/accounts")


@accounts.get("/")
@jwt_required()
def get() -> Response:
    claims = get_jwt()
    user = User.query.get(claims["sub"])
    auth_history = (
        AuthHistory.query.filter_by(user_id=user.id)
        .order_by(AuthHistory.created.desc())
        .all()
    )
    return jsonify(
        email=claims["email"],
        sessions=count_tokens(user),
        history=[
            {
                "date": row.created,
                "action": "" if row.action is None else row.action,
            }
            for row in auth_history
        ],
    )


@accounts.post("/")
@spectree.validate(json=Signup)
def signup() -> Response:
    email = is_valid_email(request.json.get("email"))
    password = hash_password(request.json.get("password"))
    user = User.query.filter_by(email=email).first()
    if user:
        return (
            jsonify(message="Пользователь с этим e-mail уже зарегистрирован"),
            HTTPStatus.CONFLICT,
        )
    user = User(email=email, password=password)
    sql.session.add(user)
    try:
        sql.session.commit()
        auth_history = AuthHistory(
            user_id=user.id,
            user_agent="",
            user_ip="",
            action="signup",
        )
        sql.session.add(auth_history)
        sql.session.commit()
    except SQLAlchemyError as err:
        return (
            jsonify(message=err),
            HTTPStatus.CONFLICT,
        )
    return jsonify(
        message="Успешная регистрация",
        id=user.id,
        email=user.email,
    )


@accounts.patch("/")
@jwt_required()
def change() -> Response:
    claims = get_jwt()
    update_email = request.json.get("email")
    update_password = request.json.get("password")
    user = User.query.get(claims["sub"])
    has_changes = False
    if update_email and user.email != update_email:
        user.email = is_valid_email(update_email)
        has_changes = True
    if update_password and not is_correct_password(
        user.password,
        update_password,
    ):
        user.password = hash_password(update_password)
        has_changes = True
    if not has_changes:
        return (
            jsonify(message="Данные не были изменены"),
            HTTPStatus.CONFLICT,
        )
    user.modified = datetime.utcnow()
    sql.session.add(user)
    auth_history = AuthHistory(
        user_id=user.id,
        user_agent=claims["userAgent"],
        user_ip=claims["userIP"],
        action="change-profile",
    )
    sql.session.add(auth_history)
    try:
        sql.session.commit()
    except SQLAlchemyError as err:
        return (
            jsonify(message=err),
            HTTPStatus.CONFLICT,
        )
    else:
        return jsonify(
            message="Успешное обновление данных",
            id=user.id,
            email=user.email,
        )


@accounts.delete("/")
@jwt_required()
def delete() -> Response:
    claims = get_jwt()
    user = User.query.get(claims["sub"])
    delete_all_tokens(user)
    try:
        sql.session.delete(user)
        sql.session.commit()
    except SQLAlchemyError as e:
        return jsonify(message=e), HTTPStatus.CONFLICT
    else:
        return (
            jsonify(message="Аккаунт пользователя успешно удален"),
            HTTPStatus.OK,
        )
