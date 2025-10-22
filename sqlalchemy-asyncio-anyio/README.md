# SQLAlchemy Asyncio Reimplementation with anyio

This experiment explores a reimplementation of SQLAlchemy's asyncio extension using [anyio](https://github.com/agronholm/anyio) instead of gevent.

## Overview

SQLAlchemy's current asyncio extension (https://github.com/sqlalchemy/sqlalchemy/tree/main/lib/sqlalchemy/ext/asyncio) is implemented using gevent for managing async operations. With Python 3.14 and free-threading on the horizon, it's unclear if gevent will support free-threading.

This experiment reimplements the asyncio extension using anyio, which provides a backend-agnostic async API that works with asyncio, trio, and other async frameworks.

## Goals

- Maintain the same public API as SQLAlchemy's asyncio extension
- Replace gevent-based async operations with anyio
- Test with SQLite and aiosqlite driver
- Demonstrate basic CRUD operations work correctly

## Key Components

The reimplementation provides:

1. **AsyncEngine**: Wraps a synchronous SQLAlchemy engine and executes operations in a thread pool using anyio
2. **AsyncConnection**: Provides async context manager for database connections
3. **AsyncSession**: Provides async ORM session functionality
4. **AsyncResult**: Wraps result sets for async iteration

## Running the Tests

```bash
# Install dependencies
uv sync

# Run basic tests
uv run test_basic.py

# Run ORM tests
uv run test_orm.py
```

## Implementation Notes

- Uses `anyio.to_thread.run_sync()` to run synchronous SQLAlchemy operations in worker threads
- Maintains compatibility with SQLAlchemy's existing API
- Provides async context managers for proper resource cleanup
- Supports both Core and ORM usage patterns

## Dependencies

- `sqlalchemy`: Core SQLAlchemy library
- `anyio`: Backend-agnostic async library
- `aiosqlite`: Async SQLite driver for testing

## Results

The reimplementation successfully provides an async API for SQLAlchemy using anyio instead of gevent, demonstrating that it's possible to build the asyncio extension without relying on gevent's greenlet-based concurrency.
