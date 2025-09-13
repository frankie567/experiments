#!/usr/bin/env python3
"""
Tagflow Reimplementation - A minimal, efficient HTML generation library.

This module provides a clean context manager API for building HTML documents
with focus on performance and simplicity. It avoids the overhead of XML parsing,
context variables, and complex state management found in the original Tagflow.

Key features:
- Direct string building for maximum performance
- Explicit document objects (no globals)
- Full type annotations with modern Python syntax
- Minimal overhead context managers
- Proper HTML escaping and attribute handling
- Shortcuts for common HTML tags (h1, div, p, etc.)
"""

from __future__ import annotations

import html
import re
from contextlib import contextmanager
from typing import Any, Iterator

__all__ = ["Document"]

# Pre-compiled regex for attribute name conversion
_ATTR_NAME_PATTERN = re.compile(r"(\w)_(\w)")

# Cache for attribute name conversions to avoid repeated regex operations
_ATTR_NAME_CACHE: dict[str, str] = {}


def _convert_attr_name(name: str) -> str:
    """Convert Python attribute names to HTML attribute names.
    
    Examples:
        data_value -> data-value
        aria_label -> aria-label
        class_ -> class
        classes -> class
    """
    if name not in _ATTR_NAME_CACHE:
        if name in ("class_", "classes"):
            _ATTR_NAME_CACHE[name] = "class"
        elif name.endswith("_"):
            # Remove trailing underscore for reserved keywords
            _ATTR_NAME_CACHE[name] = name[:-1]
        else:
            # Convert underscores to hyphens (e.g., data_value -> data-value)
            _ATTR_NAME_CACHE[name] = _ATTR_NAME_PATTERN.sub(r"\1-\2", name)
    return _ATTR_NAME_CACHE[name]


def _escape_attr_value(value: Any) -> str:
    """Escape an attribute value for safe HTML output."""
    if value is None:
        return ""
    return html.escape(str(value), quote=True)


def _escape_text(text: Any) -> str:
    """Escape text content for safe HTML output."""
    if text is None:
        return ""
    return html.escape(str(text), quote=False)


class _TagContext:
    """Context manager for HTML tags.
    
    This is a lightweight object that handles opening and closing tags
    with minimal overhead.
    """
    
    __slots__ = ("_document", "_tag_name", "_self_closing")
    
    def __init__(self, document: Document, tag_name: str, self_closing: bool = False) -> None:
        self._document = document
        self._tag_name = tag_name
        self._self_closing = self_closing
    
    def __enter__(self) -> _TagContext:
        if not self._self_closing:
            self._document._tag_stack.append(self._tag_name)
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if not self._self_closing:
            closing_tag = self._document._tag_stack.pop()
            self._document._parts.append(f"</{closing_tag}>")


class Document:
    """A minimal HTML document builder with context manager support.
    
    This class provides an efficient way to build HTML documents using
    context managers, similar to the original Tagflow but with significant
    performance optimizations.
    
    The Document class includes shortcuts for common HTML tags, allowing
    for more concise and readable code.
    
    Example:
        doc = Document()
        with doc.tag("html"):
            with doc.tag("head"):
                with doc.tag("title"):
                    doc.text("Hello World")
            with doc.tag("body"):
                with doc.h1(class_="title"):  # Shortcut for doc.tag("h1", ...)
                    doc.text("Welcome!")
                with doc.div(class_="content"):
                    with doc.p():
                        doc.text("This is a paragraph.")
        
        html_output = doc.render()
    """
    
    __slots__ = ("_parts", "_tag_stack")
    
    def __init__(self) -> None:
        """Initialize an empty document."""
        self._parts: list[str] = []
        self._tag_stack: list[str] = []
    
    def tag(self, tag_name: str, **attrs: Any) -> _TagContext:
        """Create a tag context manager.
        
        Args:
            tag_name: The HTML tag name (e.g., "div", "p", "img")
            **attrs: HTML attributes as keyword arguments
        
        Returns:
            A context manager that handles opening and closing the tag
        
        Example:
            with doc.tag("div", class_="container", data_value="123"):
                doc.text("Content")
        """
        # Check for self-closing tags
        self_closing = tag_name.lower() in {
            "area", "base", "br", "col", "embed", "hr", "img", "input",
            "link", "meta", "param", "source", "track", "wbr"
        }
        
        # Build the opening tag
        if attrs:
            attr_str = " " + " ".join(
                f'{_convert_attr_name(k)}="{_escape_attr_value(v)}"'
                for k, v in attrs.items()
                if v is not None
            )
        else:
            attr_str = ""
        
        if self_closing:
            self._parts.append(f"<{tag_name}{attr_str} />")
        else:
            self._parts.append(f"<{tag_name}{attr_str}>")
        
        return _TagContext(self, tag_name, self_closing)
    
    def text(self, content: Any) -> None:
        """Add text content to the document.
        
        Args:
            content: The text content to add (will be escaped for safety)
        
        Example:
            doc.text("Hello & welcome!")  # Becomes "Hello &amp; welcome!"
        """
        if content is not None:
            self._parts.append(_escape_text(content))
    
    def raw(self, content: Any) -> None:
        """Add raw HTML content to the document without escaping.
        
        WARNING: This method does not escape content. Only use with trusted input.
        
        Args:
            content: The raw HTML content to add
        
        Example:
            doc.raw("<em>Already formatted</em>")
        """
        if content is not None:
            self._parts.append(str(content))
    
    def render(self) -> str:
        """Render the document to an HTML string.
        
        Returns:
            The complete HTML document as a string
        
        Raises:
            RuntimeError: If there are unclosed tags
        """
        if self._tag_stack:
            unclosed = ", ".join(self._tag_stack)
            raise RuntimeError(f"Unclosed tags: {unclosed}")
        
        return "".join(self._parts)
    
    def clear(self) -> None:
        """Clear the document content, allowing reuse of the same Document object."""
        self._parts.clear()
        self._tag_stack.clear()
    
    def __str__(self) -> str:
        """Return the rendered HTML when converting to string."""
        return self.render()
    
    # Shortcut methods for common HTML tags
    
    def div(self, **attrs: Any) -> _TagContext:
        """Create a div tag. Shortcut for tag('div', **attrs)."""
        return self.tag("div", **attrs)
    
    def p(self, **attrs: Any) -> _TagContext:
        """Create a p tag. Shortcut for tag('p', **attrs)."""
        return self.tag("p", **attrs)
    
    def span(self, **attrs: Any) -> _TagContext:
        """Create a span tag. Shortcut for tag('span', **attrs)."""
        return self.tag("span", **attrs)
    
    def h1(self, **attrs: Any) -> _TagContext:
        """Create an h1 tag. Shortcut for tag('h1', **attrs)."""
        return self.tag("h1", **attrs)
    
    def h2(self, **attrs: Any) -> _TagContext:
        """Create an h2 tag. Shortcut for tag('h2', **attrs)."""
        return self.tag("h2", **attrs)
    
    def h3(self, **attrs: Any) -> _TagContext:
        """Create an h3 tag. Shortcut for tag('h3', **attrs)."""
        return self.tag("h3", **attrs)
    
    def h4(self, **attrs: Any) -> _TagContext:
        """Create an h4 tag. Shortcut for tag('h4', **attrs)."""
        return self.tag("h4", **attrs)
    
    def h5(self, **attrs: Any) -> _TagContext:
        """Create an h5 tag. Shortcut for tag('h5', **attrs)."""
        return self.tag("h5", **attrs)
    
    def h6(self, **attrs: Any) -> _TagContext:
        """Create an h6 tag. Shortcut for tag('h6', **attrs)."""
        return self.tag("h6", **attrs)
    
    def a(self, **attrs: Any) -> _TagContext:
        """Create an a tag. Shortcut for tag('a', **attrs)."""
        return self.tag("a", **attrs)
    
    def button(self, **attrs: Any) -> _TagContext:
        """Create a button tag. Shortcut for tag('button', **attrs)."""
        return self.tag("button", **attrs)
    
    def form(self, **attrs: Any) -> _TagContext:
        """Create a form tag. Shortcut for tag('form', **attrs)."""
        return self.tag("form", **attrs)
    
    def input(self, **attrs: Any) -> _TagContext:
        """Create an input tag. Shortcut for tag('input', **attrs)."""
        return self.tag("input", **attrs)
    
    def label(self, **attrs: Any) -> _TagContext:
        """Create a label tag. Shortcut for tag('label', **attrs)."""
        return self.tag("label", **attrs)
    
    def select(self, **attrs: Any) -> _TagContext:
        """Create a select tag. Shortcut for tag('select', **attrs)."""
        return self.tag("select", **attrs)
    
    def option(self, **attrs: Any) -> _TagContext:
        """Create an option tag. Shortcut for tag('option', **attrs)."""
        return self.tag("option", **attrs)
    
    def textarea(self, **attrs: Any) -> _TagContext:
        """Create a textarea tag. Shortcut for tag('textarea', **attrs)."""
        return self.tag("textarea", **attrs)
    
    def ul(self, **attrs: Any) -> _TagContext:
        """Create a ul tag. Shortcut for tag('ul', **attrs)."""
        return self.tag("ul", **attrs)
    
    def ol(self, **attrs: Any) -> _TagContext:
        """Create an ol tag. Shortcut for tag('ol', **attrs)."""
        return self.tag("ol", **attrs)
    
    def li(self, **attrs: Any) -> _TagContext:
        """Create a li tag. Shortcut for tag('li', **attrs)."""
        return self.tag("li", **attrs)
    
    def table(self, **attrs: Any) -> _TagContext:
        """Create a table tag. Shortcut for tag('table', **attrs)."""
        return self.tag("table", **attrs)
    
    def thead(self, **attrs: Any) -> _TagContext:
        """Create a thead tag. Shortcut for tag('thead', **attrs)."""
        return self.tag("thead", **attrs)
    
    def tbody(self, **attrs: Any) -> _TagContext:
        """Create a tbody tag. Shortcut for tag('tbody', **attrs)."""
        return self.tag("tbody", **attrs)
    
    def tr(self, **attrs: Any) -> _TagContext:
        """Create a tr tag. Shortcut for tag('tr', **attrs)."""
        return self.tag("tr", **attrs)
    
    def td(self, **attrs: Any) -> _TagContext:
        """Create a td tag. Shortcut for tag('td', **attrs)."""
        return self.tag("td", **attrs)
    
    def th(self, **attrs: Any) -> _TagContext:
        """Create a th tag. Shortcut for tag('th', **attrs)."""
        return self.tag("th", **attrs)
    
    def section(self, **attrs: Any) -> _TagContext:
        """Create a section tag. Shortcut for tag('section', **attrs)."""
        return self.tag("section", **attrs)
    
    def article(self, **attrs: Any) -> _TagContext:
        """Create an article tag. Shortcut for tag('article', **attrs)."""
        return self.tag("article", **attrs)
    
    def header(self, **attrs: Any) -> _TagContext:
        """Create a header tag. Shortcut for tag('header', **attrs)."""
        return self.tag("header", **attrs)
    
    def footer(self, **attrs: Any) -> _TagContext:
        """Create a footer tag. Shortcut for tag('footer', **attrs)."""
        return self.tag("footer", **attrs)
    
    def nav(self, **attrs: Any) -> _TagContext:
        """Create a nav tag. Shortcut for tag('nav', **attrs)."""
        return self.tag("nav", **attrs)
    
    def main(self, **attrs: Any) -> _TagContext:
        """Create a main tag. Shortcut for tag('main', **attrs)."""
        return self.tag("main", **attrs)
    
    def aside(self, **attrs: Any) -> _TagContext:
        """Create an aside tag. Shortcut for tag('aside', **attrs)."""
        return self.tag("aside", **attrs)
    
    def strong(self, **attrs: Any) -> _TagContext:
        """Create a strong tag. Shortcut for tag('strong', **attrs)."""
        return self.tag("strong", **attrs)
    
    def em(self, **attrs: Any) -> _TagContext:
        """Create an em tag. Shortcut for tag('em', **attrs)."""
        return self.tag("em", **attrs)
    
    def code(self, **attrs: Any) -> _TagContext:
        """Create a code tag. Shortcut for tag('code', **attrs)."""
        return self.tag("code", **attrs)
    
    def pre(self, **attrs: Any) -> _TagContext:
        """Create a pre tag. Shortcut for tag('pre', **attrs)."""
        return self.tag("pre", **attrs)
    
    def img(self, **attrs: Any) -> _TagContext:
        """Create an img tag. Shortcut for tag('img', **attrs)."""
        return self.tag("img", **attrs)
    
    def br(self, **attrs: Any) -> _TagContext:
        """Create a br tag. Shortcut for tag('br', **attrs)."""
        return self.tag("br", **attrs)
    
    def hr(self, **attrs: Any) -> _TagContext:
        """Create an hr tag. Shortcut for tag('hr', **attrs)."""
        return self.tag("hr", **attrs)


# Convenience function for creating documents
def document() -> Document:
    """Create a new Document instance.
    
    This function provides a more familiar API for users coming from
    the original Tagflow library.
    
    Returns:
        A new Document instance
    
    Example:
        doc = document()
        with doc.tag("html"):
            # ... build document
    """
    return Document()