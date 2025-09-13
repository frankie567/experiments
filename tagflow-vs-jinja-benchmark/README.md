# Tagflow vs Jinja Performance Benchmark

This experiment compares the performance of [tagflow](https://github.com/lessrest/tagflow) and [Jinja2](https://jinja.palletsprojects.com/en/stable/) for HTML generation.

## Overview

Tagflow is a Python library that allows writing HTML documents using context managers syntax, providing a more programmatic approach to HTML generation. Jinja2 is a traditional templating engine that uses template files with placeholders.

This benchmark evaluates:
- **HTML generation speed** for various scenarios
- **Memory usage** during HTML generation
- **Code complexity** and readability

## Test Scenarios

1. **Simple HTML Page**: Basic HTML structure with minimal content
2. **Complex HTML Page**: Rich HTML with nested elements, attributes, and dynamic content
3. **Repeated Elements**: Generating lists/tables with many repeated elements
4. **Large Document**: Generating a substantial HTML document

## Running the Benchmark

```bash
uv run benchmark.py
```

## Dependencies

- `tagflow`: For programmatic HTML generation using context managers
- `jinja2`: For template-based HTML generation
- `memory-profiler`: For memory usage analysis

## Results

### Key Findings

Based on 1000 iterations per test with 10 warmup runs:

**Tagflow excels at:**
- ✅ **Simple HTML generation** - 5.00x faster than Jinja2 (0.164ms vs 0.820ms)
- ✅ **Complex nested structures** - 2.83x faster than Jinja2 (0.917ms vs 2.593ms)
- ✅ **Low memory footprint** - Consistent ~47-50MB memory usage

**Jinja2 excels at:**
- ✅ **Repetitive content generation** - 3.32x faster than Tagflow for data tables (2.138ms vs 7.103ms)
- ✅ **Template-based workflows** - Better for scenarios with lots of repeated elements

### Performance Summary

| Scenario | Tagflow (ms) | Jinja2 (ms) | Winner | Ratio |
|----------|--------------|-------------|---------|-------|
| Simple Page | 0.164 | 0.820 | **Tagflow** | 5.00x |
| Complex Page | 0.917 | 2.593 | **Tagflow** | 2.83x |
| Data Table (100 rows) | 7.103 | 2.138 | **Jinja2** | 3.32x |

**Overall Average:** Jinja2 is 1.47x faster across all scenarios (1.851ms vs 2.728ms)

### Analysis

- **Tagflow's context manager approach** provides significant performance benefits for structured HTML with moderate complexity
- **Jinja2's template compilation** makes it more efficient for generating repetitive content like tables and lists
- **Memory usage** is comparable between both libraries (~47-50MB)
- **Use case matters**: Choose Tagflow for structured pages, Jinja2 for data-heavy templates

### Running the Benchmark

```bash
# Quick benchmark
uv run benchmark.py

# Full benchmark with results saved to file
uv run run_benchmark.py
```

Results are automatically saved to timestamped files (`benchmark_results_YYYYMMDD_HHMMSS.txt`).

## Implementation Notes

Both libraries are tested using equivalent HTML output to ensure fair comparison. The benchmark includes:
- 10 warmup iterations to eliminate cold start effects
- 1000 test iterations for statistical significance 
- Memory usage profiling using `memory-profiler`
- Statistical analysis (mean, std dev, min/max times)