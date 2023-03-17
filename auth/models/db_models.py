import enum
import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
from db import db


class DefaultRoleEnum(enum.Enum):
    superuser = "superuser"
    admin = "admin"
    guest = "guest"
    subscriber = "subscriber"


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {"schema": "auth"}

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.Enum(DefaultRoleEnum), default=DefaultRoleEnum.guest, nullable=False)

    def __repr__(self):
        return f'<User {self.login}>'


class AuthHistory(db.Model):
    __tablename__ = 'auth_history'
    __table_args__ = {"schema": "auth"}

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,  nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('auth.users.id', ondelete="CASCADE"), nullable=False)
    user_agent = db.Column(db.String, nullable=False)
    action = db.Column(db.String, nullable=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
