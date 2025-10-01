"""Dashboard users route."""

from starlette.requests import Request

from prev.html import Document


def route(request: Request):
    """Handle GET request for the users route."""
    doc = Document()
    
    # Sample user data
    users = [
        {"id": 1, "name": "Alice Johnson", "role": "Admin"},
        {"id": 2, "name": "Bob Smith", "role": "Developer"},
        {"id": 3, "name": "Charlie Brown", "role": "Designer"},
    ]
    
    with doc.tag("html", lang="en"):
        with doc.tag("head"):
            with doc.tag("title"):
                doc.text("Users - Dashboard - Prev")
            with doc.tag("meta", charset="utf-8"):
                pass
        with doc.tag("body"):
            with doc.header():
                with doc.h1():
                    doc.text("User Management")
            with doc.main():
                with doc.p():
                    with doc.a(href="/dashboard"):
                        doc.text("← Back to Dashboard")
                
                with doc.table():
                    with doc.thead():
                        with doc.tr():
                            with doc.th():
                                doc.text("ID")
                            with doc.th():
                                doc.text("Name")
                            with doc.th():
                                doc.text("Role")
                    
                    with doc.tbody():
                        for user in users:
                            with doc.tr():
                                with doc.td():
                                    with doc.a(href=f"/users/{user['id']}"):
                                        doc.text(str(user["id"]))
                                with doc.td():
                                    doc.text(user["name"])
                                with doc.td():
                                    doc.text(user["role"])
    
    yield doc
