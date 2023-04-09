from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis

sql = SQLAlchemy()
migrate = Migrate()
redis: StrictRedis
