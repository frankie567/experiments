#!/usr/bin/env python3
"""
Basic tests for the Tagflow Rust+PyO3 implementation.

This module contains tests to verify that the Rust implementation
works correctly and is compatible with the expected API.
"""

from tagflow_rust import Document, document


def test_simple_document():
    """Test basic document creation and rendering."""
    doc = Document()
    
    with doc.tag("html"):
        with doc.tag("head"):
            with doc.tag("title"):
                doc.text("Test Page")
        with doc.tag("body"):
            with doc.tag("h1"):
                doc.text("Hello World")
    
    html = doc.render()
    expected = "<html><head><title>Test Page</title></head><body><h1>Hello World</h1></body></html>"
    assert html == expected, f"Expected: {expected}, Got: {html}"
    print("✓ Simple document test passed")


def test_attributes():
    """Test attribute handling including special cases."""
    doc = Document()
    
    with doc.tag("div", class_="container", data_value="123", id="main"):
        with doc.tag("img", src="test.jpg", alt="Test Image"):
            pass  # Self-closing tag
    
    html = doc.render()
    # Note: img is self-closing and attribute order may vary
    assert html.startswith('<div ')
    assert 'class="container"' in html
    assert 'data-value="123"' in html  
    assert 'id="main"' in html
    assert '<img src="test.jpg" alt="Test Image" /></div>' in html
    print("✓ Attributes test passed")


def test_text_escaping():
    """Test that text content is properly escaped."""
    doc = Document()
    
    with doc.tag("p"):
        doc.text("Hello & <world> \"test\"")
    
    html = doc.render()
    expected = "<p>Hello &amp; &lt;world&gt; \"test\"</p>"  # Quotes don't need escaping in text content
    assert html == expected, f"Expected: {expected}, Got: {html}"
    print("✓ Text escaping test passed")


def test_raw_content():
    """Test raw HTML insertion."""
    doc = Document()
    
    with doc.tag("div"):
        doc.raw("<em>Already formatted</em>")
        doc.text(" and escaped")
    
    html = doc.render()
    expected = "<div><em>Already formatted</em> and escaped</div>"
    assert html == expected, f"Expected: {expected}, Got: {html}"
    print("✓ Raw content test passed")


def test_self_closing_tags():
    """Test that self-closing tags are handled correctly."""
    doc = Document()
    
    with doc.tag("div"):
        with doc.tag("br"):
            pass
        with doc.tag("img", src="test.jpg"):
            pass
        with doc.tag("input", type="text", name="test"):
            pass
    
    html = doc.render()
    expected = '<div><br /><img src="test.jpg" /><input type="text" name="test" /></div>'
    assert html == expected, f"Expected: {expected}, Got: {html}"
    print("✓ Self-closing tags test passed")


def test_convenience_function():
    """Test the convenience document() function."""
    doc = document()
    
    with doc.tag("span"):
        doc.text("Test")
    
    html = doc.render()
    expected = "<span>Test</span>"
    assert html == expected, f"Expected: {expected}, Got: {html}"
    print("✓ Convenience function test passed")


def test_tag_shortcuts():
    """Test that tag shortcuts work correctly."""
    doc = Document()
    
    # Test common tag shortcuts
    with doc.div(class_="container"):
        with doc.h1(id="title"):
            doc.text("Title")
        with doc.p(class_="text"):
            doc.text("Paragraph")
        # Test self-closing shortcuts
        doc.br()
        doc.hr()
        doc.img(src="test.jpg", alt="Test")
    
    html = doc.render()
    expected = ('<div class="container">'
               '<h1 id="title">Title</h1>'
               '<p class="text">Paragraph</p>'
               '<br /><hr /><img src="test.jpg" alt="Test" />'
               '</div>')
    
    assert html == expected, f"Expected: {expected}, Got: {html}"
    print("✓ Tag shortcuts test passed")


def test_document_reuse():
    """Test that documents can be cleared and reused."""
    doc = Document()
    
    # First use
    with doc.tag("p"):
        doc.text("First")
    html1 = doc.render()
    
    # Clear and reuse
    doc.clear()
    with doc.tag("h1"):
        doc.text("Second")
    html2 = doc.render()
    
    assert html1 == "<p>First</p>"
    assert html2 == "<h1>Second</h1>"
    print("✓ Document reuse test passed")


def test_attribute_name_conversion():
    """Test attribute name conversion from Python to HTML."""
    doc = Document()
    
    with doc.tag("div", 
                 class_="test",           # class_ -> class
                 data_value="123",        # data_value -> data-value
                 aria_label="button"):    # aria_label -> aria-label
        pass
    
    html = doc.render()
    # Attribute order may vary
    assert 'class="test"' in html
    assert 'data-value="123"' in html
    assert 'aria-label="button"' in html
    print("✓ Attribute name conversion test passed")


def test_complex_nested_structure():
    """Test complex nested HTML structure similar to benchmark tests."""
    doc = Document()
    
    with doc.tag("html", lang="en"):
        with doc.tag("head"):
            with doc.tag("title"):
                doc.text("Complex Page")
            with doc.tag("meta", charset="utf-8"):
                pass
        with doc.tag("body"):
            with doc.tag("nav", class_="navigation"):
                with doc.tag("ul"):
                    for item in ["Home", "About", "Contact"]:
                        with doc.tag("li"):
                            with doc.tag("a", href=f"#{item.lower()}"):
                                doc.text(item)
            with doc.tag("main"):
                with doc.tag("h1"):
                    doc.text("Welcome")
                with doc.tag("p"):
                    doc.text("This is a test page.")
    
    html = doc.render()
    
    # Verify it contains expected elements
    assert "<html lang=\"en\">" in html
    assert "<meta charset=\"utf-8\" />" in html
    assert "<nav class=\"navigation\">" in html
    assert "<a href=\"#home\">Home</a>" in html
    assert "<a href=\"#about\">About</a>" in html
    assert "<a href=\"#contact\">Contact</a>" in html
    
    print("✓ Complex nested structure test passed")


def run_all_tests():
    """Run all tests."""
    print("Running Tagflow Rust+PyO3 Tests...")
    print()
    
    test_simple_document()
    test_attributes()
    test_text_escaping()
    test_raw_content()
    test_self_closing_tags()
    test_convenience_function()
    test_tag_shortcuts()
    test_document_reuse()
    test_attribute_name_conversion()
    test_complex_nested_structure()
    
    print()
    print("All tests passed! ✓")


if __name__ == "__main__":
    run_all_tests()