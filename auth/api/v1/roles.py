from http import HTTPStatus
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from api.v1.api_models import spectree, RolesPost

from db import sql
from models import Role
from tokens import admin_required

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
    sql.session.delete(role)
    sql.session.commit()
    return "Роль удалена", HTTPStatus.NO_CONTENT
