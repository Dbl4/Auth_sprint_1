"""Скрипт загружает обновленные данные из Postgres в Elastic Search."""

import contextlib
import json
import logging
import os
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from time import sleep

import backoff
import psycopg2
from elasticsearch import ConnectionError, ConnectionTimeout, Elasticsearch
from elasticsearch import TransportError
from psycopg2.extras import DictCursor

import elastic
import models
import postgresql
import queries
import state as st

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger("etl")
    logger.setLevel(logging.DEBUG)
    file_handler = RotatingFileHandler(
        "etl.log",
        maxBytes=5000000,
        backupCount=5,
    )
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)

    connect_postgres = backoff.on_exception(
        wait_gen=backoff.expo,
        exception=(psycopg2.Error, psycopg2.OperationalError),
    )(
        psycopg2.connect,
    )

    connect_elastic = backoff.on_exception(
        wait_gen=backoff.expo,
        exception=(ConnectionError, TransportError, ConnectionTimeout),
    )(
        Elasticsearch,
    )

    # Перед запуском ETL загрузить в Elasticsearch схемы из папки schemas
    with contextlib.closing(
        connect_elastic(
            os.environ["ELASTIC_URL"],
        ),
    ) as es:
        for entry in os.scandir("schemas"):
            if not entry.name.endswith(".json"):
                continue
            with open(entry.path) as file:
                response = es.indices.create(
                    index=entry.name[:-5],
                    body=json.load(file),
                    ignore=400,  # ignore 400 already exists code
                )

    while True:
        logger.info(
            "Connecting to Postgres at "
            + os.environ["POSTGRES_HOST"]
            + ":"
            + os.environ["POSTGRES_PORT"]
            + "/"
            + os.environ["POSTGRES_DB"],
        )
        logger.info(
            "Connecting to Elasticsearch at " + os.environ["ELASTIC_URL"],
        )
        with (
            contextlib.closing(
                connect_postgres(
                    host=os.environ["POSTGRES_HOST"],
                    port=os.environ["POSTGRES_PORT"],
                    database=os.environ["POSTGRES_DB"],
                    user=os.environ["POSTGRES_USER"],
                    password=os.environ["POSTGRES_PASSWORD"],
                    cursor_factory=DictCursor,
                ),
            ) as pg,
            contextlib.closing(
                connect_elastic(
                    os.environ["ELASTIC_URL"],
                ),
            ) as es,
        ):
            state = st.State(st.JsonFileStorage(os.environ["ETL_STATEFILE"]))
            timepoint_string = state.get_state(
                "timepoint",
                "0001-01-01T00:00:00.000000+00:00",
            )
            logger.info("Timepoint " + timepoint_string)
            timepoint = (
                datetime.strptime(timepoint_string, "%Y-%m-%dT%H:%M:%S.%f%z")
                if timepoint_string
                else datetime.min
            )
            next_timepoint = datetime.now(timezone.utc)

            for pipeline in [
                ("movies", queries.FILMWORK_SQL, models.Filmwork),
                ("genres", queries.GENRE_SQL, models.Genre),
                ("persons", queries.PERSON_SQL, models.Person),
            ]:
                logger.info("Processing pipeline '%s'", pipeline[0])
                extractor = postgresql.Extractor(
                    sql=pipeline[1],
                    connection=pg,
                    timepoint=timepoint,
                    model=pipeline[2],
                    schema=os.environ["POSTGRES_SCHEMA"],
                    batch_size=int(os.environ["ETL_BATCHSIZE"]),
                )
                loader = elastic.Loader(es, pipeline[0])

                for batch in extractor:
                    logger.info(
                        "Processing a batch of "
                        + str(len(batch))
                        + " elements",
                    )
                    loader.load_batch(batch)

            logger.info("Done successfully")

            state.set_state("timepoint", next_timepoint.isoformat())

        sleep(float(os.environ["ETL_DELAY"]))
