# Tagflow Reimplementation

A minimal, efficient reimplementation of Tagflow that keeps the nice context manager syntax while focusing on performance and simplicity.

## Overview

This experiment creates a new Tagflow-like library from scratch, addressing the performance bottlenecks identified in previous experiments:

- **Direct string building** instead of XML ElementTree overhead
- **Explicit document object** to avoid globals and context variables  
- **Minimal context manager overhead** with efficient implementation
- **Full type annotations** using modern Python syntax
- **Simple, focused API** that prioritizes performance

## Design Principles

1. **No globals or context vars**: Start a document explicitly and derive structure from it
2. **Minimal overhead**: Direct string concatenation for maximum efficiency
3. **Type safety**: Full type annotations with Python 3.12+ syntax
4. **Clean API**: Keep the familiar context manager syntax that makes Tagflow appealing

## API Usage

```python
from tagflow_reimpl import Document

# Create a document
doc = Document()

# Build HTML using context managers
with doc.tag("html", lang="en"):
    with doc.tag("head"):
        with doc.tag("title"):
            doc.text("Hello World")
    with doc.tag("body"):
        with doc.tag("h1", class_="title"):
            doc.text("Welcome!")
        with doc.tag("p"):
            doc.text("This is a paragraph.")

# Render the final HTML
html = doc.render()
```

## Performance Goals

Based on previous experiments, original Tagflow was 14.55x slower than Jinja2. This reimplementation aims to:

- Reduce the performance gap with Jinja2 to <5x
- Be significantly faster than original Tagflow (target: 5-10x improvement)
- Maintain the same clean API and HTML output quality

## Files

- `tagflow_reimpl.py` - Main implementation
- `benchmark.py` - Performance comparison with original Tagflow and Jinja2
- `test_tagflow_reimpl.py` - Tests for correctness
- `pyproject.toml` - Dependencies and project configuration

## Running the Experiment

```bash
# Install dependencies
uv install

# Run performance benchmark
uv run benchmark.py

# Run tests
uv run test_tagflow_reimpl.py
```

## Implementation Details

### Key Optimizations

1. **String Builder Pattern**: Direct string concatenation instead of DOM building
2. **Stack-based Tag Tracking**: Lightweight stack for proper tag closing
3. **Cached Attribute Processing**: Pre-computed attribute name transformations
4. **Minimal Object Creation**: Reuse objects where possible
5. **Type-optimized Methods**: Use type hints for better performance

### Differences from Original Tagflow

- **Explicit Document**: `Document()` instead of `tagflow.document()`
- **Method-based API**: `doc.tag()` and `doc.text()` instead of module functions
- **No Context Variables**: All state maintained in document object
- **Simpler Implementation**: No live updates, mutation recording, or complex features

## Expected Outcomes

This reimplementation should demonstrate that the Tagflow concept can be made much more efficient while maintaining its appealing API design.