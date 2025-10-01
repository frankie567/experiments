"""Dashboard users route."""

from starlette.requests import Request

from prev.html import Document


def route(request: Request, html: Document):
    """Handle GET request for the users route."""
    # Sample user data
    users = [
        {"id": 1, "name": "Alice Johnson", "role": "Admin"},
        {"id": 2, "name": "Bob Smith", "role": "Developer"},
        {"id": 3, "name": "Charlie Brown", "role": "Designer"},
    ]
    
    with html.tag("html", lang="en"):
        with html.tag("head"):
            with html.tag("title"):
                html.text("Users - Dashboard - Prev")
            with html.tag("meta", charset="utf-8"):
                pass
        with html.tag("body"):
            with html.header():
                with html.h1():
                    html.text("User Management")
            with html.main():
                with html.p():
                    with html.a(href="/dashboard"):
                        html.text("← Back to Dashboard")
                
                with html.table():
                    with html.thead():
                        with html.tr():
                            with html.th():
                                html.text("ID")
                            with html.th():
                                html.text("Name")
                            with html.th():
                                html.text("Role")
                    
                    with html.tbody():
                        for user in users:
                            with html.tr():
                                with html.td():
                                    with html.a(href=f"/users/{user['id']}"):
                                        html.text(str(user["id"]))
                                with html.td():
                                    html.text(user["name"])
                                with html.td():
                                    html.text(user["role"])

