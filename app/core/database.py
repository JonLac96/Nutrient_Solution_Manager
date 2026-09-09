from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import database_url

engine = create_engine(database_url())
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
