from psycopg2.extensions import connection, cursor
from psycopg2.errors import RaiseException
import psycopg2.pool
import psycopg2
import os
import time
from dotenv import load_dotenv

load_dotenv() 

def wait_for_postgres():
    """Función utilizada para que el contenedor de telegram espere a que postgres este 100% disponible"""
    while True:
        try:
            conn = psycopg2.connect(
                dbname=os.getenv("POSTGRES_DB"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                host=os.getenv("POSTGRES_HOST"),
                port=os.getenv("POSTGRES_PORT", 5432)
            )
            conn.close()
            print("Postgres is ready!")
            break
        except psycopg2.OperationalError:
            print("Waiting for Postgres...")
            time.sleep(2)
wait_for_postgres()
conn_pool = psycopg2.pool.SimpleConnectionPool(
    1,20,
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    host=os.getenv("POSTGRES_HOST"),
    password=os.getenv("POSTGRES_PASSWORD")
)

def getConnection() -> connection:
    """Consigue una connection de la pool de conexiónes de nuestra BD"""
    if not conn_pool:
        raise RuntimeError("Pool de conexiones no se pudo inicializar")
    return conn_pool.getconn()
def returnConnection(conn:connection):
    """Retorna la connection a la pool de conexiónes de nuestra BD"""
    if conn_pool and conn:
        conn_pool.putconn(conn)



