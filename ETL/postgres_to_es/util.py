import logging
import os
import time


# looping decorator
def sleep(timeout):
    def the_real_decorator(function):
        def wrapper(*args, **kwargs):
            while True:
                function(*args, **kwargs)
                time.sleep(timeout)
        return wrapper
    return the_real_decorator


def log(name):
    if not os.path.exists('logs'):
        os.mkdir('logs')
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(f"logs/{name}.log", mode='w', encoding='utf-8')
    formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def postgres_main_query(cursor, date):
    query = f"""
            SELECT
               fw.id,
               fw.title,
               fw.description,
               fw.rating,
               fw.type,
               fw.created,
               fw.modified,
               COALESCE (
                   json_agg(
                       DISTINCT jsonb_build_object(
                           'person_role', pfw.role,
                           'person_id', p.id,
                           'person_name', p.full_name
                       )
                   ) FILTER (WHERE p.id is not null),
                   '[]'
               ) as persons,
                COALESCE (
                   json_agg(
                       DISTINCT jsonb_build_object(
                           'id', g.id,
                           'name', g.name
                       )
                   ) FILTER (WHERE g.id is not null),
                   '[]'
               ) as genres
            FROM content.film_work fw
            LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
            LEFT JOIN content.person p ON p.id = pfw.person_id
            LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
            LEFT JOIN content.genre g ON g.id = gfw.genre_id
            WHERE fw.modified > '{date}'
            GROUP BY fw.id
            ORDER BY fw.modified
            """
    cursor.execute(query)


def persons_query(cursor, date):
    query = f"""
            SELECT
               p.id,
               p.full_name,
               p.modified,
               COALESCE (
                   json_agg(
                       DISTINCT jsonb_build_object(
                           'id', fw.id,
                           'title', fw.title,
                           'imdb_rating', fw.rating
                       )
                   ) FILTER (WHERE fw.id is not null AND pfw.role = 'director'),
                   '[]'
               ) as director_films,
               COALESCE (
                   json_agg(
                       DISTINCT jsonb_build_object(
                           'id', fw.id,
                           'title', fw.title,
                           'imdb_rating', fw.rating
                       )
                   ) FILTER (WHERE fw.id is not null AND pfw.role = 'actor'),
                   '[]'
               ) as actor_films,
               COALESCE (
                   json_agg(
                       DISTINCT jsonb_build_object(
                           'id', fw.id,
                           'title', fw.title,
                           'imdb_rating', fw.rating
                       )
                   ) FILTER (WHERE fw.id is not null AND pfw.role = 'writer'),
                   '[]'
               ) as writer_films
            FROM content.person p
            LEFT JOIN content.person_film_work pfw ON pfw.person_id = p.id
            LEFT JOIN content.film_work fw ON pfw.film_work_id = fw.id
            WHERE p.modified > '{date}'
            GROUP BY p.id
            ORDER BY p.modified
            """
    cursor.execute(query)


def genres_query(cursor, date):
    query = f"""
            SELECT id, name, modified from content.genre
            where modified > '{date}'
            order by modified
            """
    cursor.execute(query)
