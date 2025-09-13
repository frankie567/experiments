# Tagflow Reimplementation

A minimal, efficient reimplementation of Tagflow that keeps the nice context manager syntax while focusing on performance and simplicity.

## Overview

This experiment creates a new Tagflow-like library from scratch, addressing the performance bottlenecks identified in previous experiments:

- **Direct string building** instead of XML ElementTree overhead
- **Explicit document object** to avoid globals and context variables  
- **Minimal context manager overhead** with efficient implementation
- **Full type annotations** using modern Python syntax
- **Simple, focused API** that prioritizes performance
- **Tag shortcuts** for common HTML elements (h1, div, p, etc.)
- **Dynamic attribute addition** via `attr()` function for conditional logic

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

### Tag Shortcuts

For convenience, the library includes shortcut methods for common HTML tags:

```python
# Instead of writing:
with doc.tag("div", class_="container"):
    with doc.tag("h1"):
        doc.text("Title")
    with doc.tag("p"):
        doc.text("Content")

# You can use shortcuts:
with doc.div(class_="container"):
    with doc.h1():
        doc.text("Title")
    with doc.p():
        doc.text("Content")
```

**Available shortcuts**: `div`, `p`, `span`, `h1`-`h6`, `a`, `button`, `form`, `input`, `label`, `select`, `option`, `textarea`, `ul`, `ol`, `li`, `table`, `thead`, `tbody`, `tr`, `td`, `th`, `section`, `article`, `header`, `footer`, `nav`, `main`, `aside`, `strong`, `em`, `code`, `pre`, `img`, `br`, `hr`

The shortcuts are equivalent to calling `doc.tag(tagname, **attrs)` and maintain the same performance characteristics.

### Dynamic Attributes with `attr()`

The library supports dynamic attribute addition using the `attr()` function, which is very handy for conditional logic:

```python
with doc.div():
    doc.attr("class", "container")
    
    if user_is_admin:
        doc.attr("data-role", "administrator")
        doc.attr("class", "container admin-panel")  # Override previous value
    
    if dark_theme:
        doc.attr("data-theme", "dark")
    
    doc.text("Content")
```

This generates different HTML based on the conditions:
- Admin with dark theme: `<div class="container admin-panel" data-role="administrator" data-theme="dark">Content</div>`
- Regular user: `<div class="container">Content</div>`

**Important notes about `attr()`**:
- Must be called within a tag context (after `with doc.tag(...)` or shortcut)
- Can only be called before any content (text, raw HTML, or nested tags) is added
- Subsequent calls to `attr()` with the same name will override previous values
- Works with all attribute name conversions (e.g., `class_` → `class`, `data_value` → `data-value`)

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