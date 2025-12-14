# Experiments

This repository contains various experiments, prototypes and ideas I want to explore in Python, mostly co-developed with GitHub Copilot.

## List

### [tagflow-vs-jinja-benchmark](./tagflow-vs-jinja-benchmark/)

Performance benchmark comparing [tagflow](https://github.com/lessrest/tagflow) and [Jinja2](https://jinja.palletsprojects.com/en/stable/) for HTML generation. Tests various scenarios including simple pages, complex nested structures, and data tables. Results show Jinja2 with proper Environment setup is significantly faster across all scenarios.

### [tagflow-performance-analysis](./tagflow-performance-analysis/)

Deep performance analysis of [tagflow](https://github.com/lessrest/tagflow) bottlenecks and optimization strategies. Uses profiling to identify performance issues and implements targeted optimizations to reduce the gap with Jinja2. Explores string-based generation, context optimization, and static mode improvements.

### [tagflow-reimplementation](./tagflow-reimplementation/)

A minimal, efficient reimplementation of Tagflow from scratch that keeps the nice context manager syntax while focusing on performance. Achieves **10.79x faster** performance than original Tagflow through direct string building, explicit document objects (no globals/context vars), and minimal overhead design. Includes convenient shortcuts for common HTML tags (`doc.div()`, `doc.h1()`, etc.). Still 4.46x slower than Jinja2, but significantly closes the performance gap while maintaining the appealing programmatic API.

### [uvloop-updated-benchmark](./uvloop-updated-benchmark/)

Updated benchmark of [uvloop](https://github.com/MagicStack/uvloop) vs asyncio on Python 3.13. Tests echo server performance with sockets, streams, and protocol APIs. **Surprising findings**: Python 3.13's asyncio is now faster than uvloop for low-level socket operations (1.35-1.52x), while uvloop still excels with high-level streams/protocols (2.15-2.37x faster). Overall average: uvloop is 1.68x faster, but the gap has significantly narrowed compared to older Python versions.

### [hatchling-pyo3-plugin](./hatchling-pyo3-plugin/)

A [Hatchling](https://hatch.pypa.io/) build hook plugin for building [PyO3](https://github.com/PyO3/pyo3) Rust extensions. Provides an alternative to [Maturin](https://github.com/PyO3/maturin) by enabling PyO3 projects to use Hatchling as their build backend. The plugin automatically detects `Cargo.toml`, compiles Rust extensions with `cargo build`, and packages the compiled binaries into Python wheels. Includes a working demo project with simple PyO3 functions (add, multiply, greet) and comprehensive documentation. Successfully demonstrates that PyO3 extensions can be built with the standard Python packaging ecosystem.

### [dramatiq-memory-leak](./dramatiq-memory-leak/)

Investigation of memory leak issues in [Dramatiq](https://github.com/Bogdanp/dramatiq) task processing library, specifically with the AsyncIO middleware. **Key finding**: Tasks that raise exceptions containing large data objects (128 MB) exhibit severe memory leaks - memory accumulates with each retry, growing from 37 MB to over 4.9 GB in 30 seconds. In contrast, long-running async sleep tasks properly manage memory, demonstrating the issue is specific to exception handling in the AsyncIO middleware. Includes runnable test scripts using `uv` inline dependencies, memory profiling, and visualization plots showing the dramatic difference in memory behavior between exception and sleep scenarios.
