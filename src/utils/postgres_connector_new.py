from psycopg2.extras import RealDictCursor
import pandas as pd
from psycopg2 import connect

client_connection = connect(
    user='michaelm',
    host='34.148.134.7',
    database='issac_data',
    password='michael1231',
    port=5432
)

from contextlib import contextmanager

@contextmanager
def get_client_connection():
    connection = client_connection
    try:
        print("connection successful")
        yield connection
    finally:
        connection.close()


@contextmanager
def get_curser(connection):
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            yield cursor
        finally:
             cursor.close()


def exec_query(sql,binds=None,commit=True,return_data=False):
    try:
        with get_client_connection() as conn:
            with get_curser(conn) as cursor: 
                cursor.execute(sql, binds)
                if return_data:
                    return pd.DataFrame(cursor.fetchall(), columns=cursor.column_mapping)
                if commit:
                    conn.commit()
    except Exception as e:
                conn.rollback()
                raise Exception(f"Error in execute_query: {e}")

# @contextmanager
# def get_curser(connection):
#     with connection.cursor(cursor_factory=RealDictCursor) as cursor:
#          yield cursor

# @contextmanager
# def get_connection_pool():
#     connection = pool_new_prod.getconn()
#     try:
#         print("connection successful")
#         yield connection
#     finally:
#         pool_new_prod.putconn(connection)




def returnThisF():
    return "hello how are you"