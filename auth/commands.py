import click
from db import db
from flask.cli import with_appcontext

from models import User


@click.command()
@click.argument("email")
@click.argument("password")
@with_appcontext
def create_superuser(email: str, password: str) -> None:
    """Создать суперпользователя"""

    # пароль потом нужно хешировать конечно
    superuser = User(password=password, email=email, is_admin=True)
    db.session.add(superuser)
    db.session.commit()
    click.echo("Superuser created")


if __name__ == "__main__":
    create_superuser()
