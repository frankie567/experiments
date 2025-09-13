# Tagflow vs Jinja Performance Benchmark

This experiment compares the performance of [tagflow](https://github.com/lessrest/tagflow) and [Jinja2](https://jinja.palletsprojects.com/en/stable/) for HTML generation.

## Overview

Tagflow is a Python library that allows writing HTML documents using context managers syntax, providing a more programmatic approach to HTML generation. Jinja2 is a traditional templating engine that uses template files with placeholders.

This benchmark evaluates:
- **HTML generation speed** for various scenarios
- **Memory usage** during HTML generation  
- **Proper Jinja2 setup importance** using Environment vs Template classes

## Test Scenarios

1. **Simple HTML Page**: Basic HTML structure with minimal content
2. **Complex HTML Page**: Rich HTML with nested elements, attributes, and dynamic content
3. **Data Table**: Generating tables with 100 rows of data

## Methodology

The benchmark uses **proper Jinja2 setup** with:
- `Environment` with `FileSystemLoader` instead of inline `Template` objects
- Template caching enabled (`cache_size=400`)
- Optimizations enabled (`auto_reload=False`, `optimized=True`) 
- Pre-compiled templates for fair comparison

## Running the Benchmark

```bash
# Quick benchmark with proper Jinja2 setup
uv run benchmark.py

# Full benchmark with results saved to file
uv run run_benchmark.py

# Compare inline templates vs Environment approach
uv run jinja_comparison.py
```

## Dependencies

- `tagflow`: For programmatic HTML generation using context managers
- `jinja2`: For template-based HTML generation
- `memory-profiler`: For memory usage analysis

## Results

### Key Findings (With Proper Jinja2 Setup)

Based on 1000 iterations per test with 10 warmup runs:

**Jinja2 with Environment excels at ALL scenarios:**
- ✅ **Simple HTML generation** - 15.39x faster than Tagflow (0.011ms vs 0.166ms)
- ✅ **Complex nested structures** - 23.62x faster than Tagflow (0.038ms vs 0.896ms)  
- ✅ **Data tables** - 13.87x faster than Tagflow (0.514ms vs 7.133ms)
- ✅ **Template compilation and caching** provides massive performance benefits

### Performance Summary

| Scenario | Tagflow (ms) | Jinja2 Environment (ms) | Winner | Ratio |
|----------|--------------|-------------------------|---------|-------|
| Simple Page | 0.166 | 0.011 | **Jinja2** | 15.39x |
| Complex Page | 0.896 | 0.038 | **Jinja2** | 23.62x |
| Data Table (100 rows) | 7.133 | 0.514 | **Jinja2** | 13.87x |

**Overall Average:** Jinja2 is **14.55x faster** across all scenarios (0.188ms vs 2.732ms)

### The Importance of Proper Jinja2 Setup

The `jinja_comparison.py` script demonstrates why proper Jinja2 setup matters:

| Method | Simple Page | Data Table | 
|---------|-------------|------------|
| Inline Template() | 0.840ms | 2.238ms |
| Environment + FileSystemLoader | 0.011ms | 0.552ms |
| **Improvement** | **74.3x faster** | **4.1x faster** |

### Analysis

- **Proper Jinja2 setup is crucial**: Using `Environment` with `FileSystemLoader` instead of inline `Template` objects provides dramatic performance improvements
- **Template compilation and caching**: Jinja2's built-in optimizations make it significantly faster when used correctly
- **Tagflow vs optimized Jinja2**: When Jinja2 is properly configured, it outperforms Tagflow in all scenarios
- **Memory usage** is comparable between both libraries (~47MB)
- **Previous benchmarks may be misleading** if they don't use proper Jinja2 setup

### Recommendations

- **Use Jinja2 Environment** with FileSystemLoader for production applications
- **Enable template caching** and optimizations in Jinja2 
- **Tagflow is still valuable** for cases where programmatic HTML generation is preferred over templates
- **Benchmark methodology matters**: Always use production-ready configurations when comparing libraries

## Implementation Notes

Both libraries are tested using equivalent HTML output to ensure fair comparison. The benchmark includes:
- 10 warmup iterations to eliminate cold start effects
- 1000 test iterations for statistical significance 
- Memory usage profiling using `memory-profiler`
- Statistical analysis (mean, std dev, min/max times)
- **Proper Jinja2 Environment setup** with template caching and optimizations

## Files

- `benchmark.py` - Main benchmark script with optimized Jinja2 setup
- `run_benchmark.py` - Runs benchmark and saves results to file
- `jinja_comparison.py` - Demonstrates difference between inline vs Environment approaches
- `templates/` - Jinja2 template files for fair comparison