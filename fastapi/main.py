import logging

import uvicorn as uvicorn
from api.v1 import films, genres, persons
from core.config import settings
from core.logger import LOGGING
from db import elastic, redis
from elasticsearch import AsyncElasticsearch
from redis import asyncio as aioredis

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    description="Информация о фильмах, жанрах и персоналиях",
    version="1.0.0",
)


@app.on_event("startup")
async def startup():
    redis.redis = await aioredis.from_url(
        settings.redis_dsn,
        max_connections=10,
        encoding="utf8",
        decode_responses=True,
    )
    elastic.es = AsyncElasticsearch(hosts=[settings.elastic_url])


@app.on_event("shutdown")
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


app.include_router(
    films.router,
    tags=["Поиск кинопроизведений"],
)

app.include_router(
    genres.router,
    tags=["Жанры"],
)

app.include_router(
    persons.router,
    tags=["Персоналии"],
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.gunicorn_host,
        port=settings.gunicorn_port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
