# Tagflow Rust+PyO3 Implementation

A high-performance reimplementation of Tagflow using Rust and PyO3 bindings.

## Overview

This experiment explores implementing the core Tagflow functionality in Rust and exposing it to Python through PyO3 bindings. The goal is to maintain the exact same Python API as our previous reimplementation while potentially achieving better performance through Rust's optimizations.

## Goals

- **API Compatibility**: Maintain identical Python API to the tagflow-reimplementation
- **Performance**: Leverage Rust's performance for string building and HTML generation
- **Benchmarking**: Compare performance with Python reimplementation, original Tagflow, and Jinja2

## API Usage

The API is identical to the Python reimplementation:

```python
from tagflow_rust import Document

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
        with doc.div():
            doc.attr("class", "container")  # Dynamic attributes
            with doc.p():
                doc.text("This is a paragraph.")

# Render the final HTML
html = doc.render()
```

## Implementation Details

### Rust Core

- **Document**: Core document builder implemented in Rust
- **TagContext**: Context manager for tags with lazy opening
- **String Building**: Optimized string concatenation using Rust's String/Vec<String>
- **HTML Escaping**: Safe HTML escaping for text and attributes
- **Attribute Conversion**: Python-style attribute name conversion (class_, data_value -> data-value)

### PyO3 Bindings

- **Python Classes**: Document and TagContext exposed as Python classes
- **Context Managers**: Proper `__enter__`/`__exit__` support
- **Tag Shortcuts**: All common HTML tag shortcuts (div, h1, p, etc.)
- **Error Handling**: Proper Python exception handling

## Performance Expectations

The Rust implementation should provide:
- Faster string building operations
- More efficient memory usage
- Reduced overhead for large documents
- Potentially better performance than Python reimplementation

However, PyO3 overhead may limit gains for small documents.

## Files

- `Cargo.toml` - Rust project configuration
- `pyproject.toml` - Python project with Maturin build system
- `src/lib.rs` - Main Rust implementation
- `python/tagflow_rust/__init__.py` - Python module wrapper
- `tests/test_tagflow_rust.py` - Compatibility tests
- `benchmark.py` - Performance comparison

## Building and Testing

```bash
# Install dependencies and build the Rust extension
uv sync

# Run tests
uv run pytest tests/

# Run benchmarks
uv run python benchmark.py
```

## Expected Results

This implementation should demonstrate whether Rust can provide meaningful performance improvements for HTML generation tasks while maintaining Python's ease of use through PyO3 bindings.