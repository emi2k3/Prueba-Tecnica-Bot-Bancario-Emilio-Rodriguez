from psycopg2.extensions import connection, cursor
from psycopg2.errors import RaiseException
import psycopg2.pool
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv() 


conn_pool = psycopg2.pool.SimpleConnectionPool(
    1,20,
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    host=os.getenv("POSTGRES_HOST"),
    password=os.getenv("POSTGRES_PASSWORD")
)

def getConnection() -> connection:
    if not conn_pool:
        raise RuntimeError("Pool de conexiones no se pudo inicializar")
    return conn_pool.getconn()
def returnConnection(conn:connection):
    if conn_pool and conn:
        conn_pool.putconn(conn)

