import psycopg2
from psycopg2.extras import RealDictCursor


def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(host='localhost',
                                database='fastapi',
                                user='postgres',
                                password='Admin#123',
                                cursor_factory=RealDictCursor)
        print("Database connection successful")

    except Exception as e:
        print(f"Failed to connect to the database {e}")

    finally:
        return conn
