"""
Tagflow Rust+PyO3 Implementation

A high-performance HTML generation library implemented in Rust with Python bindings.
This module provides the same API as the Python tagflow-reimplementation but with
Rust performance optimizations.
"""

from ._tagflow_rust import Document as _RustDocument, TagContext as _RustTagContext, document as _rust_document
from typing import Any, Dict, Iterator
import contextlib

__all__ = ["Document", "TagContext", "document"]

__version__ = "0.1.0"

# List of self-closing tags
_SELF_CLOSING_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr"
}

def _is_self_closing(tag_name: str) -> bool:
    """Check if a tag is self-closing."""
    return tag_name.lower() in _SELF_CLOSING_TAGS


class TagContext:
    """Python wrapper for Rust TagContext to provide proper context manager behavior."""
    
    def __init__(self, document: 'Document', rust_context, tag_name: str):
        self._document = document
        self._rust_context = rust_context
        self._tag_name = tag_name
        self._self_closing = _is_self_closing(tag_name)
        self._entered = False
    
    def __enter__(self) -> 'TagContext':
        self._entered = True
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._entered and not self._self_closing:
            self._document._rust_doc.close_tag()
        self._entered = False


class Document:
    """Python wrapper for Rust Document to provide full API compatibility."""
    
    def __init__(self):
        self._rust_doc = _RustDocument()
    
    def tag(self, tag_name: str, **attrs: Any) -> TagContext:
        """Create a tag context manager."""
        rust_context = self._rust_doc.tag(tag_name, **attrs)
        return TagContext(self, rust_context, tag_name)
    
    def text(self, content: Any) -> None:
        """Add text content to the document."""
        self._rust_doc.text(content)
    
    def raw(self, content: Any) -> None:
        """Add raw HTML content to the document without escaping."""
        self._rust_doc.raw(content)
    
    def attr(self, name: str, value: Any) -> None:
        """Add an attribute to the current tag (not supported in this simplified version)."""
        self._rust_doc.attr(name, value)
    
    def render(self) -> str:
        """Render the document to an HTML string."""
        return self._rust_doc.render()
    
    def clear(self) -> None:
        """Clear the document content."""
        self._rust_doc.clear()
    
    def __str__(self) -> str:
        """Return the rendered HTML when converting to string."""
        return self.render()
    
    # Tag shortcuts
    def div(self, **attrs: Any) -> TagContext:
        """Create a div tag. Shortcut for tag('div', **attrs)."""
        rust_context = self._rust_doc.div(**attrs)
        return TagContext(self, rust_context, "div")
    
    def p(self, **attrs: Any) -> TagContext:
        """Create a p tag. Shortcut for tag('p', **attrs)."""
        rust_context = self._rust_doc.p(**attrs)
        return TagContext(self, rust_context, "p")
    
    def span(self, **attrs: Any) -> TagContext:
        """Create a span tag. Shortcut for tag('span', **attrs)."""
        rust_context = self._rust_doc.span(**attrs)
        return TagContext(self, rust_context, "span")
    
    def h1(self, **attrs: Any) -> TagContext:
        """Create an h1 tag. Shortcut for tag('h1', **attrs)."""
        rust_context = self._rust_doc.h1(**attrs)
        return TagContext(self, rust_context, "h1")
    
    def h2(self, **attrs: Any) -> TagContext:
        """Create an h2 tag. Shortcut for tag('h2', **attrs)."""
        rust_context = self._rust_doc.h2(**attrs)
        return TagContext(self, rust_context, "h2")
    
    def h3(self, **attrs: Any) -> TagContext:
        """Create an h3 tag. Shortcut for tag('h3', **attrs)."""
        rust_context = self._rust_doc.h3(**attrs)
        return TagContext(self, rust_context, "h3")
    
    def a(self, **attrs: Any) -> TagContext:
        """Create an a tag. Shortcut for tag('a', **attrs)."""
        rust_context = self._rust_doc.a(**attrs)
        return TagContext(self, rust_context, "a")
    
    def ul(self, **attrs: Any) -> TagContext:
        """Create a ul tag. Shortcut for tag('ul', **attrs)."""
        rust_context = self._rust_doc.ul(**attrs)
        return TagContext(self, rust_context, "ul")
    
    def li(self, **attrs: Any) -> TagContext:
        """Create a li tag. Shortcut for tag('li', **attrs)."""
        rust_context = self._rust_doc.li(**attrs)
        return TagContext(self, rust_context, "li")
    
    def table(self, **attrs: Any) -> TagContext:
        """Create a table tag. Shortcut for tag('table', **attrs)."""
        rust_context = self._rust_doc.table(**attrs)
        return TagContext(self, rust_context, "table")
    
    def thead(self, **attrs: Any) -> TagContext:
        """Create a thead tag. Shortcut for tag('thead', **attrs)."""
        rust_context = self._rust_doc.thead(**attrs)
        return TagContext(self, rust_context, "thead")
    
    def tbody(self, **attrs: Any) -> TagContext:
        """Create a tbody tag. Shortcut for tag('tbody', **attrs)."""
        rust_context = self._rust_doc.tbody(**attrs)
        return TagContext(self, rust_context, "tbody")
    
    def tr(self, **attrs: Any) -> TagContext:
        """Create a tr tag. Shortcut for tag('tr', **attrs)."""
        rust_context = self._rust_doc.tr(**attrs)
        return TagContext(self, rust_context, "tr")
    
    def td(self, **attrs: Any) -> TagContext:
        """Create a td tag. Shortcut for tag('td', **attrs)."""
        rust_context = self._rust_doc.td(**attrs)
        return TagContext(self, rust_context, "td")
    
    def th(self, **attrs: Any) -> TagContext:
        """Create a th tag. Shortcut for tag('th', **attrs)."""
        rust_context = self._rust_doc.th(**attrs)
        return TagContext(self, rust_context, "th")
    
    # Self-closing tags
    def img(self, **attrs: Any) -> None:
        """Create an img tag. Shortcut for tag('img', **attrs)."""
        self._rust_doc.img(**attrs)
    
    def br(self, **attrs: Any) -> None:
        """Create a br tag. Shortcut for tag('br', **attrs)."""
        self._rust_doc.br(**attrs)
    
    def hr(self, **attrs: Any) -> None:
        """Create an hr tag. Shortcut for tag('hr', **attrs)."""
        self._rust_doc.hr(**attrs)


def document() -> Document:
    """Create a new Document instance.
    
    This function provides a more familiar API for users coming from
    the original Tagflow library.
    
    Returns:
        A new Document instance
    """
    return Document()