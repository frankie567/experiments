"""Dashboard route."""

from starlette.requests import Request

from prev.html import Document


def route(request: Request, html: Document):
    """Handle GET request for the dashboard route."""
    with html.tag("html", lang="en"):
        with html.tag("head"):
            with html.tag("title"):
                html.text("Dashboard - Prev")
            with html.tag("meta", charset="utf-8"):
                pass
        with html.tag("body"):
            with html.header():
                with html.h1():
                    html.text("Dashboard")
            with html.main():
                with html.p():
                    html.text("Welcome to your dashboard!")
                with html.nav():
                    with html.ul():
                        with html.li():
                            with html.a(href="/"):
                                html.text("Home")
                        with html.li():
                            with html.a(href="/dashboard/users"):
                                html.text("Manage Users")

