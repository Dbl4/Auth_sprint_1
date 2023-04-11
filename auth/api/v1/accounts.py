from uuid import uuid4, UUID
from datetime import datetime
from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from api.v1.api_models import spectree, Signup
from db import sql
from models import User, AuthHistory
from password import hash_password, is_correct_password
from tokens import is_valid_email

accounts = Blueprint("accounts", __name__, url_prefix="/accounts")


@accounts.get("/")
@jwt_required()
def get():
    claims = get_jwt()
    user = User.query.get(claims["sub"])
    auth_history = AuthHistory.query.filter_by(user_id=user.id).order_by(AuthHistory.created.desc()).all()
    return jsonify(
        email=claims["email"],
        sessions=len(auth_history),
        history=[{'date': row.created, 'action': '' if row.action is None else row.action} for row in auth_history]
    )


@accounts.post("/")
@spectree.validate(json=Signup)
def signup():
    email = is_valid_email(request.json.get("email"))
    password = hash_password(request.json.get("password"))
    user = User.query.filter_by(email=email).first()
    if user:
        return (
            jsonify(message="User already registered"),
            HTTPStatus.CONFLICT,
        )
    id = uuid4()
    user = User(id=id, email=email, password=password)
    sql.session.add(user)
    try:
        sql.session.commit()
    except SQLAlchemyError as err:
        return (
            jsonify(message=err),
            HTTPStatus.CONFLICT,
        )

    return jsonify(message="User is created.", id=id, email=email)


@accounts.patch("/")
@spectree.validate(json=Signup)
@jwt_required()
def change(user_id: UUID):
    # После изменения email пользователя надо обновлять токен, потому что email записан в payload
    email = is_valid_email(request.json("email"))
    update_password = request.json.get("password")
    user = User.query.get(user_id)
    if not user:
        return (
            jsonify(message="User does not exists"),
            HTTPStatus.NOT_FOUND,
        )
    if is_correct_password(user.password, update_password):
        return (
            jsonify(message="Passwords match"),
            HTTPStatus.CONFLICT,
        )
    try:
        user.password = hash_password(update_password)
        user.modified = datetime.utcnow()
        sql.session.commit()
    except SQLAlchemyError as err:
        return (
            jsonify(message=err),
            HTTPStatus.CONFLICT,
        )

    return jsonify(message="User password is changed.", id=user_id, email=email)
