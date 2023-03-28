import click
from db import db
from flask.cli import with_appcontext

from models import User
from utils import hash_password


@click.command()
@click.argument("email")
@click.argument("password")
@with_appcontext
def create_superuser(email: str, password: str) -> None:
    """Создать суперпользователя"""

    superuser = User(password=hash_password(password), email=email, is_admin=True)
    db.session.add(superuser)
    db.session.commit()
    click.echo("Superuser created")


if __name__ == "__main__":
    create_superuser()
