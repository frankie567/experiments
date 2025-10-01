"""
File-system based routing for Prev framework.
"""

from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path
from typing import Any, Callable

from starlette.routing import Route

__all__ = ["discover_routes"]


def _load_route_function(route_file: Path) -> Callable[..., Any] | None:
    """Load the route function from a route.py file.
    
    Args:
        route_file: Path to the route.py file
        
    Returns:
        The route function if found, None otherwise
    """
    # Load the module dynamically
    spec = importlib.util.spec_from_file_location(f"route_{route_file.parent.name}", route_file)
    if spec is None or spec.loader is None:
        return None
    
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Look for the route function
    if hasattr(module, "route"):
        route_func: Any = getattr(module, "route")
        if callable(route_func):
            return route_func  # type: ignore[no-any-return]
    
    return None


def _path_to_route(route_file: Path, base_path: Path) -> str:
    """Convert a file path to a URL route.
    
    Args:
        route_file: Path to the route.py file
        base_path: Base directory for routes (e.g., "app" folder)
        
    Returns:
        URL route string
        
    Example:
        _path_to_route(Path("app/dashboard/users/route.py"), Path("app"))
        -> "/dashboard/users"
    """
    # Get the relative path from base to the route file's parent
    relative_path = route_file.parent.relative_to(base_path)
    
    # Convert to URL path
    if str(relative_path) == ".":
        # Root route
        return "/"
    else:
        # Convert path separators to URL separators
        return "/" + str(relative_path).replace("\\", "/")


def discover_routes(base_path: Path) -> list[Route]:
    """Discover routes from a directory structure.
    
    This function walks through the directory tree starting from base_path
    and finds all route.py files. Each route.py file should define a `route`
    function that will be used as the route handler.
    
    Args:
        base_path: Base directory to search for routes
        
    Returns:
        List of Starlette Route objects
        
    Example directory structure:
        app/
            route.py              -> /
            dashboard/
                route.py          -> /dashboard
                users/
                    route.py      -> /dashboard/users
    """
    if not base_path.exists():
        raise ValueError(f"Routes directory does not exist: {base_path}")
    
    if not base_path.is_dir():
        raise ValueError(f"Routes path is not a directory: {base_path}")
    
    routes: list[Route] = []
    
    # Find all route.py files
    for route_file in base_path.rglob("route.py"):
        # Load the route function
        route_func = _load_route_function(route_file)
        
        if route_func is None:
            # Skip files without a route function
            continue
        
        # Convert file path to URL route
        url_path = _path_to_route(route_file, base_path)
        
        # Create Starlette route
        # For now, all routes are GET only as specified in requirements
        route = Route(url_path, route_func, methods=["GET"])
        routes.append(route)
    
    return routes
