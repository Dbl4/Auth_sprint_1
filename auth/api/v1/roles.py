from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from api.v1.api_forms import spec, RolesPost

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
@spec.validate(json=RolesPost)
def post():
    try:
        name = request.json.get("name")
        role = Role(name=name)
        db.session.add(role)
        try:
            db.session.commit()
        except IntegrityError:
            return "Роль уже существует", 409
        return jsonify(role.to_json())
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@roles.put("/<uuid:role_id>/")
@spec.validate(json=RolesPost)
def put(role_id):
    role = db.session.get(Role, role_id)
    if not role:
        return "Роль не найдена", 404
    role.name = request.json.get("name")
    try:
        db.session.commit()
    except IntegrityError:
        return "Роль уже существует", 409
    return "Роль переименована", 204


@roles.delete("/<uuid:role_id>/")
def delete(role_id):
    role = db.session.get(Role, role_id)
    if not role:
        return "Роль не найдена", 404
    db.session.delete(role)
    db.session.commit()
    return "Роль удалена", 204
