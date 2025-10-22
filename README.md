# Experiments

This repository contains various experiments, prototypes and ideas I want to explore in Python, mostly co-developed with GitHub Copilot.

## List

### [sqlalchemy-asyncio-anyio](./sqlalchemy-asyncio-anyio/)

Reimplementation of SQLAlchemy's asyncio extension using [anyio](https://github.com/agronholm/anyio) instead of gevent/greenlet. With Python 3.14 and free-threading on the horizon, greenlet's compatibility is uncertain. This experiment demonstrates a simpler architecture using thread pools via anyio that maintains API compatibility with the official extension while being ready for free-threading. Includes comprehensive tests with SQLite/aiosqlite demonstrating both Core and ORM usage patterns work correctly.

### [tagflow-vs-jinja-benchmark](./tagflow-vs-jinja-benchmark/)

Performance benchmark comparing [tagflow](https://github.com/lessrest/tagflow) and [Jinja2](https://jinja.palletsprojects.com/en/stable/) for HTML generation. Tests various scenarios including simple pages, complex nested structures, and data tables. Results show Jinja2 with proper Environment setup is significantly faster across all scenarios.

### [tagflow-performance-analysis](./tagflow-performance-analysis/)

Deep performance analysis of [tagflow](https://github.com/lessrest/tagflow) bottlenecks and optimization strategies. Uses profiling to identify performance issues and implements targeted optimizations to reduce the gap with Jinja2. Explores string-based generation, context optimization, and static mode improvements.

### [tagflow-reimplementation](./tagflow-reimplementation/)

A minimal, efficient reimplementation of Tagflow from scratch that keeps the nice context manager syntax while focusing on performance. Achieves **10.79x faster** performance than original Tagflow through direct string building, explicit document objects (no globals/context vars), and minimal overhead design. Includes convenient shortcuts for common HTML tags (`doc.div()`, `doc.h1()`, etc.). Still 4.46x slower than Jinja2, but significantly closes the performance gap while maintaining the appealing programmatic API.

### [uvloop-updated-benchmark](./uvloop-updated-benchmark/)

Updated benchmark of [uvloop](https://github.com/MagicStack/uvloop) vs asyncio on Python 3.13. Tests echo server performance with sockets, streams, and protocol APIs. **Surprising findings**: Python 3.13's asyncio is now faster than uvloop for low-level socket operations (1.35-1.52x), while uvloop still excels with high-level streams/protocols (2.15-2.37x faster). Overall average: uvloop is 1.68x faster, but the gap has significantly narrowed compared to older Python versions.
