# Dramatiq Memory Leak Investigation

This experiment investigates potential memory leak issues with [Dramatiq](https://github.com/Bogdanp/dramatiq), a Python distributed task processing library.

## Background

We're investigating memory leak behavior in Dramatiq, particularly:
- Issues with AsyncIO middleware and exceptions that hold large data
- Memory behavior during long-running async tasks

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

### `plot_memory.py`

Generates visualization of memory usage from the CSV files produced by the test scripts.

**Usage:**
```bash
./plot_memory.py
```

This will generate:
- `memory_usage_exception.png` - Plot of memory usage for the exception test
- `memory_usage_sleep.png` - Plot of memory usage for the sleep test

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
