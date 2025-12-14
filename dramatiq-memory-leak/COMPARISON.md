# Memory Leak Comparison: Original vs Fixed Middleware

This document provides a side-by-side comparison of the memory behavior between the original Dramatiq AsyncIO middleware and our fixed implementation.

## Test Scenario

Both tests run the same task:
- Allocate 128 MB of memory
- Raise an exception containing that data
- Configure for 1,000,000 retries with 100ms max backoff
- Log memory usage before and after allocation

## Results Summary

| Metric | Original Middleware | Fixed Middleware | Improvement |
|--------|-------------------|------------------|-------------|
| **Min Memory** | 37.58 MB | 28.21 MB | - |
| **Max Memory** | 4902.49 MB | 157.02 MB | **31x reduction** |
| **Mean Memory** | 2305.73 MB | 92.86 MB | **25x reduction** |
| **Memory Growth** | 4864.91 MB | 128.81 MB | **38x reduction** |
| **Duration** | 30.46 seconds | 45.64 seconds | - |
| **Behavior** | ❌ Continuous accumulation | ✅ Stable oscillation |

## Visual Comparison

### Original Middleware (BROKEN)

![Original Middleware Memory Leak](./memory_usage_exception.png)

**Pattern**: Exponential growth
- Memory starts at 37 MB
- Grows linearly with each retry  
- Reaches 4.9 GB after 30 seconds
- Would continue growing indefinitely
- Each retry adds 128 MB that's never freed

**Diagnostic**: This is a classic memory leak pattern where resources are allocated but never released.

### Fixed Middleware (WORKING)

![Fixed Middleware Memory Behavior](./memory_usage_fixed.png)

**Pattern**: Stable oscillation
- Memory oscillates between 29 MB and 157 MB
- After each retry, memory returns to baseline
- No accumulation over time
- Indefinite runtime would maintain this pattern

**Diagnostic**: This is the expected behavior - memory spikes temporarily during allocation then is properly freed.

## Key Findings

### The Problem

The original AsyncIO middleware retains exception objects in the event loop context. When exceptions contain large data:

1. Task allocates 128 MB → memory spikes to 165 MB
2. Exception is raised with reference to the data
3. Exception is caught by middleware but reference is retained
4. Task is scheduled for retry
5. **Memory is NOT released**
6. Repeat for each retry → continuous growth

### The Solution

The fixed middleware explicitly cleans up exception references:

1. Task allocates 128 MB → memory spikes to 157 MB
2. Exception is captured in a temporary container
3. Exception is re-raised for proper error handling  
4. **Exception references are explicitly cleared**
5. **Garbage collection is triggered**
6. Task is scheduled for retry
7. **Memory is released** → back to 29 MB baseline
8. Repeat maintains stable memory usage

## Code Comparison

### Original (Leaks)

```python
# In EventLoopThread.run_coroutine()
async def wrapped_coro() -> R:
    try:
        return await coro  # Exception escapes here
    finally:
        done.set()

future = asyncio.run_coroutine_threadsafe(wrapped_coro(), self.loop)
return future.result(timeout=self.interrupt_check_ival)
# Exception still referenced by future/loop internals
```

### Fixed (Clean)

```python
# In FixedEventLoopThread.run_coroutine()
async def wrapped_coro() -> None:
    try:
        result = await coro
        result_container.append(result)
    except BaseException as e:
        # Capture exception separately
        exception_container.append((type(e), e, e.__traceback__))
    finally:
        done.set()

# ... wait for completion ...

if exception_container:
    exc_type, exc_value, exc_tb = exception_container[0]
    exception_container.clear()  # Release container
    
    try:
        raise exc_value.with_traceback(exc_tb)
    finally:
        # Explicitly clear all references
        exc_type = None
        exc_value = None  
        exc_tb = None
        gc.collect()  # Force cleanup
```

## Impact Assessment

### For Production Systems

The memory leak would cause:
- **Worker crashes** due to OOM (Out of Memory)
- **System instability** affecting other processes
- **Increased infrastructure costs** to handle memory bloat
- **Reduced throughput** as GC struggles with large heaps

Example impact:
- Task with 10 MB data + 100 retries = **1 GB leak**
- Task with 50 MB data + 50 retries = **2.5 GB leak**
- Multiple concurrent tasks = **multiplied impact**

### After Fix

- Memory usage is **predictable** and **bounded**
- Workers can run **indefinitely** without memory issues
- **Better resource utilization** across the system
- **No unexpected OOM failures**

## Testing Methodology

Both tests used:
- Python 3.13.11
- Dramatiq 2.0.0
- Redis as message broker
- psutil for memory measurements
- 1 worker process, 1 thread
- Identical task configuration

Memory measurements taken via `psutil.Process().memory_info().rss` at key points in task execution.

## Conclusion

The fixed AsyncIO middleware completely resolves the memory leak issue through proper exception reference management and forced garbage collection. The solution is a drop-in replacement that requires no changes to user code.

**Recommendation**: Use `FixedAsyncIO` instead of the standard `AsyncIO` middleware when:
- Tasks may raise exceptions during retries
- Exceptions might contain or reference large data
- High retry counts are configured
- Long-running workers are deployed
