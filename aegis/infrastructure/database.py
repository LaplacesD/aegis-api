"""Async PostgreSQL database setup using SQLAlchemy."""

from __future__ import annotations

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from aegis.config import Settings


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""
    pass


class Database:
    """Async database engine and session factory manager.

    Usage:
        db = Database(settings)
        async with db.session() as session:
            ...
    """

    def __init__(self, settings: Settings) -> None:
        self._engine = create_async_engine(
            settings.database_url,
            echo=settings.debug,
            pool_size=5,
            max_overflow=10,
        )
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """Provide an async session as a context manager.

        Yields:
            An AsyncSession instance.
        """
        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def create_all(self) -> None:
        """Create all tables defined in the ORM metadata."""
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def dispose(self) -> None:
        """Dispose of the database engine."""
        await self._engine.dispose()
