import click
from db import db

from models import User
from utils import hash_password
from email_validator import validate_email, EmailNotValidError


def email_callback(ctx, param, value):
    try:
        email = validate_email(value).email
    except EmailNotValidError as e:
        raise click.BadParameter(str(e))
    return email


def register_commands(app):
    @app.cli.command("create-superuser")
    @click.option("--email", prompt=True, callback=email_callback)
    @click.password_option()
    def create_superuser(email: str, password: str) -> None:
        """Создать суперпользователя"""

        superuser = User(password=hash_password(password), email=email, is_admin=True)
        db.session.add(superuser)
        db.session.commit()
        click.echo("Superuser created")
