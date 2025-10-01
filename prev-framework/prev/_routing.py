"""
File-system based routing for Prev framework.
"""

from __future__ import annotations

import importlib.util
import inspect
import re
from pathlib import Path
from typing import Any, Callable, Generator

from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route

from ._response import DocumentResponse
from .html import Document

__all__ = ["discover_routes", "route_handler"]


def route_handler(func: Callable[..., Any]) -> Callable[..., Any]:
    """Wrapper for route functions that manages Document lifecycle.
    
    This decorator analyzes the route function's signature and automatically
    injects a Document instance if the function has an 'html' parameter
    type-hinted as Document.
    
    Example with html parameter (preferred):
        def route(request: Request, html: Document):
            with html.h1():
                html.text("Hello")
            # No return needed - html is automatically returned
    
    Example without html parameter (manual response):
        def route(request: Request):
            return Response("Hello", media_type="text/plain")
    
    Args:
        func: The route function to wrap
        
    Returns:
        Wrapped function that returns a Response
    """
    # Analyze the function signature once
    sig = inspect.signature(func)
    
    # Check if function has 'html' parameter with Document type hint
    has_html_param = False
    if "html" in sig.parameters:
        param = sig.parameters["html"]
        # Check if it's type-hinted as Document
        if param.annotation is Document or (
            hasattr(param.annotation, "__origin__") and param.annotation.__origin__ is Document
        ):
            has_html_param = True
    
    async def async_wrapper(request: Request) -> Response:
        # Extract path parameters from request
        path_params = request.path_params
        
        # Prepare function arguments
        kwargs = {"request": request, **path_params}
        
        # If function expects html parameter, create and inject Document
        if has_html_param:
            doc = Document()
            kwargs["html"] = doc
            
            # Call the route function
            if inspect.iscoroutinefunction(func):
                await func(**kwargs)
            else:
                func(**kwargs)
            
            # Return the document as response
            return DocumentResponse(doc)
        else:
            # Call the route function without html parameter
            if inspect.iscoroutinefunction(func):
                result = await func(**kwargs)
            else:
                result = func(**kwargs)
            
            # Return the result (should be a Response)
            if isinstance(result, Response):
                return result
            
            # If it's a Document, wrap it in DocumentResponse
            if isinstance(result, Document):
                return DocumentResponse(result)
            
            # Otherwise, return as-is
            return result  # type: ignore[no-any-return]
    
    return async_wrapper


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
    """Convert a file path to a URL route with support for path parameters.
    
    Directories with names in curly braces (e.g., {id}, {id:int}) are used
    directly as path parameters in Starlette's syntax. This supports convertors
    like {id:int}, {path:path}, etc.
    
    Args:
        route_file: Path to the route.py file
        base_path: Base directory for routes (e.g., "app" folder)
        
    Returns:
        URL route string
        
    Example:
        _path_to_route(Path("app/dashboard/users/route.py"), Path("app"))
        -> "/dashboard/users"
        
        _path_to_route(Path("app/users/{id}/route.py"), Path("app"))
        -> "/users/{id}"
        
        _path_to_route(Path("app/posts/{id:int}/route.py"), Path("app"))
        -> "/posts/{id:int}"
    """
    # Get the relative path from base to the route file's parent
    relative_path = route_file.parent.relative_to(base_path)
    
    # Convert to URL path
    if str(relative_path) == ".":
        # Root route
        return "/"
    else:
        # Convert path separators to URL separators
        path_str = str(relative_path).replace("\\", "/")
        
        # Path parameters in directory names are already in {param} or {param:converter} format
        # No transformation needed - they pass through directly to Starlette
        
        return "/" + path_str


def discover_routes(base_path: Path) -> list[Route]:
    """Discover routes from a directory structure.
    
    This function walks through the directory tree starting from base_path
    and finds all route.py files. Each route.py file should define a `route`
    function that will be used as the route handler.
    
    Supports path parameters using bracket syntax: [id] in directory names
    are converted to {id} path parameters.
    
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
                    [id]/
                        route.py  -> /dashboard/users/{id}
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
        
        # Wrap the route function to support generator-based routes
        wrapped_func = route_handler(route_func)
        
        # Convert file path to URL route
        url_path = _path_to_route(route_file, base_path)
        
        # Create Starlette route
        # For now, all routes are GET only as specified in requirements
        route = Route(url_path, wrapped_func, methods=["GET"])
        routes.append(route)
    
    return routes
