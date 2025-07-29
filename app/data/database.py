from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from typing import Callable
import logging


class AsyncDatabase:

    def __init__(self, db_url: str) -> None:
        self._db_url = db_url
      
        logging.log(logging.DEBUG, "Database Initializing...")
        self._engine = create_async_engine(
            db_url,
            echo=False,
            pool_size=10,
            max_overflow=0,
            pool_pre_ping=True,
        )

        self._session_factory = sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False
        )

        self._metadata = MetaData()

        logging.log(logging.DEBUG, "Database Initialized...")

    @property
    def session_factory(self) -> Callable[..., AsyncSession]:
        return self._session_factory

    @property
    def engine(self) -> AsyncEngine:
        return self._engine
    
    @property
    def metadata(self) -> MetaData:
        return self._metadata
    
   

