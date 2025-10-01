"""User detail route with path parameter."""

from starlette.requests import Request

from prev.html import Document


def route(request: Request, id: str):
    """Handle GET request for a specific user.
    
    Args:
        request: The Starlette request
        id: User ID from the URL path parameter
    """
    doc = Document()
    
    # Sample user data (in real app, would fetch from database)
    users = {
        "1": {"id": 1, "name": "Alice Johnson", "role": "Admin", "email": "alice@example.com"},
        "2": {"id": 2, "name": "Bob Smith", "role": "Developer", "email": "bob@example.com"},
        "3": {"id": 3, "name": "Charlie Brown", "role": "Designer", "email": "charlie@example.com"},
    }
    
    user = users.get(id)
    
    with doc.tag("html", lang="en"):
        with doc.tag("head"):
            with doc.tag("title"):
                if user:
                    doc.text(f"{user['name']} - User Detail - Prev")
                else:
                    doc.text("User Not Found - Prev")
            with doc.tag("meta", charset="utf-8"):
                pass
        with doc.tag("body"):
            with doc.header():
                with doc.h1():
                    if user:
                        doc.text(f"User: {user['name']}")
                    else:
                        doc.text("User Not Found")
            with doc.main():
                with doc.p():
                    with doc.a(href="/dashboard/users"):
                        doc.text("← Back to Users List")
                
                if user:
                    with doc.div(class_="user-details"):
                        with doc.p():
                            with doc.strong():
                                doc.text("ID: ")
                            doc.text(str(user["id"]))
                        with doc.p():
                            with doc.strong():
                                doc.text("Name: ")
                            doc.text(user["name"])
                        with doc.p():
                            with doc.strong():
                                doc.text("Role: ")
                            doc.text(user["role"])
                        with doc.p():
                            with doc.strong():
                                doc.text("Email: ")
                            doc.text(user["email"])
                else:
                    with doc.p():
                        doc.text(f"No user found with ID: {id}")
    
    yield doc
