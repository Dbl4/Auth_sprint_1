from http import HTTPStatus

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import User, AuthHistory, Role
from utils import create_tokens, is_valid_email, is_correct_password

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/login/", methods=["POST"])
def login():
    email = is_valid_email(request.json.get("email"))
    password = request.json.get("password")
    user_agent = request.json.get("user-agent")
    user_ip = request.json.get("user-ip")
    user = User.query.filter_by(email=email).first()
    if user and is_correct_password(user.password, password):
        auth_history = AuthHistory(user_id=user.id, user_agent=user_agent, user_ip=user_ip)
        db.session.add(auth_history)
        try:
            db.session.commit()
        except SQLAlchemyError as err:
            return (
                jsonify(message=err),
                HTTPStatus.BAD_REQUEST,
            )
        roles = db.session.query(Role).join(User.roles).filter(User.id == user.id).all()
        role_names = [role.name for role in roles]
        additional_claims = {
            "email": email,
            "roles": role_names,
            "admin": user.is_admin,
            "userAgent": user_agent,
            "userIP": user_ip
        }
        access_token, refresh_token = create_tokens(user.id, additional_claims)
        return jsonify(access_token=access_token, refresh_token=refresh_token)
    else:
        return (
            jsonify(message="Login or password is incorrect"),
            HTTPStatus.BAD_REQUEST,
        )
