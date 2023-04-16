import uuid
from datetime import datetime

from db import sql
from sqlalchemy.dialects.postgresql import UUID

users_roles = sql.Table(
    "users_roles",
    sql.Column(
        "user_id",
        sql.ForeignKey("auth.users.id"),
        primary_key=True,
        nullable=False,
    ),
    sql.Column(
        "role_id",
        sql.ForeignKey("auth.roles.id"),
        primary_key=True,
        nullable=False,
    ),
    sql.Column(
        "created",
        sql.DateTime,
        default=datetime.utcnow,
        nullable=False,
    ),
    sql.UniqueConstraint("user_id", "role_id"),
    schema="auth",
)


class User(sql.Model):
    __tablename__ = "users"
    __table_args__ = {"schema": "auth"}

    id = sql.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    email = sql.Column(sql.String, unique=True, nullable=False)
    password = sql.Column(sql.String, nullable=False)
    is_admin = sql.Column(sql.Boolean, nullable=False, default=False)
    created = sql.Column(sql.DateTime, default=datetime.utcnow, nullable=False)
    modified = sql.Column(
        sql.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    roles = sql.relationship(
        "Role",
        secondary=users_roles,
        back_populates="users",
    )

    def __repr__(self):
        return f"<User {self.email}>"


class Role(sql.Model):
    __tablename__ = "roles"
    __table_args__ = {"schema": "auth"}

    id = sql.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = sql.Column(sql.String, unique=True, nullable=False)
    created = sql.Column(sql.DateTime, default=datetime.utcnow, nullable=False)
    modified = sql.Column(
        sql.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    users = sql.relationship(
        "User",
        secondary=users_roles,
        back_populates="roles",
    )
    sql.UniqueConstraint("name")

    def __repr__(self):
        return f"<Role {self.name}>"

    def to_json(self):
        return {"id": self.id, "name": self.name}


class AuthHistory(sql.Model):
    __tablename__ = "auth_history"
    __table_args__ = {"schema": "auth"}

    id = sql.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    user_id = sql.Column(
        UUID(as_uuid=True),
        sql.ForeignKey("auth.users.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_agent = sql.Column(sql.String, nullable=False)
    user_ip = sql.Column(sql.String, nullable=False)
    action = sql.Column(sql.String, nullable=True)
    created = sql.Column(sql.DateTime, default=datetime.utcnow, nullable=False)
