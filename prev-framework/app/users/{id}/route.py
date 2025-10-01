"""User detail route with path parameter."""

from starlette.requests import Request

from prev.html import Document


def route(request: Request, id: str, html: Document):
    """Handle GET request for a specific user.
    
    Args:
        request: The Starlette request
        id: User ID from the URL path parameter
        html: Document instance automatically injected by the framework
    """
    # Sample user data (in real app, would fetch from database)
    users = {
        "1": {"id": 1, "name": "Alice Johnson", "role": "Admin", "email": "alice@example.com"},
        "2": {"id": 2, "name": "Bob Smith", "role": "Developer", "email": "bob@example.com"},
        "3": {"id": 3, "name": "Charlie Brown", "role": "Designer", "email": "charlie@example.com"},
    }
    
    user = users.get(id)
    
    with html.tag("html", lang="en"):
        with html.tag("head"):
            with html.tag("title"):
                if user:
                    html.text(f"{user['name']} - User Detail - Prev")
                else:
                    html.text("User Not Found - Prev")
            with html.tag("meta", charset="utf-8"):
                pass
        with html.tag("body"):
            with html.header():
                with html.h1():
                    if user:
                        html.text(f"User: {user['name']}")
                    else:
                        html.text("User Not Found")
            with html.main():
                with html.p():
                    with html.a(href="/dashboard/users"):
                        html.text("← Back to Users List")
                
                if user:
                    with html.div(class_="user-details"):
                        with html.p():
                            with html.strong():
                                html.text("ID: ")
                            html.text(str(user["id"]))
                        with html.p():
                            with html.strong():
                                html.text("Name: ")
                            html.text(user["name"])
                        with html.p():
                            with html.strong():
                                html.text("Role: ")
                            html.text(user["role"])
                        with html.p():
                            with html.strong():
                                html.text("Email: ")
                            html.text(user["email"])
                else:
                    with html.p():
                        html.text(f"No user found with ID: {id}")

