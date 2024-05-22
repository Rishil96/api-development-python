import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Function to connect to database using psycopg2 which will allow us to execute raw SQL passed as string to cursor
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


# ORM Database Connection Setup

# 1. Create a connection string
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Admin#123@localhost/fastapi"

# 2. Create an engine which is responsible for SQLAlchemy to connect to a database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 3. To actually talk to a database we make use of sessions
SessionLocal = sessionmaker(autoflush=False, bind=engine)

# 4. All of our models that we define to create our tables in Postgres will extend this base class
Base = declarative_base()
