# SQLAlchemy Asyncio with Anyio

This experiment demonstrates how to use SQLAlchemy's asyncio extension with [anyio](https://github.com/agronholm/anyio) for backend-agnostic async support.

## Overview

SQLAlchemy's asyncio extension uses async database drivers like `aiosqlite` and `asyncpg` directly - it doesn't run sync code in threads. However, it's currently tied to asyncio and uses greenlet for bridging sync-style APIs with async drivers.

This implementation wraps SQLAlchemy's official asyncio extension with anyio, providing:
- **Backend flexibility**: Works with asyncio, trio, and other anyio-supported backends
- **Async driver usage**: Uses async drivers (aiosqlite, asyncpg, etc.) directly - no thread pool
- **API compatibility**: Maintains the same async API as SQLAlchemy's extension

## How It Works

This implementation is a thin wrapper around SQLAlchemy's official AsyncEngine and AsyncSession:

```
User Code (anyio-compatible)
       ↓
Our Wrapper Classes (AsyncEngine, AsyncSession, etc.)
       ↓
SQLAlchemy's AsyncEngine/AsyncSession (greenlet-based)
       ↓
Async Database Drivers (aiosqlite, asyncpg, etc.)
       ↓
Database
```

### Key Insight

SQLAlchemy's asyncio extension DOES use async drivers directly. Greenlet is used to bridge the sync-style SQLAlchemy API with async database operations, not to run sync code in threads.

Our wrapper provides anyio compatibility on top of this, allowing the same code to work with different async backends (asyncio, trio, etc.) through anyio.

## Goals

- ✅ Use async database drivers (aiosqlite, asyncpg) directly
- ✅ Provide anyio-compatible async API
- ✅ Support multiple async backends (asyncio, trio)
- ✅ Maintain API compatibility with SQLAlchemy's extension

## Running the Tests

```bash
# Install dependencies
uv sync

# Run basic tests
uv run test_basic.py

# Run ORM tests
uv run test_orm.py

# Run examples
uv run example.py
```

## Implementation Notes

- Wraps SQLAlchemy's `AsyncEngine`, `AsyncSession`, etc.
- All async database operations use the underlying async drivers
- Greenlet is still used (via SQLAlchemy's extension) for API bridging
- Anyio provides backend flexibility on top of SQLAlchemy's async support

## Dependencies

- `sqlalchemy>=2.0.0`: Core SQLAlchemy library (includes async extension)
- `anyio>=4.0.0`: Backend-agnostic async library
- `aiosqlite>=0.20.0`: Async SQLite driver

## Results

This wrapper successfully provides anyio-compatible access to SQLAlchemy's async functionality, which uses async database drivers directly. The implementation demonstrates that you can add backend flexibility (anyio) on top of SQLAlchemy's asyncio extension without sacrificing the use of async drivers.
