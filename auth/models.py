import uuid
from datetime import datetime

from db import db
from sqlalchemy.dialects.postgresql import UUID


users_roles = db.Table(
    "users_roles",
    db.Column(
        "user_id",
        db.ForeignKey("auth.users.id"),
        primary_key=True,
        nullable=False,
    ),
    db.Column(
        "role_id",
        db.ForeignKey("auth.roles.id"),
        primary_key=True,
        nullable=False,
    ),
    db.Column("created", db.DateTime, default=datetime.utcnow, nullable=False),
    db.UniqueConstraint("user_id", "role_id"),
    schema="auth",
)


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
        secondary=users_roles,
        back_populates="users",
    )

    def __repr__(self):
        return f"<User {self.email}>"


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
        secondary=users_roles,
        back_populates="roles",
    )
    db.UniqueConstraint("name"),

    def __repr__(self):
        return f"<Role {self.name}>"

    def to_json(self):
        return {"id": self.id, "name": self.name}


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
