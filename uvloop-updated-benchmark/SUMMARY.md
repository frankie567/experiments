# uvloop vs asyncio Performance on Python 3.13 - Executive Summary

## Quick Facts

- **Python Version**: 3.13.7
- **Test Date**: October 2025
- **Benchmark Source**: uvloop official examples
- **Overall Result**: uvloop is 1.68x faster on average, but varies significantly by API

## Performance by API Type

### 🔴 Sockets API (Low-level)
**Winner: asyncio** (uvloop is 0.66-0.74x = asyncio is 1.35-1.52x faster)

This is a complete reversal from historical benchmarks where uvloop dominated.

### 🟢 Streams API (High-level)
**Winner: uvloop** (2.15-2.23x faster than asyncio)

Consistent with historical results.

### 🟢 Protocol API (High-level)
**Winner: uvloop** (2.10-2.37x faster than asyncio)

Consistent with historical results.

## What Changed?

Python 3.13's asyncio has undergone significant optimizations, particularly in low-level socket operations. The built-in event loop now outperforms uvloop for `sock_recv()` and `sock_sendall()` methods.

## Decision Guide

**Use uvloop if:**
- You're building high-level async servers using streams or protocols
- You need 2-2.4x performance boost for these workloads
- You're using older Python versions (where uvloop wins everywhere)

**Use asyncio if:**
- You're on Python 3.13+ using low-level socket operations
- You want to avoid external dependencies
- Portability and standard library usage is important

**Bottom Line:**
Python 3.13 has significantly closed the gap with uvloop. For many workloads, the built-in asyncio is now competitive or even superior, especially for low-level socket operations.
