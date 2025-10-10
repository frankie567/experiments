# uvloop Updated Benchmark

This experiment runs the uvloop benchmark on Python 3.13 to see how uvloop performance compares to the built-in asyncio event loop in the latest Python version.

## Overview

[uvloop](https://github.com/MagicStack/uvloop) is a drop-in replacement for Python's asyncio event loop, built on top of libuv (the same library that powers Node.js). According to their documentation, uvloop makes asyncio 2-4x faster.

However, the benchmark results shown in their README are from older Python versions. This experiment re-runs their echo server benchmark on Python 3.13 to see if recent asyncio improvements have reduced the performance gap.

## Test Scenario

The benchmark implements an echo server that receives messages and sends them back to clients. Three different implementations are tested:

1. **sockets**: Using `loop.sock_recv()` and `loop.sock_sendall()` methods
2. **streams**: Using asyncio high-level streams created by `asyncio.start_server()`
3. **protocol**: Using `loop.create_server()` with a simple echo protocol

Each implementation is tested with both:
- Standard asyncio event loop
- uvloop event loop

## Methodology

- Uses the original uvloop benchmark code from their repository
- Tests with multiple message sizes (1KB, 10KB, 100KB)
- Runs multiple workers in parallel to simulate real-world load
- Measures requests per second for each configuration

## Running the Benchmark

```bash
# Install dependencies
uv sync

# Run the benchmark
uv run benchmark.py
```

## Dependencies

- `uvloop`: Fast event loop implementation
- Standard library: `asyncio`, `socket`, `concurrent.futures`

## Results

### Key Findings on Python 3.13.7

The benchmark reveals interesting results that differ from older uvloop benchmarks:

**1. Sockets Mode (sock_recv/sock_sendall):**
- asyncio is actually **faster** than uvloop by 1.35-1.52x
- This is a surprising reversal from older benchmarks
- Suggests Python 3.13 has significantly improved low-level socket operations

| Message Size | asyncio (req/s) | uvloop (req/s) | Speedup |
|--------------|-----------------|----------------|---------|
| 1KB          | 21,041          | 13,854         | 0.66x   |
| 10KB         | 17,564          | 13,009         | 0.74x   |
| 100KB        | 9,601           | 6,751          | 0.70x   |

**2. Streams Mode (asyncio.start_server):**
- uvloop is **2.15-2.23x faster** than asyncio
- Consistent with historical uvloop advantages
- Shows uvloop still excels with high-level stream APIs

| Message Size | asyncio (req/s) | uvloop (req/s) | Speedup |
|--------------|-----------------|----------------|---------|
| 1KB          | 15,477          | 34,462         | 2.23x   |
| 10KB         | 13,889          | 29,883         | 2.15x   |
| 100KB        | 7,176           | 15,523         | 2.16x   |

**3. Protocol Mode (loop.create_server):**
- uvloop is **2.10-2.37x faster** than asyncio
- Similar performance gain as streams mode
- Protocol-based servers benefit significantly from uvloop

| Message Size | asyncio (req/s) | uvloop (req/s) | Speedup |
|--------------|-----------------|----------------|---------|
| 1KB          | 24,249          | 50,874         | 2.10x   |
| 10KB         | 18,575          | 44,018         | 2.37x   |
| 100KB        | 8,681           | 19,886         | 2.29x   |

**Overall Performance:**
- Average across all tests: uvloop is **1.68x faster** than asyncio
- However, this varies significantly by API used
- Some workloads (low-level sockets) now favor asyncio in Python 3.13

### Analysis

These results suggest that **Python 3.13's asyncio improvements have been significant**, particularly for low-level socket operations. The built-in asyncio event loop now performs better than uvloop when using `sock_recv()` and `sock_sendall()` methods.

However, uvloop still provides substantial benefits (2-2.4x faster) when using higher-level APIs like streams and protocols, which are more common in real-world applications.

### Comparison to Historical uvloop Benchmarks

According to uvloop's original benchmarks (from ~2016-2018), uvloop was **2-4x faster** than asyncio across all modes. Our Python 3.13 results show:

- **Sockets mode**: uvloop is now **slower** than asyncio (0.66-0.74x) - a complete reversal!
- **Streams mode**: uvloop maintains ~2.2x advantage (similar to historical results)
- **Protocol mode**: uvloop maintains ~2.3x advantage (similar to historical results)

This indicates that Python core team has made significant optimizations to asyncio, especially in low-level socket operations, narrowing the performance gap considerably.

### Recommendations

- For **new projects on Python 3.13+**: Consider whether you're using high-level (streams/protocols) or low-level (sockets) APIs
- For **high-level async APIs** (streams, protocols): uvloop still provides 2-2.4x performance improvement
- For **low-level socket operations**: Python 3.13's built-in asyncio may now be the better choice
- For **maximum portability**: Stick with asyncio; Python 3.13 has narrowed the gap significantly

See `benchmark_results.txt` for the complete results on Python 3.13.

## Files

- `benchmark.py` - Main benchmark orchestration script
- `echoserver.py` - Echo server implementation (from uvloop examples)
- `echoclient.py` - Echo client implementation (from uvloop examples)
- `benchmark_results.txt` - Performance results
