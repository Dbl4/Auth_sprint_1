from flask import Blueprint, jsonify, abort, request

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/login/", methods=["POST"])
def signup():
    return jsonify(message="User is authorized.")
