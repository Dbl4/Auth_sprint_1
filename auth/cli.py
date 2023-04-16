import click
from db import sql
from email_validator import EmailNotValidError, validate_email
from password import hash_password

from models import User


def email_callback(ctx, param, value):
    try:
        email = validate_email(value).email
    except EmailNotValidError as e:
        raise click.BadParameter(str(e))
    return email


def register_cli(app):
    @app.cli.command("create-admin")
    @click.option("--email", prompt=True, callback=email_callback)
    @click.password_option()
    def create_admin(email: str, password: str) -> None:
        """Создать администратора пользователей"""

        admin = User(
            password=hash_password(password),
            email=email,
            is_admin=True,
        )
        sql.session.add(admin)
        sql.session.commit()
        click.echo("Admin created")
