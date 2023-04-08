import click
from db import db

from models import User
from password import hash_password
from email_validator import validate_email, EmailNotValidError


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

        admin = User(password=hash_password(password), email=email, is_admin=True)
        db.session.add(admin)
        db.session.commit()
        click.echo("Admin created")
