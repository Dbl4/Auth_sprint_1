from flask import Blueprint, jsonify, abort, request
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import User, Role
from utils import hash_password, create_tokens

roles = Blueprint("roles", __name__, url_prefix="/roles")


@roles.get("/")
def get():
    roles = Role
    return jsonify("get")


@roles.post("/")
def post():
    return jsonify("post")


@roles.put("/<uuid:role_id>/")
def put(role_id):
    return jsonify("put")


@roles.delete("/<uuid:role_id>/")
def delete(role_id):
    return jsonify("delete")
