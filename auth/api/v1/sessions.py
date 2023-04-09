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
from tokens import create_tokens, is_valid_email, put_token
from password import is_correct_password

sessions = Blueprint("sessions", __name__, url_prefix="/sessions")


@sessions.post("/")
def login():
    email = is_valid_email(request.json.get("email"))
    password = request.json.get("password")
    user_agent = request.json.get("user-agent")
    user_ip = request.json.get("user-ip")
    user = User.query.filter_by(email=email).first()
    if user and is_correct_password(user.password, password):
        auth_history = AuthHistory(
            user_id=user.id, user_agent=user_agent, user_ip=user_ip
        )
        db.sql.session.add(auth_history)
        try:
            db.sql.session.commit()
        except SQLAlchemyError as err:
            return (
                jsonify(message=err),
                HTTPStatus.BAD_REQUEST,
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
        put_token(user.id, access_token, refresh_token)
        return jsonify(access_token=access_token, refresh_token=refresh_token)
    else:
        return (
            jsonify(message="Login or password is incorrect"),
            HTTPStatus.BAD_REQUEST,
        )


@sessions.get("/")
@jwt_required()
def check():
    user = User.query.get(get_jwt_identity())
    claims = get_jwt()
    return (
        jsonify(
            {
                "email": user.email,
                "user-agent": claims["userAgent"],
                "user-ip": claims["userIP"],
                "roles": claims["roles"],
            }
        ),
        200,
    )
