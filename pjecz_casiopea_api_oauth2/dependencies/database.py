"""
Database
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from ..config.settings import Settings, get_settings

Base = declarative_base()


def get_engine(settings: Settings = get_settings()) -> Engine:
    """Database engine"""
    return create_engine(
        f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )


engine = get_engine()
session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db(settings: Annotated[Settings, Depends(get_settings)]) -> Session:
    """Database session"""
    database = session_maker()
    try:
        yield database
    finally:
        database.close()
