from sqlmodel import create_engine, Session, SQLModel
from app import settings

connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)
engine = create_engine(
    connection_string, connect_args={}, pool_recycle=300
)


def get_session():
    with Session(engine) as session:
        yield session
