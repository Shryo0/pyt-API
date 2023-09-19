import psycopg2
from psycopg2 import DatabaseError
from decouple import config

def get_connection():
    try:
        return psycopg2.connect(
            host=config('PGSQL_HOST'),   
            user=config('PGSQL_USER'),
            password=config('PGSQL_USER'),
            database=config('PGSQL_USER')
        )
    except DatabaseError as ex:
        raise ex