from psycopg2 import Error, extras
from psycopg2.extensions import connection as _connection
from redis_storage import State
from table import ElasticGenre, ElasticIndex, ElasticPerson
from util import genres_query, log, persons_query, postgres_main_query

# logging setup
logger = log(__name__)


class PostgresExtractor:
    DB_NAMES: dict = {
        'movies': 'film_work',
        'persons': 'person',
        'genres': 'genre',
    }
    DB_QUERIES: dict = {
        'movies': postgres_main_query,
        'persons': persons_query,
        'genres': genres_query,
    }
    INDEX_MODELS: dict = {
        'movies': ElasticIndex,
        'persons': ElasticPerson,
        'genres': ElasticGenre,
    }

    def __init__(self, index: str, conn: _connection, state: State):
        """
        Organize input fields through pydentic mechanics.

        Args:
            conn: _connection
        """
        self.conn = conn
        self.cursor = conn.cursor(cursor_factory=extras.DictCursor)
        self.state = state
        self.index = index

    def extract(self) -> None:
        """
        Extract from PG.

        Get data with condition of date

        Args:
            date: date to query
        """

        try:
            self.cursor.execute(f"""SELECT MIN(modified) FROM content.{self.DB_NAMES[self.index]}""")
            min_modified_date = self.cursor.fetchone()
            modified_date = self.state.get_state(self.index)

            # Уменьшаю минимальное время на одну миллисекунду, что бы учесть оригинальное минимальное время при
            # строгой выборке
            modified_date = modified_date if modified_date else min_modified_date[0]\
                .replace(microsecond=min_modified_date[0].microsecond - 1)

            self.DB_QUERIES[self.index](self.cursor, modified_date)

        # Using special error handler from psycopg
        except (Exception, Error) as error:
            logger.exception(error)

    def transform(self, data: list) -> list:

        res = []
        for elem in data:
            res.append(self.INDEX_MODELS[self.index].from_pg(elem))

        return res
