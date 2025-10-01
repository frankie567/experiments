# Prev Framework

A file-system based routing web framework for Python, inspired by Next.js but fully server-side.

## Features

- **File-system based routing**: Create routes by creating directories and `route.py` files
- **Path parameters**: Support for dynamic route segments using bracket syntax `[id]`
- **Generator-based templates**: Yield Document objects directly for cleaner code
- **First-class HTML templates**: Use a clean context manager syntax for building HTML
- **Built on Starlette**: Production-ready ASGI framework with async support
- **Full type annotations**: Complete type safety for better developer experience
- **Zero JavaScript**: Pure Python, server-side rendering

## Installation

```bash
uv sync
```

## Quick Start

1. Create your route structure:

```
app/
    route.py                # Root route: /
    dashboard/
        route.py            # Dashboard route: /dashboard
        users/
            route.py        # Users route: /dashboard/users
            [id]/
                route.py    # User detail: /dashboard/users/{id}
```

2. Define a route in `app/route.py` using the generator syntax:

```python
from starlette.requests import Request
from prev.html import Document

def route(request: Request):
    """Handle GET request for the root route."""
    doc = Document()
    
    with doc.tag("html"):
        with doc.tag("body"):
            with doc.h1():
                doc.text("Hello from Prev!")
    
    yield doc
```

3. Route with path parameters in `app/users/[id]/route.py`:

```python
from starlette.requests import Request
from prev.html import Document

def route(request: Request, id: str):
    """Handle GET request for a specific user."""
    doc = Document()
    
    with doc.tag("html"):
        with doc.tag("body"):
            with doc.h1():
                doc.text(f"User ID: {id}")
    
    yield doc
```

4. Create your app in `main.py`:

```python
from prev import Prev

app = Prev()
```

5. Run with uvicorn:

```bash
uvicorn main:app --reload
```

## Document API

The `Document` class provides a clean context manager syntax for building HTML:

```python
from prev.html import Document

doc = Document()

with doc.tag("html", lang="en"):
    with doc.tag("head"):
        with doc.tag("title"):
            doc.text("My Page")
    with doc.tag("body"):
        # Use shortcut methods
        with doc.div(class_="container"):
            with doc.h1():
                doc.text("Welcome")
            with doc.p():
                doc.text("This is a paragraph")
            
            # Self-closing tags
            doc.br()
            doc.hr()
            doc.img(src="logo.png", alt="Logo")

# Render to HTML string
html = doc.render()
```

### Available Shortcuts

Common HTML tags have shortcut methods: `div`, `p`, `span`, `h1`-`h6`, `a`, `button`, `form`, `input`, `label`, `ul`, `ol`, `li`, `table`, `tr`, `td`, `th`, `header`, `footer`, `nav`, `main`, `section`, `article`, and more.

### Dynamic Attributes

Use `doc.attr()` for conditional attribute addition:

```python
with doc.div():
    if user.is_admin:
        doc.attr("class", "admin-panel")
        doc.attr("data-role", "admin")
    doc.text("Content")
```

## Architecture

- **Prev**: Main application class that bootstraps the app and discovers routes
- **Document**: HTML document builder with context manager API
- **DocumentResponse**: Starlette Response that renders a Document to HTML

## Current Limitations

- Only GET requests are supported (other HTTP methods to be added)
- No built-in data validation or database access (use your favorite libraries)
- Routes are discovered at startup (no dynamic route addition yet)

## Development

Run tests:

```bash
uv run pytest
```

Type checking:

```bash
uv run mypy prev/
```

## License

MIT
