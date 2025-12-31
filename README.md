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

Investigation and **solution** for memory leak issues in [Dramatiq](https://github.com/Bogdanp/dramatiq) task processing library's AsyncIO middleware. **Problem identified**: Tasks that raise exceptions containing large data objects exhibit severe memory leaks - memory accumulates with each retry, growing from 37 MB to 4.9 GB in 30 seconds (130x growth). **Nested exceptions are 2× worse** - reaching 9.3 GB due to exception chaining. **Solution implemented**: A fixed AsyncIO middleware (`FixedAsyncIO`) that properly cleans up exception references through explicit cleanup and forced garbage collection, reducing max memory from 4.9 GB to just 157 MB (31x improvement). Includes complete test scripts for multiple scenarios using `uv` inline dependencies, memory profiling, visual comparisons, and a drop-in replacement middleware that resolves the issue without requiring code changes.

### [movie-duration-by-year](./movie-duration-by-year/)

Analysis of movie duration evolution from 1930 to present using the [IMDB API](https://imdbapi.dev/). Fetches data for 67,514 movies across 96 years and generates visualizations showing how average movie runtimes have changed over time. **Key findings**: Average duration increased from **84.6 minutes in the 1930s to 109.1 minutes in the 2020s** (29% increase). The 1930s had the shortest movies (averaging 84.6 min), while 2025 shows the longest average at 116.0 minutes. Includes year-by-year and decade-by-decade analysis with dual-axis plots showing both average duration trends and the exponential growth in movie production volume.
