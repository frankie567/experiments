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

**2. Streams Mode (asyncio.start_server):**
- uvloop is **2.15-2.23x faster** than asyncio
- Consistent with historical uvloop advantages
- Shows uvloop still excels with high-level stream APIs

**3. Protocol Mode (loop.create_server):**
- uvloop is **2.10-2.37x faster** than asyncio
- Similar performance gain as streams mode
- Protocol-based servers benefit significantly from uvloop

**Overall Performance:**
- Average across all tests: uvloop is **1.68x faster** than asyncio
- However, this varies significantly by API used
- Some workloads (low-level sockets) now favor asyncio in Python 3.13

### Analysis

These results suggest that **Python 3.13's asyncio improvements have been significant**, particularly for low-level socket operations. The built-in asyncio event loop now performs better than uvloop when using `sock_recv()` and `sock_sendall()` methods.

However, uvloop still provides substantial benefits (2-2.4x faster) when using higher-level APIs like streams and protocols, which are more common in real-world applications.

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
