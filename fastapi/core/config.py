from enum import Enum
from logging import config as logging_config

from core.logger import LOGGING
from pydantic import AnyHttpUrl, BaseSettings, Field, RedisDsn

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class LoggerLevel(str, Enum):
    critical = "CRITICAL"
    error = "ERROR"
    warning = "WARNING"
    info = "INFO"
    debug = "DEBUG"
    notset = "NOTSET"


class Settings(BaseSettings):
    logger_level: LoggerLevel = LoggerLevel.debug
    # Название проекта. Используется в Swagger-документации
    project_name: str = Field(
        "Read-only API для онлайн-кинотеатра",
        env="PROJECT_NAME",
    )
    redis_dsn: RedisDsn = Field("redis://localhost:6379", env="REDIS_DSN")
    elastic_url: AnyHttpUrl = Field("http://localhost:9200", env="ELASTIC_URL")
    gunicorn_host: str = Field("0.0.0.0", env="GUNICORN_HOST")
    gunicorn_port: int = Field(8000, env="GUNICORN_PORT")
    service_url: AnyHttpUrl = Field("http://localhost:9200", env="SERVICE_URL")


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
