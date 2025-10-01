"""Root route."""

from starlette.requests import Request

from prev.html import Document


def route(request: Request, html: Document):
    """Handle GET request for the root route."""
    with html.tag("html", lang="en"):
        with html.tag("head"):
            with html.tag("title"):
                html.text("Welcome to Prev")
            with html.tag("meta", charset="utf-8"):
                pass
        with html.tag("body"):
            with html.header():
                with html.h1():
                    html.text("Welcome to Prev Framework")
            with html.main():
                with html.p():
                    html.text("This is a file-system based routing web framework.")
                with html.p():
                    html.text("Check out these routes:")
                with html.ul():
                    with html.li():
                        with html.a(href="/dashboard"):
                            html.text("Dashboard")
                    with html.li():
                        with html.a(href="/dashboard/users"):
                            html.text("Users")
                    with html.li():
                        with html.a(href="/users/123"):
                            html.text("User Detail (ID: 123)")

