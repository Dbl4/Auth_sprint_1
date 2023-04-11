from faker import Faker
from settings import settings
from faker import Faker
from models import User
from password import hash_password


def create_user(session, admin=False):
    session.add(
        User(
            password=hash_password(settings.test_user_password),
            email=settings.test_user_email,
            is_admin=admin,
        )
    )
    session.commit()
    user = User.query.filter_by(email=settings.test_user_email).first()
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
    return response.json['access'], response.json['refresh']
