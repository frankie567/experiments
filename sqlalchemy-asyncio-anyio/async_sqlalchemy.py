"""
SQLAlchemy asyncio extension using anyio.

This module provides anyio-compatible wrappers around SQLAlchemy's official asyncio
extension. It enables using SQLAlchemy's async functionality with anyio for backend-
agnostic async support (works with asyncio, trio, etc.).

Important: This implementation wraps SQLAlchemy's official AsyncEngine and AsyncSession,
which use async database drivers (like aiosqlite, asyncpg) directly - not thread pools.

Architecture:
    User Code → Our anyio Wrapper → SQLAlchemy AsyncEngine → Async DB Drivers → Database

Benefits:
- Backend-agnostic async (anyio vs asyncio-only)
- Uses async drivers directly (via SQLAlchemy's extension)
- Same API as SQLAlchemy's official async extension
- Works with asyncio, trio, and other anyio backends
"""

from __future__ import annotations

import functools
from typing import Any, AsyncIterator, Optional, Sequence, Type, TypeVar
from contextlib import asynccontextmanager

import anyio
from sqlalchemy.ext.asyncio import (
    create_async_engine as _sa_create_async_engine,
    AsyncEngine as _SAAsyncEngine,
    AsyncConnection as _SAAsyncConnection,
    AsyncSession as _SAAsyncSession,
    async_sessionmaker as _sa_async_sessionmaker,
)
from sqlalchemy.ext.asyncio import AsyncResult as _SAAsyncResult


T = TypeVar("T")


class AsyncEngine:
    """
    Anyio-compatible wrapper around SQLAlchemy's AsyncEngine.
    
    This wraps SQLAlchemy's official AsyncEngine to provide anyio compatibility.
    The underlying engine uses async database drivers (like aiosqlite) directly.
    """
    
    def __init__(self, sa_async_engine: _SAAsyncEngine):
        """
        Initialize AsyncEngine with SQLAlchemy's AsyncEngine.
        
        Args:
            sa_async_engine: A SQLAlchemy AsyncEngine instance
        """
        self._sa_engine = sa_async_engine
    
    @property
    def sync_engine(self):
        """Access the underlying synchronous engine for table creation."""
        return self._sa_engine.sync_engine
    
    @property
    def url(self):
        """Get the database URL."""
        return self._sa_engine.url
    
    @property
    def dialect(self):
        """Get the database dialect."""
        return self._sa_engine.dialect
    
    async def dispose(self) -> None:
        """Dispose of the connection pool."""
        await self._sa_engine.dispose()
    
    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        """
        Get an async connection context manager.
        
        Usage:
            async with engine.connect() as conn:
                result = await conn.execute(query)
        """
        async with self._sa_engine.connect() as sa_conn:
            yield AsyncConnection(sa_conn)
    
    @asynccontextmanager
    async def begin(self) -> AsyncIterator[AsyncConnection]:
        """
        Get an async connection with automatic transaction management.
        
        Usage:
            async with engine.begin() as conn:
                await conn.execute(query)
                # Transaction is automatically committed
        """
        async with self._sa_engine.begin() as sa_conn:
            yield AsyncConnection(sa_conn)


class AsyncConnection:
    """
    Anyio-compatible wrapper around SQLAlchemy's AsyncConnection.
    
    Provides async methods for executing queries and managing transactions.
    Uses async database drivers directly (no thread pool).
    """
    
    def __init__(self, sa_async_connection: _SAAsyncConnection):
        """
        Initialize AsyncConnection with SQLAlchemy's AsyncConnection.
        
        Args:
            sa_async_connection: A SQLAlchemy AsyncConnection instance
        """
        self._sa_conn = sa_async_connection
    
    async def run_sync(self, fn, *args, **kwargs):
        """
        Run a synchronous function in a worker thread.
        
        This is useful for operations like metadata.create_all() or metadata.drop_all()
        that need to run synchronously.
        
        Args:
            fn: Synchronous function to run
            *args: Positional arguments
            **kwargs: Keyword arguments
        """
        return await self._sa_conn.run_sync(fn, *args, **kwargs)
    
    async def execute(self, statement, parameters=None) -> AsyncResult:
        """
        Execute a SQL statement asynchronously.
        
        Args:
            statement: SQL statement to execute
            parameters: Optional parameters for the statement
            
        Returns:
            AsyncResult wrapping the result set
        """
        if parameters is not None:
            result = await self._sa_conn.execute(statement, parameters)
        else:
            result = await self._sa_conn.execute(statement)
        return AsyncResult(result)
    
    async def scalar(self, statement, parameters=None) -> Any:
        """
        Execute a statement and return a scalar result.
        
        Args:
            statement: SQL statement to execute
            parameters: Optional parameters for the statement
            
        Returns:
            Scalar value from the result
        """
        if parameters is not None:
            return await self._sa_conn.scalar(statement, parameters)
        else:
            return await self._sa_conn.scalar(statement)
    
    async def commit(self) -> None:
        """Commit the current transaction."""
        await self._sa_conn.commit()
    
    async def rollback(self) -> None:
        """Roll back the current transaction."""
        await self._sa_conn.rollback()
    
    async def close(self) -> None:
        """Close the connection."""
        await self._sa_conn.close()
    
    @asynccontextmanager
    async def begin(self):
        """
        Begin a transaction as an async context manager.
        
        Usage:
            async with conn.begin():
                await conn.execute(query)
                # Transaction is automatically committed
        """
        async with self._sa_conn.begin():
            yield self


class AsyncResult:
    """
    Anyio-compatible wrapper around SQLAlchemy's Result/CursorResult.
    
    Note: The underlying result from SQLAlchemy's async engine is already
    fully buffered and has synchronous methods, so this wrapper provides
    the same synchronous API.
    """
    
    def __init__(self, sa_async_result):
        """
        Initialize AsyncResult with SQLAlchemy's result.
        
        Args:
            sa_async_result: A SQLAlchemy Result/CursorResult instance
        """
        self._sa_result = sa_async_result
    
    def fetchone(self):
        """Fetch one row from the result set."""
        return self._sa_result.fetchone()
    
    def fetchall(self) -> Sequence:
        """Fetch all rows from the result set."""
        return self._sa_result.fetchall()
    
    def fetchmany(self, size: Optional[int] = None) -> Sequence:
        """Fetch multiple rows from the result set."""
        if size is not None:
            return self._sa_result.fetchmany(size)
        return self._sa_result.fetchmany()
    
    def scalar(self) -> Any:
        """Return a scalar result."""
        return self._sa_result.scalar()
    
    def scalars(self) -> AsyncScalars:
        """Return an AsyncScalars object for scalar iteration."""
        return AsyncScalars(self._sa_result.scalars())
    
    def all(self) -> Sequence:
        """Fetch all rows from the result set (alias for fetchall)."""
        return self._sa_result.all()
    
    def first(self):
        """Fetch the first row from the result set."""
        return self._sa_result.first()
    
    def one(self):
        """Fetch exactly one row, raise if zero or multiple rows."""
        return self._sa_result.one()
    
    def one_or_none(self):
        """Fetch one row or None if no rows."""
        return self._sa_result.one_or_none()


class AsyncScalars:
    """
    Anyio-compatible wrapper for scalar results.
    
    Provides methods for fetching scalar values.
    """
    
    def __init__(self, sa_scalars):
        """
        Initialize AsyncScalars with SQLAlchemy's ScalarResult.
        
        Args:
            sa_scalars: A SQLAlchemy ScalarResult instance
        """
        self._sa_scalars = sa_scalars
    
    def all(self) -> Sequence:
        """Fetch all scalar values."""
        return self._sa_scalars.all()
    
    def first(self):
        """Fetch the first scalar value."""
        return self._sa_scalars.first()
    
    def one(self):
        """Fetch exactly one scalar value."""
        return self._sa_scalars.one()
    
    def one_or_none(self):
        """Fetch one scalar value or None."""
        return self._sa_scalars.one_or_none()


class AsyncSession:
    """
    Anyio-compatible wrapper around SQLAlchemy's AsyncSession.
    
    Provides async methods for ORM operations.
    """
    
    def __init__(self, sa_async_session: _SAAsyncSession):
        """
        Initialize AsyncSession with SQLAlchemy's AsyncSession.
        
        Args:
            sa_async_session: A SQLAlchemy AsyncSession instance
        """
        self._sa_session = sa_async_session
    
    async def execute(self, statement, parameters=None) -> AsyncResult:
        """
        Execute a statement asynchronously.
        
        Args:
            statement: SQL or ORM statement to execute
            parameters: Optional parameters for the statement
            
        Returns:
            AsyncResult wrapping the result set
        """
        if parameters is not None:
            result = await self._sa_session.execute(statement, parameters)
        else:
            result = await self._sa_session.execute(statement)
        return AsyncResult(result)
    
    async def scalar(self, statement, parameters=None) -> Any:
        """
        Execute a statement and return a scalar result.
        
        Args:
            statement: SQL or ORM statement to execute
            parameters: Optional parameters for the statement
            
        Returns:
            Scalar value from the result
        """
        if parameters is not None:
            return await self._sa_session.scalar(statement, parameters)
        else:
            return await self._sa_session.scalar(statement)
    
    async def get(self, entity: Type[T], ident: Any) -> Optional[T]:
        """
        Get an entity by primary key.
        
        Args:
            entity: The entity class
            ident: The primary key identifier
            
        Returns:
            Entity instance or None
        """
        return await self._sa_session.get(entity, ident)
    
    def add(self, instance: Any) -> None:
        """
        Add an instance to the session (synchronous).
        
        Args:
            instance: The entity instance to add
        """
        self._sa_session.add(instance)
    
    def add_all(self, instances: Sequence[Any]) -> None:
        """
        Add multiple instances to the session (synchronous).
        
        Args:
            instances: Sequence of entity instances to add
        """
        self._sa_session.add_all(instances)
    
    async def delete(self, instance: Any) -> None:
        """
        Delete an instance from the database.
        
        Args:
            instance: The entity instance to delete
        """
        await self._sa_session.delete(instance)
    
    async def commit(self) -> None:
        """Commit the current transaction."""
        await self._sa_session.commit()
    
    async def rollback(self) -> None:
        """Roll back the current transaction."""
        await self._sa_session.rollback()
    
    async def flush(self) -> None:
        """Flush pending changes to the database."""
        await self._sa_session.flush()
    
    async def refresh(self, instance: Any) -> None:
        """
        Refresh an instance from the database.
        
        Args:
            instance: The entity instance to refresh
        """
        await self._sa_session.refresh(instance)
    
    async def close(self) -> None:
        """Close the session."""
        await self._sa_session.close()


class AsyncSessionmaker:
    """
    Factory for creating AsyncSession instances.
    
    Wraps SQLAlchemy's async_sessionmaker for anyio compatibility.
    """
    
    def __init__(
        self,
        bind: Optional[AsyncEngine] = None,
        **kwargs
    ):
        """
        Initialize AsyncSessionmaker.
        
        Args:
            bind: Optional AsyncEngine to bind sessions to
            **kwargs: Additional arguments passed to async_sessionmaker
        """
        self._bind = bind
        self._sa_sessionmaker = _sa_async_sessionmaker(
            bind=bind._sa_engine if bind else None,
            **kwargs
        )
    
    @asynccontextmanager
    async def __call__(self) -> AsyncIterator[AsyncSession]:
        """
        Create and yield an async session.
        
        Usage:
            async with sessionmaker() as session:
                await session.execute(query)
                await session.commit()
        """
        async with self._sa_sessionmaker() as sa_session:
            yield AsyncSession(sa_session)
    
    @asynccontextmanager
    async def begin(self) -> AsyncIterator[AsyncSession]:
        """
        Create a session with automatic transaction management.
        
        Usage:
            async with sessionmaker.begin() as session:
                await session.execute(query)
                # Transaction is automatically committed
        """
        async with self._sa_sessionmaker.begin() as sa_session:
            yield AsyncSession(sa_session)


def create_async_engine(url: str, **kwargs) -> AsyncEngine:
    """
    Create an AsyncEngine instance.
    
    This creates a SQLAlchemy AsyncEngine that uses async database drivers
    (like aiosqlite, asyncpg) directly - no thread pool execution.
    
    Args:
        url: Database URL with async driver (e.g., "sqlite+aiosqlite:///./test.db")
        **kwargs: Additional arguments passed to create_async_engine
        
    Returns:
        AsyncEngine instance
    
    Example:
        engine = create_async_engine("sqlite+aiosqlite:///./test.db")
    """
    sa_engine = _sa_create_async_engine(url, **kwargs)
    return AsyncEngine(sa_engine)
