from mariadb import connect
from mariadb.connections import Connection
from functools import lru_cache
from config import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()
settings = get_settings()


DATABASE = settings.database
USER = settings.db_user
PASSWORD = settings.db_password
HOST = settings.db_host
PORT = settings.db_port


def _get_connection() -> Connection:
    return connect(
        database=DATABASE,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
    )


def read_query(sql: str, sql_params: tuple = ()) -> list:
    with _get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(sql, sql_params)

        return list(cursor)
    

def insert_query(sql: str, sql_params: tuple = ()) -> list:
    with _get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(sql, sql_params)
        connection.commit()

        return list(cursor)
    

def update_query(sql: str, sql_params: tuple = ()) -> list:
    with _get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(sql, sql_params)
        connection.commit()

        return list(cursor)
    

def delete_query(sql: str, sql_params: tuple = ()) -> list:
    with _get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(sql, sql_params)
        connection.commit()

        return list(cursor)
    


