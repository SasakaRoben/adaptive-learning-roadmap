import psycopg
from psycopg.rows import dict_row
from contextlib import contextmanager
from app.core.config import settings
from typing import Generator
from psycopg import Connection as PGConnection

def get_db_connection() -> PGConnection:
    """Create a database connection.

    Returns a psycopg2 connection configured with a dict-like cursor.
    A small connect timeout and application_name are set for resilience and observability.
    """
    conn = psycopg.connect(
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT,
        dbname=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        connect_timeout=10,
        application_name="adaptive-learning-api",
        row_factory=dict_row,
    )
    return conn

@contextmanager
def get_db() -> Generator[PGConnection, None, None]:
    """Context manager for database connections.

    Commits on success, rolls back on error, and always closes the connection.
    """
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
       