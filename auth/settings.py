from pydantic import BaseSettings, PostgresDsn, Field


class Settings(BaseSettings):
    auth_postgres_url: PostgresDsn = Field("postgresql://app:123qwe@localhost:5432/auth",
                                           env="AUTH_POSTGRES_URL")


settings = Settings()
