# Experiments

This repository contains various experiments, prototypes and ideas I want to explore in Python, mostly co-developed with GitHub Copilot.

## List

### [tagflow-vs-jinja-benchmark](./tagflow-vs-jinja-benchmark/)

Performance benchmark comparing [tagflow](https://github.com/lessrest/tagflow) and [Jinja2](https://jinja.palletsprojects.com/en/stable/) for HTML generation. Tests various scenarios including simple pages, complex nested structures, and data tables. Results show Jinja2 with proper Environment setup is significantly faster across all scenarios.

### [tagflow-performance-analysis](./tagflow-performance-analysis/)

Deep performance analysis of [tagflow](https://github.com/lessrest/tagflow) bottlenecks and optimization strategies. Uses profiling to identify performance issues and implements targeted optimizations to reduce the gap with Jinja2. Explores string-based generation, context optimization, and static mode improvements.
