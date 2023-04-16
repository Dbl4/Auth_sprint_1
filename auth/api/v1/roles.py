from http import HTTPStatus

from api.v1.api_models import RolesPost, spectree
from db import sql
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from tokens import admin_required

from models import Role, User

roles = Blueprint("roles", __name__, url_prefix="/roles")


@roles.get("/")
@admin_required()
def get():
    roles = []
    for role in Role.query.all():
        roles.append(role.to_json())
    return jsonify(roles)


@roles.post("/")
@admin_required()
@spectree.validate(json=RolesPost)
def post():
    role = Role(name=request.json.get("name"))
    sql.session.add(role)
    try:
        sql.session.commit()
    except IntegrityError:
        return "Роль уже существует", HTTPStatus.CONFLICT
    return jsonify(role.to_json())


@roles.put("/<uuid:role_id>/")
@admin_required()
@spectree.validate(json=RolesPost)
def put(role_id):
    role = sql.session.get(Role, role_id)
    if not role:
        return "Роль не найдена", HTTPStatus.NOT_FOUND
    role.name = request.json.get("name")
    try:
        sql.session.commit()
    except IntegrityError:
        return "Роль уже существует", HTTPStatus.CONFLICT
    return "Роль переименована", HTTPStatus.NO_CONTENT


@roles.delete("/<uuid:role_id>/")
@admin_required()
def delete(role_id):
    role = sql.session.get(Role, role_id)
    if not role:
        return "Роль не найдена", HTTPStatus.NOT_FOUND
    for user in User.query.all():
        if role in user.roles:
            user.roles.remove(role)
    sql.session.delete(role)
    sql.session.commit()
    return "Роль удалена", HTTPStatus.NO_CONTENT
