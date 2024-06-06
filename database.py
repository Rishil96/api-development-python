import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings


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
SQLALCHEMY_DATABASE_URL = (f"postgresql://{settings.database_username}:{settings.database_password}@"
                           f"{settings.database_hostname}:{settings.database_port}/{settings.database_name}")

# 2. Create an engine which is responsible for SQLAlchemy to connect to a database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 3. To actually talk to a database we make use of sessions
SessionLocal = sessionmaker(autoflush=False, bind=engine)

# 4. All of our models that we define to create our tables in Postgres will extend this base class
Base = declarative_base()


# 5. Create a dependency function that we can pass directly into route function to connect to the database
def get_db():
    db = SessionLocal()
    try:
        # Using yield instead of return is basically to retain control in this function so db connection can be closed.
        yield db
    finally:
        db.close()
