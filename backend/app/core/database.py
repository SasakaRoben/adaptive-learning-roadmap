import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from app.core.config import settings

def get_db_connection():
    """Create a database connection"""
    conn = psycopg2.connect(
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT,
        database=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        cursor_factory=RealDictCursor
    )
    return conn

@contextmanager
def get_db():
    """Context manager for database connections"""
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
       