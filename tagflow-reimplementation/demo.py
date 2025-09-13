#!/usr/bin/env python3
"""
Demo script showcasing the Tagflow reimplementation API.

This script demonstrates the clean context manager syntax and various features
of the reimplemented Tagflow library.
"""

from tagflow_reimpl import Document


def demo_simple_page():
    """Demonstrate basic usage with a simple page."""
    print("=== Simple Page Demo ===")
    
    doc = Document()
    with doc.tag("html", lang="en"):
        with doc.tag("head"):
            with doc.tag("title"):
                doc.text("Welcome to Tagflow Reimpl")
            with doc.tag("meta", charset="utf-8"):
                pass
        with doc.tag("body"):
            with doc.h1(class_="title"):  # Using shortcut!
                doc.text("Hello World!")
            with doc.p():  # Using shortcut!
                doc.text("This is generated using the reimplemented Tagflow.")
    
    html = doc.render()
    print(html)
    print()


def demo_tag_shortcuts():
    """Demonstrate the new tag shortcuts functionality."""
    print("=== Tag Shortcuts Demo ===")
    
    doc = Document()
    with doc.tag("html", lang="en"):
        with doc.tag("head"):
            with doc.tag("title"):
                doc.text("Tag Shortcuts Demo")
        with doc.tag("body"):
            # Header section using shortcuts
            with doc.header(class_="main-header"):
                with doc.h1():
                    doc.text("Welcome to Tagflow")
                with doc.p():
                    doc.text("Now with convenient tag shortcuts!")
            
            # Navigation using shortcuts
            with doc.nav():
                with doc.ul(class_="nav-list"):
                    for item in ["Home", "About", "Contact"]:
                        with doc.li():
                            with doc.a(href=f"#{item.lower()}", class_="nav-link"):
                                doc.text(item)
            
            # Main content using shortcuts
            with doc.main():
                with doc.section(class_="content"):
                    with doc.h2():
                        doc.text("Features")
                    with doc.div(class_="feature-grid"):
                        for i, feature in enumerate(["Fast", "Simple", "Type-safe"], 1):
                            with doc.div(class_="feature-card"):
                                with doc.h3():
                                    doc.text(f"Feature {i}")
                                with doc.p():
                                    doc.text(f"This feature is {feature.lower()}.")
                
                # Form example using shortcuts
                with doc.section(class_="form-section"):
                    with doc.h2():
                        doc.text("Contact Form")
                    with doc.form(action="/submit", method="post"):
                        with doc.div(class_="form-group"):
                            with doc.label(for_="name"):
                                doc.text("Name:")
                            doc.input(type="text", id="name", name="name", required="true")
                        
                        with doc.div(class_="form-group"):
                            with doc.label(for_="email"):
                                doc.text("Email:")
                            doc.input(type="email", id="email", name="email", required="true")
                        
                        with doc.div(class_="form-group"):
                            with doc.label(for_="message"):
                                doc.text("Message:")
                            with doc.textarea(id="message", name="message", rows="4"):
                                doc.text("Enter your message here...")
                        
                        with doc.button(type="submit", class_="submit-btn"):
                            doc.text("Send Message")
                
                # Table example using shortcuts
                with doc.section(class_="table-section"):
                    with doc.h2():
                        doc.text("Performance Comparison")
                    with doc.table(class_="comparison-table"):
                        with doc.thead():
                            with doc.tr():
                                with doc.th():
                                    doc.text("Library")
                                with doc.th():
                                    doc.text("Speed")
                                with doc.th():
                                    doc.text("Type Safety")
                        with doc.tbody():
                            data = [
                                ("Original Tagflow", "Slow", "No"),
                                ("Tagflow Reimpl", "Fast", "Yes"),
                                ("Jinja2", "Fastest", "Limited")
                            ]
                            for lib, speed, types in data:
                                with doc.tr():
                                    with doc.td():
                                        doc.text(lib)
                                    with doc.td():
                                        with doc.strong():
                                            doc.text(speed)
                                    with doc.td():
                                        with doc.em():
                                            doc.text(types)
            
            # Self-closing tags demo
            with doc.footer():
                with doc.p():
                    doc.text("Some self-closing tag examples:")
                doc.br()  # Line break
                doc.hr()  # Horizontal rule
                doc.img(src="logo.png", alt="Logo", width="100")
    
    html = doc.render()
    print(html)
    print()


def demo_complex_features():
    """Demonstrate advanced features like attribute handling and escaping."""
    print("=== Advanced Features Demo ===")
    
    doc = Document()
    with doc.tag("div", class_="container", data_value="test"):
        with doc.tag("h2"):
            doc.text("Features & Escaping")
        
        # Text escaping
        with doc.tag("p"):
            doc.text("This text contains <special> & \"quoted\" characters.")
        
        # Attribute escaping
        with doc.tag("input", 
                     type="text", 
                     value="Default & <value>",
                     placeholder="Enter your \"name\""):
            pass
        
        # Raw HTML (use with caution)
        with doc.tag("div"):
            doc.text("Escaped: ")
            doc.raw("<em>Raw HTML</em>")
        
        # Self-closing tags
        with doc.tag("img", src="image.jpg", alt="Sample image"):
            pass
        
        with doc.tag("br"):
            pass
    
    html = doc.render()
    print(html)
    print()


def demo_data_generation():
    """Demonstrate dynamic content generation."""
    print("=== Dynamic Content Demo ===")
    
    # Sample data
    users = [
        {"name": "Alice", "age": 30, "role": "Developer"},
        {"name": "Bob", "age": 25, "role": "Designer"},
        {"name": "Charlie", "age": 35, "role": "Manager"}
    ]
    
    doc = Document()
    with doc.tag("html"):
        with doc.tag("head"):
            with doc.tag("title"):
                doc.text("User Directory")
        with doc.tag("body"):
            with doc.tag("h1"):
                doc.text("Team Members")
            
            with doc.tag("table", class_="user-table"):
                with doc.tag("thead"):
                    with doc.tag("tr"):
                        for header in ["Name", "Age", "Role"]:
                            with doc.tag("th"):
                                doc.text(header)
                
                with doc.tag("tbody"):
                    for user in users:
                        with doc.tag("tr"):
                            with doc.tag("td"):
                                doc.text(user["name"])
                            with doc.tag("td"):
                                doc.text(str(user["age"]))
                            with doc.tag("td", class_="role"):
                                doc.text(user["role"])
    
    html = doc.render()
    print(html)
    print()


def demo_document_reuse():
    """Demonstrate document reuse for multiple generations."""
    print("=== Document Reuse Demo ===")
    
    doc = Document()
    
    # Generate multiple small HTML snippets
    for i in range(3):
        with doc.tag("div", id=f"item-{i}"):
            with doc.tag("h3"):
                doc.text(f"Item {i + 1}")
            with doc.tag("p"):
                doc.text(f"This is content for item {i + 1}.")
        
        print(f"Item {i + 1}: {doc.render()}")
        doc.clear()  # Clear for next use
    
    print()


def main():
    """Run all demos."""
    print("Tagflow Reimplementation Demo")
    print("=" * 40)
    print()
    
    demo_simple_page()
    demo_tag_shortcuts()
    demo_complex_features()
    demo_data_generation()
    demo_document_reuse()
    
    print("Demo complete! ✓")


if __name__ == "__main__":
    main()