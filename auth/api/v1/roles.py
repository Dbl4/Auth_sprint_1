from flask import Blueprint, jsonify, abort, request
<<<<<<< HEAD
from sqlalchemy.exc import SQLAlchemyError
=======
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
>>>>>>> cd0c6dc (02 tests (#11))

from db import db
from models import User, Role
from utils import hash_password, create_tokens

roles = Blueprint("roles", __name__, url_prefix="/roles")


@roles.get("/")
def get():
<<<<<<< HEAD
    roles = Role
    return jsonify("get")
=======
    roles = []
    for role in Role.query.all():
        roles.append(role.to_json())
    return jsonify(roles)
>>>>>>> cd0c6dc (02 tests (#11))


@roles.post("/")
def post():
<<<<<<< HEAD
    return jsonify("post")
=======
    name = request.json.get("name")
    role = Role(name=name)
    db.session.add(role)
    try:
        db.session.commit()
    except IntegrityError:
        abort(409, description="Role already exists")
    return jsonify(name=name)
>>>>>>> cd0c6dc (02 tests (#11))


@roles.put("/<uuid:role_id>/")
def put(role_id):
    return jsonify("put")


@roles.delete("/<uuid:role_id>/")
def delete(role_id):
    return jsonify("delete")
