"""Tests for DocumentResponse."""

from prev import Document, DocumentResponse


def test_document_response_basic() -> None:
    """Test basic DocumentResponse functionality."""
    doc = Document()
    
    with doc.tag("html"):
        with doc.tag("body"):
            with doc.h1():
                doc.text("Test")
    
    response = DocumentResponse(doc)
    
    assert response.status_code == 200
    assert response.media_type == "text/html"
    assert b"<html><body><h1>Test</h1></body></html>" == response.body


def test_document_response_custom_status() -> None:
    """Test DocumentResponse with custom status code."""
    doc = Document()
    
    with doc.p():
        doc.text("Not Found")
    
    response = DocumentResponse(doc, status_code=404)
    
    assert response.status_code == 404


def test_document_response_custom_headers() -> None:
    """Test DocumentResponse with custom headers."""
    doc = Document()
    
    with doc.p():
        doc.text("Content")
    
    response = DocumentResponse(doc, headers={"X-Custom": "Value"})
    
    assert response.headers["x-custom"] == "Value"
