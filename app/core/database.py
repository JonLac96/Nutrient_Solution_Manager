from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import database_url

# SQLite erlaubt Verbindungen standardmäßig nur im erzeugenden Thread.
# FastAPI kann Requests in anderen Threads bearbeiten.
engine = create_engine(
    database_url(),
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
