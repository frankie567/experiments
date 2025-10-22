# Implementation Comparison

This document compares SQLAlchemy's official asyncio extension with our anyio wrapper.

## Architecture Overview

### Official SQLAlchemy Asyncio Extension

The official extension:
- **Uses async drivers directly** (aiosqlite, asyncpg, etc.)
- **Uses greenlet** for bridging sync-style API with async operations
- **Backend-specific** (asyncio only)

Key characteristics:
- Async drivers handle all I/O
- Greenlet switches between sync API calls and async driver operations
- No thread pool for database operations
- Tied to asyncio event loop

### Anyio Wrapper (This Implementation)

Our wrapper:
- **Wraps SQLAlchemy's AsyncEngine/AsyncSession**
- **Uses async drivers directly** (via SQLAlchemy's extension)
- **Adds anyio compatibility** on top
- **Backend-agnostic** (asyncio, trio, etc.)

Key characteristics:
- Thin wrapper around official extension
- Same async driver usage as official extension
- Anyio provides backend flexibility
- Still uses greenlet (indirectly, via SQLAlchemy)

## API Comparison

Both implementations support the same async API:

```python
# Both use the same patterns:

# Creating engines
engine = create_async_engine("sqlite+aiosqlite:///./test.db")

# Using connections
async with engine.connect() as conn:
    result = await conn.execute(select(users))
    rows = result.fetchall()  # Results are already buffered

# Using sessions
async with async_session() as session:
    result = await session.execute(select(User))
    users = result.scalars().all()  # Scalars are buffered too
```

## Key Differences

| Aspect | Official Extension | Anyio Wrapper |
|--------|-------------------|---------------|
| **Async Drivers** | ✅ Yes (aiosqlite, asyncpg) | ✅ Yes (via official extension) |
| **Thread Pool** | ❌ No | ❌ No |
| **Greenlet** | ✅ Yes (for API bridging) | ✅ Yes (via SQLAlchemy) |
| **Backend Support** | asyncio only | asyncio, trio, etc. |
| **Complexity** | Moderate | Low (thin wrapper) |
| **Overhead** | Low | Slightly higher (wrapper layer) |

## Common Misconception

**MISCONCEPTION**: "SQLAlchemy's asyncio extension uses greenlet to run sync code in threads"

**REALITY**: 
- SQLAlchemy's asyncio extension uses **async drivers directly**
- Greenlet is used for **API bridging**, not threading
- No worker threads or thread pools for database I/O
- All I/O is truly async via async drivers

## How Greenlet Is Actually Used

SQLAlchemy uses greenlet to allow:
```python
# You write sync-looking code:
result = conn.execute(select(users))

# But under the hood:
# 1. Greenlet switches to async context
# 2. Async driver performs I/O: await cursor.execute(...)  
# 3. Greenlet switches back with result
# 4. You get the result synchronously
```

This is different from running sync code in threads!

## Performance Comparison

### Official Extension
- ✅ Direct async driver usage (fast)
- ✅ Low overhead (no extra layers)
- ✅ Optimal for asyncio projects

### Anyio Wrapper
- ✅ Same async driver usage (equally fast for I/O)
- ⚖️ Slight wrapper overhead (minimal impact)
- ✅ Optimal for anyio/trio projects

## When to Use Each

### Use Official Extension When:
- Building asyncio-only projects
- Need the most direct approach
- Want official support
- Performance is absolutely critical

### Use Anyio Wrapper When:
- Using trio or need backend flexibility
- Already using anyio in your project
- Want backend-agnostic code
- Slight overhead is acceptable for flexibility

## Migration Path

Moving from official extension to anyio wrapper is straightforward:

```python
# Before (official):
from sqlalchemy.ext.asyncio import create_async_engine

# After (anyio wrapper):
from async_sqlalchemy import create_async_engine

# Everything else stays the same!
```

## Conclusion

Both approaches use async drivers directly. The main difference is:
- **Official extension**: asyncio-specific
- **Anyio wrapper**: Backend-agnostic layer on top

Choose based on your async backend needs, not on perceived threading/driver differences - both use the same async drivers!
