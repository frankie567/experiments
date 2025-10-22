# Code Structure

This document provides an overview of the code organization and key components.

## File Overview

| File | Lines | Purpose |
|------|-------|---------|
| `async_sqlalchemy.py` | 497 | Core implementation of async wrapper classes |
| `test_basic.py` | 208 | Basic Core SQL tests |
| `test_orm.py` | 303 | ORM usage tests |
| `example.py` | 244 | Comprehensive usage examples |
| `README.md` | 55 | Project overview and getting started |
| `SUMMARY.md` | 94 | Executive summary of findings |
| `COMPARISON.md` | 137 | Comparison with official extension |

## Core Implementation (`async_sqlalchemy.py`)

### Main Classes

1. **AsyncEngine** (~70 lines)
   - Wraps sync SQLAlchemy Engine
   - Provides async connection management
   - Uses thread pool for all operations

2. **AsyncConnection** (~100 lines)
   - Wraps sync Connection
   - Async execute, commit, rollback methods
   - Transaction context managers

3. **AsyncSession** (~150 lines)
   - Wraps sync ORM Session
   - Async ORM operations (add, delete, query)
   - Session lifecycle management

4. **AsyncResult** (~70 lines)
   - Wraps result sets
   - Async fetchone, fetchall, scalar methods
   - Result iteration support

5. **AsyncScalars** (~30 lines)
   - Handles scalar result iteration
   - Async all, first, one methods

6. **AsyncSessionmaker** (~70 lines)
   - Factory for AsyncSession
   - Async context manager support
   - Automatic transaction management

### Key Design Pattern

All async methods follow the same pattern:

```python
async def method(self, *args, **kwargs):
    return await anyio.to_thread.run_sync(
        functools.partial(self._sync_object.method, *args, **kwargs)
    )
```

This simple pattern:
- Executes sync SQLAlchemy code in a thread pool
- Returns results to the async context
- No greenlets or complex context switching

## Test Coverage

### `test_basic.py` - Core SQL Tests
- Table creation and schema management
- CRUD operations (insert, select, update, delete)
- Transaction management and rollback
- Scalar queries and result handling

### `test_orm.py` - ORM Tests
- Model definition with declarative base
- Session lifecycle and context managers
- ORM queries (select, filter, order)
- Entity operations (add, update, delete, get)
- Transaction control and rollback
- Bulk operations

## Usage Examples

### `example.py` - Comprehensive Examples

1. **Core Usage**
   - Engine creation
   - Connection management
   - Basic queries

2. **ORM Usage**
   - Session creation
   - Model operations
   - Queries with ORM

3. **Transaction Management**
   - Automatic commit on success
   - Automatic rollback on error
   - Manual transaction control

## Dependencies

- `sqlalchemy>=2.0.0` - Core database toolkit
- `anyio>=4.0.0` - Backend-agnostic async library
- `aiosqlite>=0.20.0` - Async SQLite driver (for testing)

## Architecture Diagram

```
┌─────────────────────────────────────────┐
│          User's Async Code              │
└──────────────┬──────────────────────────┘
               │ await
               │
┌──────────────▼──────────────────────────┐
│      Async Wrapper Classes              │
│  (AsyncEngine, AsyncSession, etc.)      │
└──────────────┬──────────────────────────┘
               │ anyio.to_thread.run_sync()
               │
┌──────────────▼──────────────────────────┐
│         Worker Thread Pool              │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│      Sync SQLAlchemy Objects            │
│   (Engine, Session, Connection)         │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│           Database                      │
└─────────────────────────────────────────┘
```

## Key Differences from Official Extension

| Aspect | Official | This Implementation |
|--------|----------|---------------------|
| Async Strategy | Greenlet context switching | Thread pool execution |
| Complexity | High (greenlet magic) | Low (simple wrappers) |
| Dependencies | greenlet required | Standard threading only |
| Free-threading | Uncertain | Ready |
| Backend Support | asyncio only | anyio-compatible backends |

## Performance Characteristics

- **Overhead**: Each async call involves thread switching
- **Throughput**: Lower than greenlet-based approach
- **Simplicity**: Much easier to understand and debug
- **Compatibility**: Better future compatibility

## Future Enhancements

Potential improvements:
- [ ] Batch operations optimization
- [ ] Connection pool tuning
- [ ] Performance benchmarking
- [ ] Support for async database drivers
- [ ] Event system integration
- [ ] Streaming result sets
