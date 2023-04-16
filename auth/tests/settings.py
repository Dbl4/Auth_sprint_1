from faker import Faker
from password import hash_password
from settings import settings

from models import User


def create_user(
    session,
    admin=False,
    password=settings.test_user_password,
    email=settings.test_user_email,
):
    session.add(
        User(
            password=hash_password(password),
            email=email,
            is_admin=admin,
        ),
    )
    session.commit()
    user = User.query.filter_by(email=email).first()
    return user.id


def login_user(test_client):
    faker = Faker()
    response = test_client.post(
        "/v1/sessions/",
        json={
            "email": settings.test_user_email,
            "password": settings.test_user_password,
            "user-agent": faker.user_agent(),
            "user-ip": faker.ipv4(),
        },
    )
    return response.json["access"], response.json["refresh"]
