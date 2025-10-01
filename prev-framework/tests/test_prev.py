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
            "from prev import Document, DocumentResponse\n"
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
