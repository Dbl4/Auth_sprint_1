from flask import Blueprint

from api.v1.auth import auth
<<<<<<< HEAD
from api.v1.roles import roles
=======
>>>>>>> 2ea87f3 (Добавил signup, change)
from api.v1.users import users

v1 = Blueprint("v1", __name__, url_prefix="/v1")

v1.register_blueprint(auth)
v1.register_blueprint(users)
<<<<<<< HEAD
v1.register_blueprint(roles)
=======
>>>>>>> 2ea87f3 (Добавил signup, change)
