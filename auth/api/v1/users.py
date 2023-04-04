<<<<<<< HEAD
import uuid
from datetime import datetime
from http import HTTPStatus

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from api.v1.api_models import spectree, AuthSignup
from db import db
from models import User
from utils import hash_password, is_correct_password, is_valid_email

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
    id = uuid.uuid4()
    user = User(id=id, email=email, password=hash_password(password))
    db.session.add(user)
    try:
        db.session.commit()
    except SQLAlchemyError as err:
        return (
            jsonify(message=err),
            HTTPStatus.BAD_REQUEST,
        )

    return jsonify(message="User is created.", id=id, email=email)


@users.route("/change/<uuid:user_id>/", methods=["PATCH"])
@spectree.validate(json=AuthSignup)
def change(user_id):
    # к методу надо прикладывать аксес токен: Bearer a5301be
    # после того как залогинились
    # нужно будет добавить, что изменять данные могут только текущий пользователь и админ
    email = is_valid_email(request.json.get("email"))
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
        db.session.commit()
    except SQLAlchemyError as err:
        return (
            jsonify(message=err),
            HTTPStatus.BAD_REQUEST,
        )

    return jsonify(message="User password is changed.", id=user_id, email=email)
=======
from flask import Blueprint, jsonify, abort, request
from sqlalchemy.exc import SQLAlchemyError

from api.v1.api_forms import spec, SignupForm
from db import db
from models import User
from utils import hash_password, create_tokens

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/signup", methods=["POST"])
@spec.validate(
    json=SignupForm,
)
def signup():
    email = request.json.get("email")
    password = hash_password(request.json.get("password"))
    access_token, refresh_token = create_tokens(identity=email)
    user = User(email=email, password=hash_password(password))
    # надо как-то куда-то сохранять выданный рефреш токен в базу, а аксес летит в редис
    db.session.add(user)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        abort(422, description="User already exists")

    return jsonify(access_token=access_token, refresh_token=refresh_token)
>>>>>>> cd0c6dc (02 tests (#11))
