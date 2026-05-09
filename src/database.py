import os
import psycopg2 as pg

DATABASE_URL = os.getenv("DATABASE_URL")
DB_PORT = os.getenv("DB_PORT") or 5432
DB_NAME = os.getenv("DB_NAME") or "rag"
DB_USER = os.getenv("DB_USER") or "postgres"
DB_PASSWORD = os.getenv("DB_PASSWORD") or "postgres"

def connect_to_database():
    conn = pg.connect(
        host=DATABASE_URL,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

def test_connection(conn):
    try:
        conn.cursor().execute("SELECT 1")
        return True
    except pg.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return False

def setup_database():
    conn = connect_to_database()
    if not conn:
        print("Não foi possível conectar ao banco de dados.")
        exit(1)
    
    if not test_connection(conn):
        print("Não foi possível testar a conexão com o banco de dados.")
        exit(1)

    return conn

def get_connection_string():
    return f"postgresql://{DB_USER}:{DB_PASSWORD}@{DATABASE_URL}:{DB_PORT}/{DB_NAME}"