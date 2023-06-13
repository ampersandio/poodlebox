from mariadb import connect
from mariadb.connections import Connection
import mariadb.constants.CLIENT as CLIENT
from config import settings



DATABASE = settings.db_name
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
        client_flag=CLIENT.MULTI_STATEMENTS | CLIENT.MULTI_RESULTS,
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

        return cursor.lastrowid

def update_query(sql: str, sql_params: tuple = ()) -> list:
    with _get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(sql, sql_params)
        connection.commit()

        return cursor.rowcount
    

    
def delete_query(sql: str, sql_params: tuple = ()) -> list:
    with _get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(sql, sql_params)
        connection.commit()

        return cursor.rowcount


def multiple_query(statements: str, params: list) -> None:
    with _get_connection() as connection:
        cursor = connection.cursor()

        statements = statements.split('; ')
        param_count = 0
        for statement in statements:
            param_count = statement.count('?')
            cursor.execute(statement, tuple(params[:param_count]))
            connection.commit()
            params = params[param_count:]