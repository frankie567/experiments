"""Root route."""

from starlette.requests import Request

from prev import Document, DocumentResponse


def route(request: Request) -> DocumentResponse:
    """Handle GET request for the root route."""
    doc = Document()
    
    with doc.tag("html", lang="en"):
        with doc.tag("head"):
            with doc.tag("title"):
                doc.text("Welcome to Prev")
            with doc.tag("meta", charset="utf-8"):
                pass
        with doc.tag("body"):
            with doc.header():
                with doc.h1():
                    doc.text("Welcome to Prev Framework")
            with doc.main():
                with doc.p():
                    doc.text("This is a file-system based routing web framework.")
                with doc.p():
                    doc.text("Check out these routes:")
                with doc.ul():
                    with doc.li():
                        with doc.a(href="/dashboard"):
                            doc.text("Dashboard")
                    with doc.li():
                        with doc.a(href="/dashboard/users"):
                            doc.text("Users")
    
    return DocumentResponse(doc)
