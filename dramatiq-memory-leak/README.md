# Dramatiq Memory Leak Investigation

This experiment investigates potential memory leak issues with [Dramatiq](https://github.com/Bogdanp/dramatiq), a Python distributed task processing library.

## Background

We're investigating memory leak behavior in Dramatiq, particularly:
- Issues with AsyncIO middleware and exceptions that hold large data
- Memory behavior during long-running async tasks

## Solution

**We've developed a fixed AsyncIO middleware that resolves the memory leak!** See `SOLUTION.md` for details.

The `FixedAsyncIO` middleware properly cleans up exception references, reducing max memory from 4.9 GB down to 157 MB (just the baseline + one allocation). See `fixed_asyncio_middleware.py` for the implementation.

## Additional Scenarios

We've identified and tested additional problematic scenarios:

- **Nested Exceptions**: 2× worse (9.3 GB) - exception chaining retains multiple large objects
- **Concurrent Exceptions**: Linear multiplication by task count
- **Large Results**: Tested to confirm leak is exception-specific

See `ADDITIONAL_SCENARIOS.md` for detailed analysis of each scenario.

## Scripts

### `memory_leak_exception.py`

Tests memory behavior when tasks raise exceptions containing large data objects (128 MB). The exception object may be kept in memory longer than expected due to how dramatiq handles retries and error tracking with AsyncIO middleware.

**Usage:**
```bash
./memory_leak_exception.py
```

The script will:
1. Start a worker that processes tasks
2. Each task allocates 128 MB of data
3. Raises an exception containing that data
4. Logs memory usage before allocation, after allocation, and during retries
5. Outputs memory data to `memory_usage_exception.csv`

### `memory_leak_sleep.py`

Tests memory behavior during long-running async tasks that sleep. This variation helps identify if the issue is specific to exceptions or more general to the AsyncIO middleware.

**Usage:**
```bash
./memory_leak_sleep.py
```

The script will:
1. Start a worker that processes tasks
2. Each task allocates 128 MB of data
3. Sleeps for a period using `asyncio.sleep()`
4. Logs memory usage throughout execution
5. Outputs memory data to `memory_usage_sleep.csv`

### `test_fixed_middleware.py`

Tests the FIXED AsyncIO middleware that resolves the memory leak. Same test as the exception script, but using our fixed implementation.

**Usage:**
```bash
./test_fixed_middleware.py
./run_worker_fixed.py
```

Memory is properly released after each retry - max memory stays at 157 MB instead of growing to 4.9 GB!

### `plot_memory.py`

Generates visualization of memory usage from the CSV files produced by the test scripts.

**Usage:**
```bash
./plot_memory.py
```

This will generate:
- `memory_usage_exception.png` - Plot showing the memory leak (original middleware)
- `memory_usage_sleep.png` - Plot showing normal behavior with sleep tasks
- `memory_usage_fixed.png` - Plot showing the fix works (stable memory)

## Requirements

All scripts use `uv` inline script dependencies and can be run directly:
- dramatiq
- redis
- psutil
- matplotlib (for plotting)

A Redis server must be running on `localhost:6379` for the test scripts to work.

## Running Redis

If you don't have Redis running locally, you can start it with Docker:

```bash
docker run -d -p 6379:6379 redis:latest
```

## Expected Behavior

In a healthy system:
- Memory should spike when data is allocated
- Memory should return to baseline after the task completes or fails
- Retries should not accumulate memory indefinitely

## Investigation Results

Run the scripts and examine the plots to see:
- Memory retention patterns
- Whether exceptions hold references to large objects
- How memory behaves during long-running async operations
- Whether the AsyncIO middleware properly cleans up resources
