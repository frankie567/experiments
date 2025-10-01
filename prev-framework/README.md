# Prev Framework

A file-system based routing web framework for Python, inspired by Next.js but fully server-side.

## Features

- **File-system based routing**: Create routes by creating directories and `route.py` files
- **Path parameters**: Support for dynamic route segments using bracket syntax `[id]`
- **Automatic Document injection**: Framework manages Document lifecycle via function signature analysis
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

2. Define a route in `app/route.py` with automatic Document injection:

```python
from starlette.requests import Request
from prev.html import Document

def route(request: Request, html: Document):
    """Handle GET request for the root route."""
    with html.tag("html"):
        with html.tag("body"):
            with html.h1():
                html.text("Hello from Prev!")
    # No return needed - html is automatically returned as DocumentResponse
```

3. Route with path parameters in `app/users/[id]/route.py`:

```python
from starlette.requests import Request
from prev.html import Document

def route(request: Request, id: str, html: Document):
    """Handle GET request for a specific user."""
    with html.tag("html"):
        with html.tag("body"):
            with html.h1():
                html.text(f"User ID: {id}")
    # Framework automatically returns html as DocumentResponse
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

## Route Function Signatures

Prev supports two approaches for defining routes:

### 1. With `html` Parameter (Recommended)

The framework analyzes your route function's signature. If it has an `html` parameter type-hinted as `Document`, the framework automatically:
- Creates a `Document` instance
- Injects it into your function
- Returns it as a `DocumentResponse`

```python
def route(request: Request, html: Document):
    with html.h1():
        html.text("Hello")
    # No return needed!
```

### 2. Manual Response (for custom responses)

If your route doesn't have an `html` parameter, you can return any Response:

```python
from starlette.responses import JSONResponse

def route(request: Request):
    return JSONResponse({"message": "Hello"})
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
