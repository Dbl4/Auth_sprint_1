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
