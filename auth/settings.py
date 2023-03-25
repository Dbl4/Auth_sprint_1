from pydantic import BaseSettings


class Settings(BaseSettings):
    auth_postgres_user: str
    auth_postgres_password: str
    auth_postgres_host: str
    auth_postgres_port: int
    auth_postgres_db: str


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')
