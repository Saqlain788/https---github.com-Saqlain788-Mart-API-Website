from sqlmodel import create_engine, Session, SQLModel
from app import settings

connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)
engine = create_engine(
    connection_string, connect_args={}, pool_recycle=300
)

def create_db_and_tables():
    SQLModel.metadata.drop_all(engine)  # Drop all tables
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()
    print("Tables created successfully")

def get_session():
    with Session(engine) as session:
        yield session
