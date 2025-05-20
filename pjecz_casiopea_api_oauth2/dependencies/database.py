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


def get_engine(settings: Annotated[Settings, Depends(get_settings)]) -> Engine:
    """Database engine"""

    # Create engine
    engine = create_engine(
        f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )

    return engine


async def get_db(settings: Annotated[Settings, Depends(get_settings)]) -> Session:
    """Database session"""

    # Create engine
    engine = get_engine(settings)

    # Create session
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    try:
        database = session_local()
        yield database
    finally:
        database.close()
