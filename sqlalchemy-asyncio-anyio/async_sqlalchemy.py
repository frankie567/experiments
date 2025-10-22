"""
SQLAlchemy asyncio extension reimplemented with anyio.

This module provides async versions of SQLAlchemy's core components using anyio
instead of gevent. The API is designed to be compatible with SQLAlchemy's
official asyncio extension.
"""

from __future__ import annotations

import functools
from typing import Any, AsyncIterator, Optional, Sequence, Type, TypeVar
from contextlib import asynccontextmanager

import anyio
from sqlalchemy import create_engine, Engine, Result, CursorResult
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool


T = TypeVar("T")


class AsyncEngine:
    """
    Async wrapper around SQLAlchemy's synchronous Engine.
    
    Uses anyio.to_thread.run_sync() to execute synchronous operations in a
    worker thread pool.
    """
    
    def __init__(self, sync_engine: Engine):
        """
        Initialize AsyncEngine with a synchronous engine.
        
        Args:
            sync_engine: A synchronous SQLAlchemy Engine instance
        """
        self._sync_engine = sync_engine
    
    @property
    def sync_engine(self) -> Engine:
        """Access the underlying synchronous engine."""
        return self._sync_engine
    
    @property
    def url(self):
        """Get the database URL."""
        return self._sync_engine.url
    
    @property
    def dialect(self):
        """Get the database dialect."""
        return self._sync_engine.dialect
    
    async def dispose(self) -> None:
        """Dispose of the connection pool."""
        await anyio.to_thread.run_sync(self._sync_engine.dispose)
    
    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        """
        Get an async connection context manager.
        
        Usage:
            async with engine.connect() as conn:
                result = await conn.execute(query)
        """
        # Get connection in thread pool
        sync_conn = await anyio.to_thread.run_sync(self._sync_engine.connect)
        
        async_conn = AsyncConnection(sync_conn)
        try:
            yield async_conn
        finally:
            await async_conn.close()
    
    @asynccontextmanager
    async def begin(self) -> AsyncIterator[AsyncConnection]:
        """
        Get an async connection with automatic transaction management.
        
        Usage:
            async with engine.begin() as conn:
                await conn.execute(query)
                # Transaction is automatically committed
        """
        async with self.connect() as conn:
            async with conn.begin():
                yield conn


class AsyncConnection:
    """
    Async wrapper around SQLAlchemy's synchronous Connection.
    
    Provides async methods for executing queries and managing transactions.
    """
    
    def __init__(self, sync_connection):
        """
        Initialize AsyncConnection with a synchronous connection.
        
        Args:
            sync_connection: A synchronous SQLAlchemy Connection instance
        """
        self._sync_connection = sync_connection
    
    @property
    def sync_connection(self):
        """Access the underlying synchronous connection."""
        return self._sync_connection
    
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
            result = await anyio.to_thread.run_sync(
                functools.partial(self._sync_connection.execute, statement, parameters)
            )
        else:
            result = await anyio.to_thread.run_sync(
                functools.partial(self._sync_connection.execute, statement)
            )
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
        result = await self.execute(statement, parameters)
        return await result.scalar()
    
    async def commit(self) -> None:
        """Commit the current transaction."""
        await anyio.to_thread.run_sync(self._sync_connection.commit)
    
    async def rollback(self) -> None:
        """Roll back the current transaction."""
        await anyio.to_thread.run_sync(self._sync_connection.rollback)
    
    async def close(self) -> None:
        """Close the connection."""
        await anyio.to_thread.run_sync(self._sync_connection.close)
    
    @asynccontextmanager
    async def begin(self):
        """
        Begin a transaction as an async context manager.
        
        Usage:
            async with conn.begin():
                await conn.execute(query)
                # Transaction is automatically committed
        """
        transaction = await anyio.to_thread.run_sync(self._sync_connection.begin)
        try:
            yield self
            await anyio.to_thread.run_sync(transaction.commit)
        except Exception:
            await anyio.to_thread.run_sync(transaction.rollback)
            raise


class AsyncResult:
    """
    Async wrapper around SQLAlchemy's Result/CursorResult.
    
    Provides async methods for fetching rows from a result set.
    """
    
    def __init__(self, sync_result: Result | CursorResult):
        """
        Initialize AsyncResult with a synchronous result.
        
        Args:
            sync_result: A synchronous SQLAlchemy Result instance
        """
        self._sync_result = sync_result
    
    @property
    def sync_result(self) -> Result | CursorResult:
        """Access the underlying synchronous result."""
        return self._sync_result
    
    async def fetchone(self):
        """Fetch one row from the result set."""
        return await anyio.to_thread.run_sync(self._sync_result.fetchone)
    
    async def fetchall(self) -> Sequence:
        """Fetch all rows from the result set."""
        return await anyio.to_thread.run_sync(self._sync_result.fetchall)
    
    async def fetchmany(self, size: Optional[int] = None) -> Sequence:
        """Fetch multiple rows from the result set."""
        if size is not None:
            return await anyio.to_thread.run_sync(
                functools.partial(self._sync_result.fetchmany, size)
            )
        return await anyio.to_thread.run_sync(self._sync_result.fetchmany)
    
    async def scalar(self) -> Any:
        """Return a scalar result."""
        return await anyio.to_thread.run_sync(self._sync_result.scalar)
    
    async def scalars(self) -> AsyncScalars:
        """Return an AsyncScalars object for scalar iteration."""
        scalars = await anyio.to_thread.run_sync(self._sync_result.scalars)
        return AsyncScalars(scalars)
    
    async def all(self) -> Sequence:
        """Fetch all rows from the result set (alias for fetchall)."""
        return await self.fetchall()
    
    async def first(self):
        """Fetch the first row from the result set."""
        return await anyio.to_thread.run_sync(self._sync_result.first)
    
    async def one(self):
        """Fetch exactly one row, raise if zero or multiple rows."""
        return await anyio.to_thread.run_sync(self._sync_result.one)
    
    async def one_or_none(self):
        """Fetch one row or None if no rows."""
        return await anyio.to_thread.run_sync(self._sync_result.one_or_none)


class AsyncScalars:
    """
    Async wrapper for scalar results.
    
    Provides async methods for fetching scalar values.
    """
    
    def __init__(self, sync_scalars):
        """
        Initialize AsyncScalars with synchronous scalars.
        
        Args:
            sync_scalars: A synchronous SQLAlchemy ScalarResult instance
        """
        self._sync_scalars = sync_scalars
    
    async def all(self) -> Sequence:
        """Fetch all scalar values."""
        return await anyio.to_thread.run_sync(self._sync_scalars.all)
    
    async def first(self):
        """Fetch the first scalar value."""
        return await anyio.to_thread.run_sync(self._sync_scalars.first)
    
    async def one(self):
        """Fetch exactly one scalar value."""
        return await anyio.to_thread.run_sync(self._sync_scalars.one)
    
    async def one_or_none(self):
        """Fetch one scalar value or None."""
        return await anyio.to_thread.run_sync(self._sync_scalars.one_or_none)


class AsyncSession:
    """
    Async wrapper around SQLAlchemy's ORM Session.
    
    Provides async methods for ORM operations.
    """
    
    def __init__(self, sync_session: Session):
        """
        Initialize AsyncSession with a synchronous session.
        
        Args:
            sync_session: A synchronous SQLAlchemy Session instance
        """
        self._sync_session = sync_session
    
    @property
    def sync_session(self) -> Session:
        """Access the underlying synchronous session."""
        return self._sync_session
    
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
            result = await anyio.to_thread.run_sync(
                functools.partial(self._sync_session.execute, statement, parameters)
            )
        else:
            result = await anyio.to_thread.run_sync(
                functools.partial(self._sync_session.execute, statement)
            )
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
        result = await self.execute(statement, parameters)
        return await result.scalar()
    
    async def get(self, entity: Type[T], ident: Any) -> Optional[T]:
        """
        Get an entity by primary key.
        
        Args:
            entity: The entity class
            ident: The primary key identifier
            
        Returns:
            Entity instance or None
        """
        return await anyio.to_thread.run_sync(
            functools.partial(self._sync_session.get, entity, ident)
        )
    
    def add(self, instance: Any) -> None:
        """
        Add an instance to the session (synchronous).
        
        Args:
            instance: The entity instance to add
        """
        self._sync_session.add(instance)
    
    def add_all(self, instances: Sequence[Any]) -> None:
        """
        Add multiple instances to the session (synchronous).
        
        Args:
            instances: Sequence of entity instances to add
        """
        self._sync_session.add_all(instances)
    
    async def delete(self, instance: Any) -> None:
        """
        Delete an instance from the database.
        
        Args:
            instance: The entity instance to delete
        """
        await anyio.to_thread.run_sync(
            functools.partial(self._sync_session.delete, instance)
        )
    
    async def commit(self) -> None:
        """Commit the current transaction."""
        await anyio.to_thread.run_sync(self._sync_session.commit)
    
    async def rollback(self) -> None:
        """Roll back the current transaction."""
        await anyio.to_thread.run_sync(self._sync_session.rollback)
    
    async def flush(self) -> None:
        """Flush pending changes to the database."""
        await anyio.to_thread.run_sync(self._sync_session.flush)
    
    async def refresh(self, instance: Any) -> None:
        """
        Refresh an instance from the database.
        
        Args:
            instance: The entity instance to refresh
        """
        await anyio.to_thread.run_sync(
            functools.partial(self._sync_session.refresh, instance)
        )
    
    async def close(self) -> None:
        """Close the session."""
        await anyio.to_thread.run_sync(self._sync_session.close)


class AsyncSessionmaker:
    """
    Factory for creating AsyncSession instances.
    
    Similar to SQLAlchemy's sessionmaker but for async sessions.
    """
    
    def __init__(
        self,
        bind: Optional[AsyncEngine] = None,
        class_: Type[Session] = Session,
        **kwargs
    ):
        """
        Initialize AsyncSessionmaker.
        
        Args:
            bind: Optional AsyncEngine to bind sessions to
            class_: Session class to use
            **kwargs: Additional arguments passed to sessionmaker
        """
        self._bind = bind
        self._sync_sessionmaker = sessionmaker(
            bind=bind.sync_engine if bind else None,
            class_=class_,
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
        # Create synchronous session in thread pool
        sync_session = await anyio.to_thread.run_sync(self._sync_sessionmaker)
        
        async_session = AsyncSession(sync_session)
        try:
            yield async_session
        except Exception:
            await async_session.rollback()
            raise
        finally:
            await async_session.close()
    
    @asynccontextmanager
    async def begin(self) -> AsyncIterator[AsyncSession]:
        """
        Create a session with automatic transaction management.
        
        Usage:
            async with sessionmaker.begin() as session:
                await session.execute(query)
                # Transaction is automatically committed
        """
        async with self() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise


def create_async_engine(url: str, **kwargs) -> AsyncEngine:
    """
    Create an AsyncEngine instance.
    
    Args:
        url: Database URL (can use async drivers like aiosqlite)
        **kwargs: Additional arguments passed to create_engine
        
    Returns:
        AsyncEngine instance
    
    Example:
        engine = create_async_engine("sqlite+aiosqlite:///./test.db")
    """
    # For async drivers, we need to use the sync version
    # anyio handles the async execution
    if "+aiosqlite" in url:
        # Convert aiosqlite URL to standard sqlite
        # Since we're using thread pool, we use sync sqlite
        url = url.replace("+aiosqlite", "")
        # Add poolclass to avoid threading issues with sqlite
        kwargs.setdefault("poolclass", NullPool)
    
    sync_engine = create_engine(url, **kwargs)
    return AsyncEngine(sync_engine)
