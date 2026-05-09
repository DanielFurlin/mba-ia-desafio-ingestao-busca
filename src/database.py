import os
import psycopg2 as pg
from psycopg2.extensions import connection as PgConnection


def connect_to_database() -> PgConnection:
  return pg.connect(
    host=os.getenv("DATABASE_URL"),
    port=os.getenv("DB_PORT", "5432"),
    database=os.getenv("DB_NAME", "rag"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD", "postgres"),
  )


def setup_database() -> PgConnection:
  try:
    return connect_to_database()
  except pg.Error as e:
    print(f"Não foi possível conectar ao banco de dados: {e}")
    exit(1)


def get_connection_string() -> str:
  user = os.getenv("DB_USER", "postgres")
  password = os.getenv("DB_PASSWORD", "postgres")
  host = os.getenv("DATABASE_URL")
  port = os.getenv("DB_PORT", "5432")
  name = os.getenv("DB_NAME", "rag")
  return f"postgresql://{user}:{password}@{host}:{port}/{name}"
