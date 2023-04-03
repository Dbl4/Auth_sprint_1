from flask import Blueprint

from api.v1.auth import auth
from api.v1.users import users

v1 = Blueprint("v1", __name__, url_prefix="/v1")

v1.register_blueprint(auth)
v1.register_blueprint(users)
