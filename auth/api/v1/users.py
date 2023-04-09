from uuid import UUID
from datetime import datetime
from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError

from api.v1.api_models import spectree, Signup
from db import sql
from models import User
from password import hash_password, is_correct_password
from tokens import is_valid_email

users = Blueprint("users", __name__, url_prefix="/users")


@users.patch("/<uuid:user_id>/")
@spectree.validate(json=Signup)
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
