from http import HTTPStatus
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from api.v1.api_models import spectree, RolesPost

from db import db
from models import Role

roles = Blueprint("roles", __name__, url_prefix="/roles")


@roles.get("/")
def get():
    roles = []
    for role in Role.query.all():
        roles.append(role.to_json())
    return jsonify(roles)


@roles.post("/")
@spectree.validate(json=RolesPost)
def post():
    role = Role(name=request.json.get("name"))
    db.session.add(role)
    try:
        db.session.commit()
    except IntegrityError:
        return "Роль уже существует", HTTPStatus.CONFLICT
    return jsonify(role.to_json())


@roles.put("/<uuid:role_id>/")
@spectree.validate(json=RolesPost)
def put(role_id):
    role = db.session.get(Role, role_id)
    if not role:
        return "Роль не найдена", HTTPStatus.NOT_FOUND
    role.name = request.json.get("name")
    try:
        db.session.commit()
    except IntegrityError:
        return "Роль уже существует", HTTPStatus.CONFLICT
    return "Роль переименована", HTTPStatus.NO_CONTENT


@roles.delete("/<uuid:role_id>/")
def delete(role_id):
    role = db.session.get(Role, role_id)
    if not role:
        return "Роль не найдена", HTTPStatus.NOT_FOUND
    db.session.delete(role)
    db.session.commit()
    return "Роль удалена", HTTPStatus.NO_CONTENT
