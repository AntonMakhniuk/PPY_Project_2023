from typing import Iterable

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session, registry

metadata = MetaData()
mapper_registry = registry(metadata=metadata)

DB_URL = "sqlite:///my.db"


engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
connection = engine.connect()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_new_session() -> Iterable[Session]:
    with SessionLocal() as db:
        yield db


def close_connection() -> None:
    connection.close()


get_db = get_new_session
