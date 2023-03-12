import os

from pydantic import AnyHttpUrl, BaseSettings, Field, RedisDsn


class TestSettings(BaseSettings):
    elastic_url: AnyHttpUrl = Field("http://localhost:9200", env="ELASTIC_URL")
    redis_dsn: RedisDsn = Field("redis://localhost:6379", env="REDIS_DSN")
    service_url: AnyHttpUrl = Field("http://localhost:8000", env="SERVICE_URL")


test_settings = TestSettings()
