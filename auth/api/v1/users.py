from uuid import uuid4, UUID
from datetime import datetime
from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError

from api.v1.api_models import spectree, AuthSignup
from db import sql
from models import User
from password import hash_password, is_correct_password
from tokens import is_valid_email

users = Blueprint("users", __name__, url_prefix="/users")


@users.route("/signup/", methods=["POST"])
@spectree.validate(json=AuthSignup)
def signup():
    email = is_valid_email(request.json.get("email"))
    password = hash_password(request.json.get("password"))
    user = User.query.filter_by(email=email).first()
    if user:
        return (
            jsonify(message="User already registered"),
            HTTPStatus.BAD_REQUEST,
        )
    id = uuid4()
    user = User(id=id, email=email, password=hash_password(password))
    sql.session.add(user)
    try:
        sql.session.commit()
    except SQLAlchemyError as err:
        return (
            jsonify(message=err),
            HTTPStatus.BAD_REQUEST,
        )

    return jsonify(message="User is created.", id=id, email=email)


@users.route("/change/<uuid:user_id>/", methods=["PATCH"])
@spectree.validate(json=AuthSignup)
@jwt_required()
def change(user_id: UUID):
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
            HTTPStatus.BAD_REQUEST,
        )
    try:
        user.password = hash_password(update_password)
        user.modified = datetime.utcnow()
        sql.session.commit()
    except SQLAlchemyError as err:
        return (
            jsonify(message=err),
            HTTPStatus.BAD_REQUEST,
        )

    return jsonify(message="User password is changed.", id=user_id, email=email)
