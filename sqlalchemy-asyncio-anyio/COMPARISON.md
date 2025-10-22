# Implementation Comparison

This document compares SQLAlchemy's official asyncio extension (using gevent/greenlet) with our anyio-based reimplementation.

## Architecture Differences

### Official SQLAlchemy asyncio Extension

The official extension uses:
- **greenlet** for lightweight cooperative concurrency
- **gevent** (optional) for additional async capabilities
- Context switching between sync and async code using greenlets
- Proxy objects that switch contexts when awaited

Key characteristics:
- Tightly coupled with greenlet's implementation
- Uses greenlet context switching to run sync code "as if" it were async
- Complex proxy system to bridge sync/async worlds
- Dependency on greenlet which may have challenges with Python 3.14's free-threading

### Anyio-based Reimplementation

Our implementation uses:
- **anyio** for backend-agnostic async operations
- **Thread pool execution** via `anyio.to_thread.run_sync()`
- Simple wrapper classes around sync SQLAlchemy objects
- No greenlets or context switching

Key characteristics:
- Simple and straightforward architecture
- Runs sync SQLAlchemy code in worker threads
- Compatible with anyio's multiple backends (asyncio, trio)
- Ready for Python 3.14's free-threading (no greenlet dependency)
- More explicit about when thread switching occurs

## API Compatibility

Our implementation maintains API compatibility with the official extension for common patterns:

```python
# Both implementations support the same API patterns:

# Creating engines
engine = create_async_engine("sqlite+aiosqlite:///./test.db")

# Using connections
async with engine.connect() as conn:
    result = await conn.execute(select(users))
    rows = await result.fetchall()

# Using sessions
async with async_session() as session:
    result = await session.execute(select(User))
    users = await (await result.scalars()).all()

# Transaction management
async with engine.begin() as conn:
    await conn.execute(insert(users).values(...))
```

## Performance Considerations

### Official Extension
- Lower overhead due to greenlet context switching
- No actual thread switching for most operations
- Better CPU efficiency for I/O-bound operations
- Lower memory footprint

### Anyio Implementation
- Higher overhead due to thread pool execution
- Each database operation involves thread switching
- More suitable for truly concurrent workloads
- Better isolation between operations
- More compatible with CPU-bound tasks

## Free-Threading Readiness

### Official Extension
- **Uncertain** - Depends on greenlet's free-threading support
- As of October 2024, greenlet's free-threading compatibility is unclear
- May require significant refactoring for Python 3.14+

### Anyio Implementation
- **Ready** - No greenlet dependency
- Uses standard threading which will work with free-threading
- anyio itself is actively working on free-threading support
- More future-proof architecture

## Trade-offs

### Official Extension Advantages
- ✅ Lower overhead
- ✅ Battle-tested in production
- ✅ Official support from SQLAlchemy team
- ✅ More mature ecosystem

### Official Extension Disadvantages
- ❌ Greenlet dependency unclear for free-threading
- ❌ More complex internal implementation
- ❌ Tied to specific async backends (asyncio)

### Anyio Implementation Advantages
- ✅ No greenlet dependency
- ✅ Free-threading ready
- ✅ Backend-agnostic (asyncio, trio, etc.)
- ✅ Simpler architecture
- ✅ Explicit thread boundaries

### Anyio Implementation Disadvantages
- ❌ Higher overhead per operation
- ❌ Not officially supported
- ❌ Less mature and tested
- ❌ May have edge cases not yet discovered

## Conclusion

The anyio-based reimplementation demonstrates that it's possible to build a functional async SQLAlchemy interface without relying on greenlets. While it has higher overhead, it offers better compatibility with future Python versions and clearer separation of concerns.

For production use, the official extension is still recommended. However, as Python 3.14 and free-threading become more prevalent, approaches like this anyio-based implementation may become more attractive.

## Recommendations

**Use the official extension if:**
- You need maximum performance
- You're on Python 3.13 or earlier
- You need official support and a mature ecosystem

**Consider the anyio implementation if:**
- You're preparing for Python 3.14+ free-threading
- You want backend flexibility (trio support, etc.)
- You prefer simpler, more explicit architecture
- You're building a new project with future compatibility in mind

**For Python 3.14+ projects:**
- Monitor greenlet's free-threading support progress
- Consider this anyio approach as a fallback
- Evaluate performance requirements vs. compatibility needs
