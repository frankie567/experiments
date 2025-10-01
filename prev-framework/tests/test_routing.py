"""Tests for file-system based routing."""

from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from prev._routing import _path_to_route, discover_routes


def test_path_to_route_root() -> None:
    """Test converting root route.py to URL path."""
    route_file = Path("app/route.py")
    base_path = Path("app")
    
    url = _path_to_route(route_file, base_path)
    assert url == "/"


def test_path_to_route_nested() -> None:
    """Test converting nested route.py to URL path."""
    route_file = Path("app/dashboard/users/route.py")
    base_path = Path("app")
    
    url = _path_to_route(route_file, base_path)
    assert url == "/dashboard/users"


def test_path_to_route_single_level() -> None:
    """Test converting single-level nested route.py to URL path."""
    route_file = Path("app/about/route.py")
    base_path = Path("app")
    
    url = _path_to_route(route_file, base_path)
    assert url == "/about"


def test_discover_routes_nonexistent_dir() -> None:
    """Test that discover_routes raises error for nonexistent directory."""
    with pytest.raises(ValueError, match="does not exist"):
        discover_routes(Path("/nonexistent/path"))


def test_discover_routes_not_a_dir() -> None:
    """Test that discover_routes raises error for non-directory path."""
    with TemporaryDirectory() as tmpdir:
        file_path = Path(tmpdir) / "file.txt"
        file_path.write_text("test")
        
        with pytest.raises(ValueError, match="not a directory"):
            discover_routes(file_path)


def test_discover_routes_empty_dir() -> None:
    """Test that discover_routes returns empty list for directory without routes."""
    with TemporaryDirectory() as tmpdir:
        routes = discover_routes(Path(tmpdir))
        assert routes == []


def test_discover_routes_with_routes() -> None:
    """Test discovering routes from directory structure."""
    with TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        
        # Create route structure
        (base / "route.py").write_text(
            "from starlette.requests import Request\n"
            "from starlette.responses import Response\n"
            "def route(request: Request) -> Response:\n"
            "    return Response('root')\n"
        )
        
        (base / "about").mkdir()
        (base / "about" / "route.py").write_text(
            "from starlette.requests import Request\n"
            "from starlette.responses import Response\n"
            "def route(request: Request) -> Response:\n"
            "    return Response('about')\n"
        )
        
        (base / "dashboard").mkdir()
        (base / "dashboard" / "users").mkdir(parents=True)
        (base / "dashboard" / "users" / "route.py").write_text(
            "from starlette.requests import Request\n"
            "from starlette.responses import Response\n"
            "def route(request: Request) -> Response:\n"
            "    return Response('users')\n"
        )
        
        routes = discover_routes(base)
        
        # Should find 3 routes
        assert len(routes) == 3
        
        # Check that routes have correct paths
        paths = sorted([route.path for route in routes])
        assert paths == ["/", "/about", "/dashboard/users"]


def test_discover_routes_skips_files_without_route_function() -> None:
    """Test that files without a route function are skipped."""
    with TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        
        # Create a route.py without route function
        (base / "route.py").write_text("# No route function here\n")
        
        # Create a route.py with route function
        (base / "valid").mkdir()
        (base / "valid" / "route.py").write_text(
            "from starlette.requests import Request\n"
            "from starlette.responses import Response\n"
            "def route(request: Request) -> Response:\n"
            "    return Response('valid')\n"
        )
        
        routes = discover_routes(base)
        
        # Should only find the valid route
        assert len(routes) == 1
        assert routes[0].path == "/valid"
