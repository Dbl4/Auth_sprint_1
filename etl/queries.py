"""SQL запросы для извлечения данных для пайплайнов."""

FILMWORK_SQL = """
SELECT
    f.id as uuid,
    f.title,
    f.description,
    f.rating as imdb_rating,
    COALESCE (
        json_agg (
            DISTINCT jsonb_build_object (
                'uuid', p.id,
                'full_name', p.full_name
            )
        ) FILTER (WHERE p.id is not null AND pf.role = 'actor'),
        '[]'
    ) as actors,
    COALESCE (
        json_agg (
            DISTINCT jsonb_build_object (
                'uuid', p.id,
                'full_name', p.full_name
            )
        ) FILTER (WHERE p.id is not null AND pf.role = 'writer'),
        '[]'
    ) as writers,
    COALESCE (
        json_agg (
            DISTINCT jsonb_build_object (
                'uuid', p.id,
                'full_name', p.full_name
            )
        ) FILTER (WHERE p.id is not null AND pf.role = 'director'),
        '[]'
    ) as directors,
    COALESCE (
        json_agg (
            DISTINCT jsonb_build_object (
                'uuid', g.id,
                'name', g.name
            )
        ) FILTER (WHERE g.id is not null AND gf.film_work_id = f.id),
        '[]'
    ) as genres,
    COALESCE (
        array_agg (DISTINCT p.full_name) FILTER (
            WHERE p.id is not null AND pf.role = 'writer'
        ),
        '{{}}'
    ) as writers_names,
    COALESCE (
        array_agg (DISTINCT p.full_name) FILTER (
            WHERE p.id is not null AND pf.role = 'actor'
        ),
        '{{}}'
    ) as actors_names,
    COALESCE (
        array_agg (DISTINCT p.full_name) FILTER (
            WHERE p.id is not null AND pf.role = 'director'
        ),
        '{{}}'
    ) as directors_names
FROM {schema}.film_work f
LEFT JOIN {schema}.person_film_work pf ON pf.film_work_id = f.id
LEFT JOIN {schema}.person p ON p.id = pf.person_id
LEFT JOIN {schema}.genre_film_work gf ON gf.film_work_id = f.id
LEFT JOIN {schema}.genre g ON g.id = gf.genre_id
WHERE (
    f.modified > %(timepoint)s
    OR p.modified > %(timepoint)s
    OR g.modified > %(timepoint)s
)
GROUP BY f.id
"""

GENRE_SQL = """
SELECT
    id as uuid,
    name,
    description
FROM {schema}.genre
WHERE modified > %(timepoint)s
"""

PERSON_SQL = """
SELECT
    p.id AS uuid,
    p.full_name,
    pf.role,
    COALESCE (
        array_agg (DISTINCT CAST(f.id AS VARCHAR)),
        '{{}}'
    ) as film_ids
FROM
    {schema}.person p
    LEFT JOIN {schema}.person_film_work pf ON pf.person_id = p.id
    LEFT JOIN {schema}.film_work f ON f.id = pf.film_work_id
WHERE (
    p.modified > %(timepoint)s
    OR pf.created > %(timepoint)s
    OR f.modified > %(timepoint)s
)
GROUP BY
    p.id, pf.role
"""
