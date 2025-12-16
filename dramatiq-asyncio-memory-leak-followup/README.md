# Dramatiq AsyncIO Memory Leak Follow-up

This experiment provides a clean, PR-ready demonstration and detailed explanation of the memory leak bug discovered in Dramatiq's AsyncIO middleware and the proposed fix.

## Purpose

Following the investigation in the [dramatiq-memory-leak](../dramatiq-memory-leak/) experiment, this follow-up provides:

1. **Unit tests** demonstrating the buggy behavior
2. **Unit tests** proving the fix works
3. **Detailed technical explanation** of why the problem occurs and how the fix resolves it

This is designed as a clean package that can be proposed upstream to the Dramatiq project.

## Structure

- `test_memory_leak.py` - Unit tests demonstrating the memory leak with the original AsyncIO middleware
- `test_fixed_middleware.py` - Unit tests proving the fix works
- `fixed_asyncio_middleware.py` - The proposed fix (copied from parent experiment)
- `TECHNICAL_EXPLANATION.md` - Detailed explanation of the root cause and solution
- `pyproject.toml` - Python project configuration and dependencies

## The Problem

The Dramatiq AsyncIO middleware exhibits a critical memory leak when tasks raise exceptions containing large data objects. Memory accumulates linearly with each retry:

- **Symptom**: Memory grows from ~40 MB to 5 GB in 30 seconds
- **Impact**: 130x memory growth with high retry counts
- **Root Cause**: Exception objects are retained in asyncio event loop context and never released

## The Solution

The `FixedAsyncIO` middleware implements proper exception cleanup through:

1. Exception capture in a container (breaks reference chain)
2. Explicit reference clearing after re-raising
3. Forced garbage collection
4. Proper future object cleanup

This reduces max memory from 4.9 GB to just 157 MB (31x improvement).

## Running the Tests

All tests use `uv` inline script dependencies and can be run directly:

```bash
# Test demonstrating the bug (requires Redis)
uv run test_memory_leak.py

# Test proving the fix works (requires Redis)
uv run test_fixed_middleware.py
```

Both tests require a Redis server running on `localhost:6379`. You can start one with Docker:

```bash
docker run -d -p 6379:6379 redis:latest
```

## Expected Test Output

### test_memory_leak.py

This test demonstrates the memory leak with the original AsyncIO middleware:

- Creates a task that raises an exception with a 64 MB payload
- Retries the task 5 times
- Measures memory growth
- **Expected**: Memory should grow by approximately 320 MB (64 MB × 5 retries)
- **Result**: FAIL - demonstrates the bug

### test_fixed_middleware.py

This test proves the fix works:

- Uses the FixedAsyncIO middleware
- Same task and retry behavior
- **Expected**: Memory should stay relatively stable (single allocation only)
- **Result**: PASS - memory leak is fixed

## Technical Details

See [TECHNICAL_EXPLANATION.md](./TECHNICAL_EXPLANATION.md) for a comprehensive analysis of:

- Why the memory leak occurs (asyncio internals, exception context, traceback chains)
- How the fix addresses each source of memory retention
- Python garbage collection considerations
- Implementation details and tradeoffs

## Important Limitations

The `FixedAsyncIO` middleware has some limitations to be aware of:

1. **Global State Modification**: The middleware sets a global event loop thread in both its own module and the original `dramatiq.asyncio` module. This is necessary for actor decorators to work but means:
   - Do not use both `AsyncIO` and `FixedAsyncIO` in the same application
   - Multiple broker instances with different middleware configurations may conflict

2. **Sensitive Data in Exceptions**: The fix temporarily stores exception objects with their tracebacks, which contain local variables from all stack frames. While this is necessary to re-raise exceptions correctly, be mindful of:
   - Avoid storing passwords or secrets in local variables when raising exceptions
   - The data is cleared immediately after re-raising, but exists briefly in memory

These are inherent to how the fix works and would need to be addressed in any upstream implementation.

## Files

- `README.md` - This file
- `test_memory_leak.py` - Demonstrates the bug
- `test_fixed_middleware.py` - Proves the fix
- `fixed_asyncio_middleware.py` - Proposed fix implementation
- `TECHNICAL_EXPLANATION.md` - Detailed technical analysis
- `pyproject.toml` - Project configuration

## For Upstream Contribution

This experiment is structured to facilitate an upstream PR to Dramatiq:

1. The tests clearly demonstrate the problem and solution
2. The technical explanation provides context for reviewers
3. The fix is a drop-in replacement for the existing middleware
4. All code follows Dramatiq's style and patterns

## Related Work

This builds on the original investigation in [dramatiq-memory-leak](../dramatiq-memory-leak/) which includes:

- Comprehensive memory profiling with visualizations
- Multiple test scenarios (nested exceptions, concurrent tasks, etc.)
- Detailed findings and analysis
- Production recommendations
