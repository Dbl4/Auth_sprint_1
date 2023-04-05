from flask import Blueprint, jsonify, abort, request
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import User, Role
from utils import hash_password, create_tokens

roles = Blueprint("roles", __name__, url_prefix="/roles")


@roles.get("/")
def get():
    roles = []
    for role in Role.query.all():
        roles.append(role.to_json())
    return jsonify(roles)


@roles.post("/")
def post():
    name = request.json.get("name")
    role = Role(name=name)
    db.session.add(role)
    try:
        db.session.commit()
    except IntegrityError:
        abort(409, description="Role already exists")
    return jsonify(name=name)


@roles.put("/<uuid:role_id>/")
def put(role_id):
    return jsonify("put")


@roles.delete("/<uuid:role_id>/")
def delete(role_id):
    return jsonify("delete")
