from pydantic import BaseSettings, Field
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    auth_postgres_user: str = Field("app", env="AUTH_POSTGRES_USER")
    auth_postgres_password: str = Field("123qwe", env="AUTH_POSTGRES_PASSWORD")
    auth_postgres_host: str = Field("0.0.0.0", env="AUTH_POSTGRES_HOST")
    auth_postgres_port: int = Field(5433, env="AUTH_POSTGRES_PORT")
    auth_postgres_db: str = Field("auth", env="AUTH_POSTGRES_DB")
    jwt_secret_key: str = Field("super-secret", env="JWT_SECRET_KEY")


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")

config = {}

auth_postgres_url = URL.create(
    drivername="postgresql",
    username=settings.auth_postgres_user,
    password=settings.auth_postgres_password,
    host=settings.auth_postgres_host,
    port=settings.auth_postgres_port,
    database=settings.auth_postgres_db
)
