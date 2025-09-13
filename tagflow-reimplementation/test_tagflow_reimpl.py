#!/usr/bin/env python3
"""
Tests for the Tagflow reimplementation.

This module contains basic tests to verify that the reimplemented Tagflow
produces correct HTML output and handles various edge cases properly.
"""

from tagflow_reimpl import Document, document


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
    # Note: img is self-closing
    expected = '<div class="container" data-value="123" id="main"><img src="test.jpg" alt="Test Image" /></div>'
    assert html == expected, f"Expected: {expected}, Got: {html}"
    print("✓ Attributes test passed")


def test_text_escaping():
    """Test that text content is properly escaped."""
    doc = Document()
    
    with doc.tag("p"):
        doc.text("Hello & <world> \"test\"")
    
    html = doc.render()
    expected = "<p>Hello &amp; &lt;world&gt; \"test\"</p>"
    assert html == expected, f"Expected: {expected}, Got: {html}"
    print("✓ Text escaping test passed")


def test_attribute_escaping():
    """Test that attribute values are properly escaped."""
    doc = Document()
    
    with doc.tag("div", title="Test & \"quoted\" <value>"):
        pass
    
    html = doc.render()
    expected = '<div title="Test &amp; &quot;quoted&quot; &lt;value&gt;"></div>'
    assert html == expected, f"Expected: {expected}, Got: {html}"
    print("✓ Attribute escaping test passed")


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


def test_attribute_name_conversion():
    """Test attribute name conversion from Python to HTML."""
    doc = Document()
    
    with doc.tag("div", 
                 class_="test",           # class_ -> class
                 data_value="123",        # data_value -> data-value
                 aria_label="button"):    # aria_label -> aria-label
        pass
    
    html = doc.render()
    expected = '<div class="test" data-value="123" aria-label="button"></div>'
    assert html == expected, f"Expected: {expected}, Got: {html}"
    print("✓ Attribute name conversion test passed")


def test_reserved_keyword_attributes():
    """Test that reserved Python keywords work as HTML attributes."""
    doc = Document()
    
    # Test 'for' attribute - common with label tags
    with doc.label(for_="username", class_="form-label"):
        doc.text("Username:")
    
    with doc.input(type="text", id="username", name="username"):
        pass
    
    html = doc.render()
    expected = '<label for="username" class="form-label">Username:</label><input type="text" id="username" name="username" />'
    assert html == expected, f"Expected: {expected}, Got: {html}"
    print("✓ Reserved keyword attributes test passed")


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
        with doc.ul():
            with doc.li():
                doc.text("Item 1")
            with doc.li():
                doc.text("Item 2")
        with doc.button(type="submit", disabled="true"):
            doc.text("Submit")
        # Test self-closing shortcuts
        doc.br()
        doc.hr()
        doc.img(src="test.jpg", alt="Test")
    
    html = doc.render()
    expected = ('<div class="container">'
               '<h1 id="title">Title</h1>'
               '<p class="text">Paragraph</p>'
               '<ul><li>Item 1</li><li>Item 2</li></ul>'
               '<button type="submit" disabled="true">Submit</button>'
               '<br /><hr /><img src="test.jpg" alt="Test" />'
               '</div>')
    
    assert html == expected, f"Expected: {expected}, Got: {html}"
    print("✓ Tag shortcuts test passed")


def test_shortcuts_equivalent_to_tag():
    """Test that shortcuts produce identical output to tag() method."""
    doc1 = Document()
    doc2 = Document()
    
    # Using shortcuts
    with doc1.div(class_="test"):
        with doc1.h1():
            doc1.text("Hello")
        with doc1.p():
            doc1.text("World")
    
    # Using tag() method
    with doc2.tag("div", class_="test"):
        with doc2.tag("h1"):
            doc2.text("Hello")
        with doc2.tag("p"):
            doc2.text("World")
    
    html1 = doc1.render()
    html2 = doc2.render()
    
    assert html1 == html2, f"Shortcut output differs from tag() output: {html1} != {html2}"
    print("✓ Shortcuts equivalent to tag() test passed")


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
    print("Running Tagflow Reimplementation Tests...")
    print()
    
    test_simple_document()
    test_attributes()
    test_text_escaping()
    test_attribute_escaping()
    test_raw_content()
    test_self_closing_tags()
    test_attribute_name_conversion()
    test_reserved_keyword_attributes()
    test_document_reuse()
    test_convenience_function()
    test_tag_shortcuts()
    test_shortcuts_equivalent_to_tag()
    test_complex_nested_structure()
    
    print()
    print("All tests passed! ✓")


if __name__ == "__main__":
    run_all_tests()