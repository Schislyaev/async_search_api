import os

from dotenv import load_dotenv

load_dotenv('.env.example')

# General settings
PAGE_SIZE = 500
TIMEOUT = 10

# Postgres settings
DSL = {
    'dbname': os.environ.get('PG_DB_NAME'),
    'user': os.environ.get('PG_USER'),
    'password': os.environ.get('PG_PASSWORD'),
    'host': os.environ.get('PG_HOST'),
    'port': os.environ.get('PG_PORT')
}

# Elastic settings
INDEX_NAMES = ['genres', 'movies', 'persons']
ELASTIC_HOST = os.environ.get('ELASTIC_HOST')
ELASTIC_PORT = os.environ.get('ELASTIC_PORT')

# Redis settings
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
REDIS_DB_NUMBER = 0
