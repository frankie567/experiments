"""Dashboard route."""

from starlette.requests import Request

from prev.html import Document


def route(request: Request):
    """Handle GET request for the dashboard route."""
    doc = Document()
    
    with doc.tag("html", lang="en"):
        with doc.tag("head"):
            with doc.tag("title"):
                doc.text("Dashboard - Prev")
            with doc.tag("meta", charset="utf-8"):
                pass
        with doc.tag("body"):
            with doc.header():
                with doc.h1():
                    doc.text("Dashboard")
            with doc.main():
                with doc.p():
                    doc.text("Welcome to your dashboard!")
                with doc.nav():
                    with doc.ul():
                        with doc.li():
                            with doc.a(href="/"):
                                doc.text("Home")
                        with doc.li():
                            with doc.a(href="/dashboard/users"):
                                doc.text("Manage Users")
    
    yield doc
