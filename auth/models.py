import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
from db import db


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {"schema": "auth"}

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(db.DateTime, default=datetime.utcnow)

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
