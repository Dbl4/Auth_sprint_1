from flask import Blueprint

from api.v1.accounts import accounts
from api.v1.sessions import sessions
from api.v1.roles import roles
from api.v1.users import users

v1 = Blueprint("v1", __name__, url_prefix="/v1")

v1.register_blueprint(sessions)
v1.register_blueprint(users)
v1.register_blueprint(roles)
v1.register_blueprint(accounts)
