import uuid
from datetime import datetime
from http import HTTPStatus

from flask import Blueprint, jsonify, abort, request
from sqlalchemy.exc import SQLAlchemyError

from api.v1.api_forms import spec, SignupForm
from db import db
from models import User
from utils import hash_password, is_correct_password

users = Blueprint("users", __name__, url_prefix="/users")


@users.route("/signup/", methods=["POST"])
@spec.validate(
    json=SignupForm,
)
def signup():
    email = request.json.get("email")
    password = hash_password(request.json.get("password"))
    id = uuid.uuid4()
    user = User(id=id, email=email, password=hash_password(password))
    db.session.add(user)
    try:
        db.session.commit()
    except SQLAlchemyError as err:
        abort(422, description="User already exists")

    return jsonify(message="User is created.", id=id, email=email)


@users.route("/change/<uuid:user_id>/", methods=["PATCH"])
@spec.validate(
    json=SignupForm,
)
def change(user_id: uuid):
    # к методу надо прикладывать аксес токен: Bearer a5301be
    # после того как залогинились
    # нужно будет добавить, что изменять данные могут только текущий пользователь и админ
    email = request.json.get("email")
    update_password = request.json.get("password")
    user = User.query.get(user_id)
    if is_correct_password(user.password, update_password):
        abort(HTTPStatus.BAD_REQUEST, description="Passwords match")
    try:
        user.password = hash_password(update_password)
        user.modified = datetime.utcnow()
        db.session.commit()
    except SQLAlchemyError as err:
        abort(422, description=err)

    return jsonify(message="User password is changed.", id=user_id, email=email)
