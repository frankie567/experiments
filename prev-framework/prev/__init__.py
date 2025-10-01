"""
Prev - A file-system based routing web framework.

This framework provides a Next.js-inspired developer experience with server-side
rendering, file-system based routing, and first-class HTML template support.
"""

from __future__ import annotations

import inspect
from pathlib import Path

from starlette.applications import Starlette

from ._response import DocumentResponse
from ._routing import discover_routes
from ._tagflow import Document

__all__ = ["Prev", "Document", "DocumentResponse"]

__version__ = "0.1.0"


class Prev:
    """Main application class for Prev framework.
    
    This class bootstraps the application by discovering routes from the
    file-system and creating a Starlette ASGI application.
    
    Example:
        # main.py
        from prev import Prev
        
        app = Prev()
        
        # Then run with: uvicorn main:app
        
    With custom app directory:
        app = Prev(app_dir=Path("my_routes"))
    """
    
    def __init__(self, app_dir: Path | None = None, debug: bool = False) -> None:
        """Initialize the Prev application.
        
        Args:
            app_dir: Directory containing route files. If None, looks for an "app"
                    directory alongside the file that instantiates Prev.
            debug: Enable debug mode (passed to Starlette)
        """
        # Determine the app directory
        if app_dir is None:
            # Find the caller's file location
            frame = inspect.currentframe()
            if frame is not None and frame.f_back is not None:
                caller_file = inspect.getframeinfo(frame.f_back).filename
                caller_dir = Path(caller_file).parent
                app_dir = caller_dir / "app"
            else:
                # Fallback to current directory
                app_dir = Path.cwd() / "app"
        
        self.app_dir = app_dir
        self.debug = debug
        
        # Discover routes from the file system
        routes = discover_routes(self.app_dir)
        
        # Create Starlette application
        self._app = Starlette(debug=debug, routes=routes)
    
    async def __call__(self, scope: dict[str, any], receive: any, send: any) -> None:  # type: ignore
        """ASGI application interface.
        
        This makes Prev directly usable as an ASGI application.
        """
        await self._app(scope, receive, send)
    
    @property
    def routes(self) -> list[any]:  # type: ignore
        """Get the list of routes registered with the application."""
        return self._app.routes
