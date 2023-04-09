from pydantic import BaseSettings, Field
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    auth_postgres_user: str = Field("app", env="AUTH_POSTGRES_USER")
    auth_postgres_password: str = Field(..., env="AUTH_POSTGRES_PASSWORD")
    auth_postgres_host: str = Field("0.0.0.0", env="AUTH_POSTGRES_HOST")
    auth_postgres_port: int = Field(5433, env="AUTH_POSTGRES_PORT")
    auth_postgres_port_test: int = Field(5434, env="AUTH_POSTGRES_PORT_TEST")
    auth_postgres_db: str = Field("auth", env="AUTH_POSTGRES_DB")
    jwt_secret_key: str = Field(..., env="JWT_SECRET_KEY")
    test_user_email: str = Field(..., env="TEST_USER_EMAIL")
    test_user_password: str = Field(..., env="TEST_USER_PASSWORD")
    auth_redis_host: str = Field(..., env="AUTH_REDIS_HOST")
    auth_redis_port: int = Field(6379, env="AUTH_REDIS_PORT")
    auth_access_token_minutes: int = Field(5, env="AUTH_ACCESS_TOKEN_MINUTES")
    auth_refresh_token_minutes: int = Field(14400, env="AUTH_REFRESH_TOKEN_MINUTES")


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")

config = {
    "SQLALCHEMY_DATABASE_URI": URL.create(
        drivername="postgresql",
        username=settings.auth_postgres_user,
        password=settings.auth_postgres_password,
        host=settings.auth_postgres_host,
        port=settings.auth_postgres_port,
        database=settings.auth_postgres_db
    ),
    "JWT_SECRET_KEY": settings.jwt_secret_key,
    "JWT_ENCODE_NBF": False,
    "REDIS_HOST": settings.auth_redis_host,
    "REDIS_PORT": settings.auth_redis_port,
    "ACCESS_TOKEN_MINUTES": settings.auth_access_token_minutes,
    "REFRESH_TOKEN_MINUTES": settings.auth_refresh_token_minutes,
}
