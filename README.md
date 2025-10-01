# Experiments

This repository contains various experiments, prototypes and ideas I want to explore in Python, mostly co-developed with GitHub Copilot.

## List

### [prev-framework](./prev-framework/)

A file-system based routing web framework for Python, inspired by Next.js but fully server-side. Built on Starlette with first-class HTML template support using tagflow-inspired syntax. Create routes by simply creating directories and `route.py` files - the framework automatically discovers them and maps them to URLs. Features full type annotations, zero JavaScript, and a clean context manager API for building HTML. Example: `app/dashboard/users/route.py` automatically becomes the `/dashboard/users` route.

### [tagflow-vs-jinja-benchmark](./tagflow-vs-jinja-benchmark/)

Performance benchmark comparing [tagflow](https://github.com/lessrest/tagflow) and [Jinja2](https://jinja.palletsprojects.com/en/stable/) for HTML generation. Tests various scenarios including simple pages, complex nested structures, and data tables. Results show Jinja2 with proper Environment setup is significantly faster across all scenarios.

### [tagflow-performance-analysis](./tagflow-performance-analysis/)

Deep performance analysis of [tagflow](https://github.com/lessrest/tagflow) bottlenecks and optimization strategies. Uses profiling to identify performance issues and implements targeted optimizations to reduce the gap with Jinja2. Explores string-based generation, context optimization, and static mode improvements.

### [tagflow-reimplementation](./tagflow-reimplementation/)

A minimal, efficient reimplementation of Tagflow from scratch that keeps the nice context manager syntax while focusing on performance. Achieves **10.79x faster** performance than original Tagflow through direct string building, explicit document objects (no globals/context vars), and minimal overhead design. Includes convenient shortcuts for common HTML tags (`doc.div()`, `doc.h1()`, etc.). Still 4.46x slower than Jinja2, but significantly closes the performance gap while maintaining the appealing programmatic API.
