"""Tests for the Prev application class."""

from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from starlette.testclient import TestClient

from prev import Prev


def test_prev_initialization_with_custom_dir() -> None:
    """Test Prev initialization with custom app directory."""
    with TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        
        # Create a simple route
        (base / "route.py").write_text(
            "from starlette.requests import Request\n"
            "from starlette.responses import Response\n"
            "def route(request: Request) -> Response:\n"
            "    return Response('test')\n"
        )
        
        app = Prev(app_dir=base)
        
        assert app.app_dir == base
        assert len(app.routes) == 1


def test_prev_as_asgi_app() -> None:
    """Test that Prev works as an ASGI application."""
    with TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        
        # Create a simple route
        (base / "route.py").write_text(
            "from starlette.requests import Request\n"
            "from prev.html import Document\n"
            "from prev import DocumentResponse\n"
            "def route(request: Request) -> DocumentResponse:\n"
            "    doc = Document()\n"
            "    with doc.tag('html'):\n"
            "        with doc.tag('body'):\n"
            "            with doc.h1():\n"
            "                doc.text('Test')\n"
            "    return DocumentResponse(doc)\n"
        )
        
        app = Prev(app_dir=base)
        client = TestClient(app)
        
        response = client.get("/")
        assert response.status_code == 200
        assert b"<h1>Test</h1>" in response.content


def test_prev_multiple_routes() -> None:
    """Test Prev with multiple routes."""
    with TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        
        # Create root route
        (base / "route.py").write_text(
            "from starlette.requests import Request\n"
            "from starlette.responses import Response\n"
            "def route(request: Request) -> Response:\n"
            "    return Response('root')\n"
        )
        
        # Create about route
        (base / "about").mkdir()
        (base / "about" / "route.py").write_text(
            "from starlette.requests import Request\n"
            "from starlette.responses import Response\n"
            "def route(request: Request) -> Response:\n"
            "    return Response('about')\n"
        )
        
        app = Prev(app_dir=base)
        client = TestClient(app)
        
        # Test root route
        response = client.get("/")
        assert response.status_code == 200
        assert response.text == "root"
        
        # Test about route
        response = client.get("/about")
        assert response.status_code == 200
        assert response.text == "about"


def test_prev_nonexistent_route() -> None:
    """Test that accessing nonexistent route returns 404."""
    with TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        
        # Create a single route
        (base / "route.py").write_text(
            "from starlette.requests import Request\n"
            "from starlette.responses import Response\n"
            "def route(request: Request) -> Response:\n"
            "    return Response('root')\n"
        )
        
        app = Prev(app_dir=base)
        client = TestClient(app)
        
        response = client.get("/nonexistent")
        assert response.status_code == 404


def test_prev_debug_mode() -> None:
    """Test Prev initialization with debug mode."""
    with TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        
        (base / "route.py").write_text(
            "from starlette.requests import Request\n"
            "from starlette.responses import Response\n"
            "def route(request: Request) -> Response:\n"
            "    return Response('test')\n"
        )
        
        app = Prev(app_dir=base, debug=True)
        
        assert app.debug is True


def test_prev_generator_route() -> None:
    """Test Prev with generator-based route."""
    with TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        
        # Create a route using generator syntax
        (base / "route.py").write_text(
            "from starlette.requests import Request\n"
            "from prev.html import Document\n"
            "def route(request: Request):\n"
            "    doc = Document()\n"
            "    with doc.tag('html'):\n"
            "        with doc.tag('body'):\n"
            "            with doc.h1():\n"
            "                doc.text('Generator Test')\n"
            "    yield doc\n"
        )
        
        app = Prev(app_dir=base)
        client = TestClient(app)
        
        response = client.get("/")
        assert response.status_code == 200
        assert b"<h1>Generator Test</h1>" in response.content


def test_prev_path_parameters() -> None:
    """Test Prev with path parameters."""
    with TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        
        # Create a route with path parameter
        (base / "users").mkdir()
        (base / "users" / "[id]").mkdir()
        (base / "users" / "[id]" / "route.py").write_text(
            "from starlette.requests import Request\n"
            "from prev.html import Document\n"
            "def route(request: Request, id: str):\n"
            "    doc = Document()\n"
            "    with doc.tag('html'):\n"
            "        with doc.tag('body'):\n"
            "            with doc.h1():\n"
            "                doc.text(f'User ID: {id}')\n"
            "    yield doc\n"
        )
        
        app = Prev(app_dir=base)
        client = TestClient(app)
        
        response = client.get("/users/123")
        assert response.status_code == 200
        assert b"User ID: 123" in response.content
