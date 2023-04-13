from uuid import UUID
from datetime import datetime
from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

import db
from api.v1.api_models import spectree, Signup, RolesPost
from db import sql
from models import User, AuthHistory, Role
from password import hash_password, is_correct_password
from tokens import is_valid_email, admin_required, count_tokens, delete_all_tokens

users = Blueprint("users", __name__, url_prefix="/users")


@users.get("/")
@admin_required()
def get_users():
    users = []
    for user in User.query.all():
        user_data = {
            "user_id": user.ud,
            "email": user.email,
            "created": user.created,
            "modified": user.modified,
        }
        users.append(user_data.to_json())
    return jsonify(users)


@users.get("/<uuid:user_id>/")
@admin_required()
def get_user_detail(user_id: UUID):
    user = User.query.get(user_id)
    if not user:
        return (
            jsonify(message="User does not exists"),
            HTTPStatus.NOT_FOUND,
        )
    auth_history = AuthHistory.query.filter_by(user_id=user.id).order_by(AuthHistory.created.desc()).all()
    return jsonify(
        email=user.email,
        sessions=count_tokens(user),
        history=[{'date': row.created, 'action': '' if row.action is None else row.action} for row in auth_history],
        roles=[{"id": role.id, "name": role.name} for role in user.roles]
    )


@users.patch("/<uuid:user_id>/")
@admin_required()
@spectree.validate(json=Signup)
def change(user_id: UUID):
    claims = get_jwt()
    update_email = request.json.get("email")
    update_password = request.json.get("password")
    user = User.query.get(user_id)
    if not user:
        return (
            jsonify(message="User does not exists"),
            HTTPStatus.NOT_FOUND,
        )

    if update_email and user.email == update_email:
        return (
            jsonify(message="Emails match"),
            HTTPStatus.BAD_REQUEST,
        )
    else:
        user.email = is_valid_email(update_email)

    if update_password and is_correct_password(user.password, update_password):
        return (
            jsonify(message="Passwords match"),
            HTTPStatus.BAD_REQUEST,
        )
    else:
        user.password = hash_password(update_password)

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

    return jsonify(message="User email/password is changed.", id=user_id, email=update_email)


@users.delete("/<uuid:user_id>/")
@admin_required()
def delete_user(user_id: UUID):
    user = User.query.get(user_id)
    if not user:
        return (
            jsonify(message="User does not exists"),
            HTTPStatus.NOT_FOUND,
        )
    delete_all_tokens(user)
    try:
        sql.session.delete(user)
        sql.session.commit()
    except SQLAlchemyError as e:
        return jsonify(message=e), HTTPStatus.CONFLICT

    return jsonify(message="User deleted"), HTTPStatus.OK


@users.get("/<uuid:user_id>/roles")
@admin_required()
def get_user_roles(user_id: UUID):
    user = User.query.get(user_id)
    if not user:
        return (
            jsonify(message="User does not exists"),
            HTTPStatus.NOT_FOUND,
        )
    roles = [{"id": role.id, "name": role.name} for role in user.roles]

    return jsonify(roles=roles), HTTPStatus.OK


@users.get("/<uuid:user_id>/roles")
@admin_required()
def get_user_roles(user_id: UUID):
    user = User.query.get(user_id)
    if not user:
        return (
            jsonify(message="User does not exists"),
            HTTPStatus.NOT_FOUND,
        )
    roles = [{"id": role.id, "name": role.name} for role in user.roles]

    return jsonify(roles=roles), HTTPStatus.OK


@users.put("/<uuid:user_id>/roles")
@admin_required()
@spectree.validate(json=RolesPost)
def put_user_roles(user_id: UUID):
    # доделать
    # если в RolesPost добавлю id ничего не сломается?
    assignment_role = request.json.get("name")
    user = User.query.get(user_id)
    role = Role.query.get(assignment_role)

    if not role:
        return "Роль не найдена", HTTPStatus.NOT_FOUND

    if not user:
        return (
            jsonify(message="User does not exists"),
            HTTPStatus.NOT_FOUND,
        )

    return jsonify(id=role.id, name=role.name), HTTPStatus.OK
