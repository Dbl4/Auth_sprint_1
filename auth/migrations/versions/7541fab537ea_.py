"""empty message

Revision ID: 7541fab537ea
Revises: 
Create Date: 2023-04-03 00:08:35.149258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7541fab537ea"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("create schema auth")
    op.create_table(
        "roles",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("name"),
        schema="auth",
    )
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("id"),
        schema="auth",
    )
    op.create_table(
        "auth_history",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("user_agent", sa.String(), nullable=False),
        sa.Column("user_ip", sa.String(), nullable=False),
        sa.Column("action", sa.String(), nullable=True),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["auth.users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        schema="auth",
    )
    op.create_table(
        "users_roles",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("role_id", sa.UUID(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["auth.roles.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["auth.users.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "role_id"),
        sa.UniqueConstraint("user_id", "role_id"),
        schema="auth",
    )


def downgrade():
    op.drop_table("users_roles", schema="auth")
    op.drop_table("auth_history", schema="auth")
    op.drop_table("users", schema="auth")
    op.drop_table("roles", schema="auth")
    op.execute("drop schema auth")
