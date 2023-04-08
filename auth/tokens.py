from flask import jsonify
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt
from functools import wraps


def register_tokens(app):
    jwt = JWTManager(app)

    @jwt.unauthorized_loader
    def my_unauthorized_loader(reason):
        return jsonify(message=reason), 401


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["admin"]:
                return fn(*args, **kwargs)
            else:
                return jsonify(message="Admins only!"), 403

        return decorator

    return wrapper
