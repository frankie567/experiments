"""Tests for the Document HTML builder."""

from prev._tagflow import Document


def test_simple_document() -> None:
    """Test basic document creation and rendering."""
    doc = Document()
    
    with doc.tag("html"):
        with doc.tag("body"):
            with doc.h1():
                doc.text("Hello World")
    
    html = doc.render()
    expected = "<html><body><h1>Hello World</h1></body></html>"
    assert html == expected


def test_attributes() -> None:
    """Test attribute handling."""
    doc = Document()
    
    with doc.div(class_="container", data_value="123", id="main"):
        doc.text("Content")
    
    html = doc.render()
    assert 'class="container"' in html
    assert 'data-value="123"' in html
    assert 'id="main"' in html


def test_text_escaping() -> None:
    """Test that text content is properly escaped."""
    doc = Document()
    
    with doc.p():
        doc.text("Hello & <world>")
    
    html = doc.render()
    assert "&amp;" in html
    assert "&lt;world&gt;" in html


def test_self_closing_tags() -> None:
    """Test that self-closing tags are handled correctly."""
    doc = Document()
    
    with doc.div():
        doc.br()
        doc.hr()
        doc.img(src="test.jpg")
    
    html = doc.render()
    assert "<br />" in html
    assert "<hr />" in html
    assert '<img src="test.jpg" />' in html


def test_tag_shortcuts() -> None:
    """Test that tag shortcuts work correctly."""
    doc = Document()
    
    with doc.div():
        with doc.h1():
            doc.text("Title")
        with doc.p():
            doc.text("Paragraph")
    
    html = doc.render()
    assert "<div>" in html
    assert "<h1>Title</h1>" in html
    assert "<p>Paragraph</p>" in html
    assert "</div>" in html


def test_attr_function() -> None:
    """Test the attr() function for dynamic attribute addition."""
    doc = Document()
    
    with doc.div():
        doc.attr("class", "container")
        doc.attr("id", "main")
        doc.text("Content")
    
    html = doc.render()
    assert '<div class="container" id="main">Content</div>' == html


def test_document_reuse() -> None:
    """Test that documents can be cleared and reused."""
    doc = Document()
    
    with doc.p():
        doc.text("First")
    html1 = doc.render()
    
    doc.clear()
    with doc.h1():
        doc.text("Second")
    html2 = doc.render()
    
    assert html1 == "<p>First</p>"
    assert html2 == "<h1>Second</h1>"
