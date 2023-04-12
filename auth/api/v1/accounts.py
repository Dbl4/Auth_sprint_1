import uuid
from datetime import datetime
from http import HTTPStatus

from flask import Blueprint, jsonify, request, Response
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from api.v1.api_models import spectree, Signup
from db import sql
from models import User, AuthHistory
from password import hash_password, is_correct_password
from tokens import is_valid_email, count_tokens, delete_all_tokens

accounts = Blueprint("accounts", __name__, url_prefix="/accounts")


@accounts.get("/")
@jwt_required()
def get() -> Response:
    claims = get_jwt()
    user = User.query.get(claims["sub"])
    auth_history = AuthHistory.query.filter_by(user_id=user.id).order_by(AuthHistory.created.desc()).all()
    return jsonify(
        email=claims["email"],
        sessions=count_tokens(user),
        history=[{'date': row.created, 'action': '' if row.action is None else row.action} for row in auth_history]
    )


@accounts.post("/")
@spectree.validate(json=Signup)
def signup() -> Response:
    email = is_valid_email(request.json.get("email"))
    password = hash_password(request.json.get("password"))
    user = User.query.filter_by(email=email).first()
    if user:
        return (
            jsonify(message="User already registered"),
            HTTPStatus.CONFLICT,
        )
    user = User(id=uuid.uuid4(), email=email, password=password)
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
    return jsonify(message="User is created.", id=user.id, email=user.email)


@accounts.patch("/")
@jwt_required()
def change() -> Response:
    claim = get_jwt()
    user_id = claim["sub"]
    update_email = request.json.get("email")
    update_password = request.json.get("password")
    user = User.query.get(user_id)
    if update_email:
        user.email = is_valid_email(update_email)
    if update_password:
        user.password = hash_password(update_password)
    user.modified = datetime.utcnow()
    sql.session.add(user)
    auth_history = AuthHistory(
        user_id=user.id,
        user_agent="",
        user_ip="",
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
        if update_email:
            delete_all_tokens(user_id)
        return jsonify(
            message="User email/password is changed.",
            id=user.id,
            email=user.email
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
        return jsonify(message='Пользователь удален'), HTTPStatus.OK
