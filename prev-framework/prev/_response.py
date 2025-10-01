"""
Starlette Response classes for Prev framework.
"""

from __future__ import annotations

from starlette.responses import Response

from .html import Document

__all__ = ["DocumentResponse"]


class DocumentResponse(Response):
    """A Starlette Response that renders a Document to HTML.
    
    This response class integrates the Document builder with Starlette's
    response system, automatically rendering the document to HTML and
    setting the appropriate content type.
    
    Example:
        def route(request):
            doc = Document()
            with doc.tag("html"):
                with doc.tag("body"):
                    with doc.h1():
                        doc.text("Hello World")
            return DocumentResponse(doc)
    """
    
    media_type = "text/html"
    
    def __init__(
        self,
        document: Document,
        status_code: int = 200,
        headers: dict[str, str] | None = None,
        media_type: str | None = None,
    ) -> None:
        """Initialize a DocumentResponse.
        
        Args:
            document: The Document to render
            status_code: HTTP status code (default: 200)
            headers: Optional HTTP headers
            media_type: Optional media type (default: "text/html")
        """
        content = document.render()
        super().__init__(
            content=content,
            status_code=status_code,
            headers=headers,
            media_type=media_type,
        )
