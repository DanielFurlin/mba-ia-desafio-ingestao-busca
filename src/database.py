import psycopg2 as pg
from psycopg2.extensions import connection as PgConnection

from settings import settings


def connect_to_database() -> PgConnection:
    return pg.connect(
        host=settings.db_host,
        port=settings.db_port,
        database=settings.db_name,
        user=settings.db_user,
        password=settings.db_password.get_secret_value(),
    )


def setup_database() -> PgConnection:
    try:
        return connect_to_database()
    except pg.Error as e:
        raise RuntimeError("Não foi possível conectar ao banco de dados.") from e


def get_connection_string() -> str:
    s = settings
    return f"postgresql://{s.db_user}:{s.db_password.get_secret_value()}@{s.db_host}:{s.db_port}/{s.db_name}"
