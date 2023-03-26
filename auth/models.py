import uuid
from datetime import datetime

from db import db
from sqlalchemy.dialects.postgresql import UUID


class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {"schema": "auth"}

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    modified = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    roles = db.relationship(
        "Role",
        secondary="auth.users_roles",
        back_populates="users",
    )

    def __repr__(self):
        return f"<User {self.login}>"


class Role(db.Model):
    __tablename__ = "roles"
    __table_args__ = {"schema": "auth"}

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = db.Column(db.String, unique=True, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    modified = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    users = db.relationship(
        "User",
        secondary="auth.users_roles",
        back_populates="roles",
    )

    def __repr__(self):
        return f"<User {self.login}>"


class AuthHistory(db.Model):
    __tablename__ = "auth_history"
    __table_args__ = {"schema": "auth"}

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("auth.users.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_agent = db.Column(db.String, nullable=False)
    user_ip = db.Column(db.String, nullable=False)
    action = db.Column(db.String, nullable=True)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class RefreshToken(db.Model):
    __tablename__ = "refresh_tokens"
    __table_args__ = {"schema": "auth"}

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("auth.users.id", ondelete="CASCADE"),
        nullable=False,
    )
    expires_at = db.Column(db.DateTime, nullable=False)
    user_agent = db.Column(db.String, nullable=False)
    user_ip = db.Column(db.String, nullable=False)


users_roles = db.Table(
    "users_roles",
    db.Column(
        "user_id",
        db.ForeignKey(User.id),
        primary_key=True,
        nullable=False,
    ),
    db.Column(
        "role_id",
        db.ForeignKey(Role.id),
        primary_key=True,
        nullable=False,
    ),
    db.Column("created", db.DateTime, default=datetime.utcnow, nullable=False),
    db.UniqueConstraint("user_id", "role_id"),
    schema="auth",
)
