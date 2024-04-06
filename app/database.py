from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv()

db_password = os.getenv('DB_PASS')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')

# Connessione al database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{db_user}:{db_password}@localhost/{db_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)



SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# DeclarativeBase per sqlalchemy 2.0
class Base(DeclarativeBase):
    pass

# Function to test the database connection and print all tables
def test_db_connection():
    try:
        with engine.connect() as connection:
            # Query to get all table names
            result = connection.execute(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
            """))
            tables = result.fetchall()
            print("Database connection successful!")
            print("Tables in the database:")
            for table in tables:
                print(table[0])
    except Exception as e:
        print(f"Database connection failed! ERROR: {e}")
# Call the function to test the connection
test_db_connection()