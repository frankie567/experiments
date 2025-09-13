#!/usr/bin/env python3
"""
Optimized Tagflow implementations to reduce performance bottlenecks.

This module contains several optimized versions of Tagflow functionality,
each targeting specific performance issues identified through profiling.
"""

import re
import time
from typing import Any, List, Union, Optional, Dict
from contextlib import contextmanager
from contextvars import ContextVar
import xml.etree.ElementTree as ET


# Fast attribute name conversion cache
_attr_name_cache: Dict[str, str] = {}

def cached_attr_name_to_xml(name: str) -> str:
    """Cached version of attribute name conversion"""
    if name not in _attr_name_cache:
        if name == "classes" or name == "class_":
            _attr_name_cache[name] = "class"
        else:
            _attr_name_cache[name] = re.sub(r"(\w)_(\w)", r"\1-\2", name)
    return _attr_name_cache[name]


class FastStringBuilder:
    """
    Fast HTML string builder that avoids ElementTree overhead.
    Uses direct string concatenation for maximum performance.
    """
    
    def __init__(self):
        self.parts: List[str] = []
        self.tag_stack: List[str] = []
    
    def open_tag(self, tag_name: str, attrs: Dict[str, str] = None, self_closing: bool = False):
        """Add an opening tag"""
        if attrs:
            attr_str = " " + " ".join(f'{k}="{v}"' for k, v in attrs.items())
        else:
            attr_str = ""
        
        if self_closing:
            self.parts.append(f"<{tag_name}{attr_str} />")
        else:
            self.parts.append(f"<{tag_name}{attr_str}>")
            self.tag_stack.append(tag_name)
    
    def close_tag(self):
        """Close the most recent tag"""
        if self.tag_stack:
            tag_name = self.tag_stack.pop()
            self.parts.append(f"</{tag_name}>")
    
    def add_text(self, text: str):
        """Add text content"""
        # Simple HTML escaping
        escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        self.parts.append(escaped)
    
    def to_string(self) -> str:
        """Get the final HTML string"""
        return "".join(self.parts)


class OptimizedStaticTagflow:
    """
    Optimized Tagflow implementation for static HTML generation.
    
    Key optimizations:
    1. Disables mutation recording
    2. Uses string concatenation instead of ElementTree
    3. Reduces context variable usage
    4. Caches attribute conversions
    5. Skips ID generation
    """
    
    def __init__(self):
        self.builder = FastStringBuilder()
        self._current_builder: ContextVar[FastStringBuilder] = ContextVar('builder')
    
    @contextmanager
    def document(self):
        """Create a document context"""
        token = self._current_builder.set(self.builder)
        try:
            yield self
        finally:
            self._current_builder.reset(token)
    
    @contextmanager 
    def tag(self, tag_name: str, **attrs):
        """Create a tag context manager"""
        builder = self._current_builder.get()
        
        # Process attributes efficiently
        processed_attrs = {}
        for k, v in attrs.items():
            if v is None or v is False:
                continue
            xml_name = cached_attr_name_to_xml(k)
            if v is True:
                processed_attrs[xml_name] = ""
            else:
                processed_attrs[xml_name] = str(v)
        
        builder.open_tag(tag_name, processed_attrs)
        try:
            yield
        finally:
            builder.close_tag()
    
    def text(self, content: str):
        """Add text content"""
        builder = self._current_builder.get()
        builder.add_text(content)
    
    def to_html(self) -> str:
        """Get the final HTML"""
        return self.builder.to_string()
    
    def __str__(self) -> str:
        return self.to_html()


class OptimizedElementTreeTagflow:
    """
    Optimized ElementTree-based Tagflow that keeps the DOM structure
    but removes unnecessary overhead.
    
    Key optimizations:
    1. Disables mutation recording for static mode
    2. Skips ID generation unless needed
    3. Reduces context variable calls
    4. Optimizes attribute processing
    """
    
    def __init__(self, static_mode: bool = True):
        self.static_mode = static_mode
        self.element = ET.Element("fragment")
        self._current_element: ContextVar[ET.Element] = ContextVar('element')
    
    @contextmanager
    def document(self):
        """Create a document context"""
        token = self._current_element.set(self.element)
        try:
            yield self
        finally:
            self._current_element.reset(token)
    
    @contextmanager
    def tag(self, tag_name: str, **attrs):
        """Create a tag context manager"""
        parent = self._current_element.get()
        
        # Process attributes efficiently - batch operation
        processed_attrs = {}
        for k, v in attrs.items():
            if v is None or v is False:
                continue
            xml_name = cached_attr_name_to_xml(k)
            if v is True:
                processed_attrs[xml_name] = ""
            else:
                processed_attrs[xml_name] = str(v)
        
        # Create element once with all attributes
        element = ET.SubElement(parent, tag_name, attrib=processed_attrs)
        
        # Set context
        token = self._current_element.set(element)
        try:
            yield element
        finally:
            self._current_element.reset(token)
    
    def text(self, content: str):
        """Add text content"""
        current_el = self._current_element.get()
        if len(current_el) > 0:
            # Add to tail of last child
            last_child = current_el[-1]
            old_tail = last_child.tail or ""
            last_child.tail = old_tail + content
        else:
            # Add to text of current element
            old_text = current_el.text or ""
            current_el.text = old_text + content
    
    def to_html(self) -> str:
        """Convert to HTML string"""
        if len(self.element) == 0:
            return ""
        return "".join(
            ET.tostring(child, encoding="unicode", method="html")
            for child in self.element
        )
    
    def __str__(self) -> str:
        return self.to_html()


class CachedTagflow:
    """
    Tagflow with aggressive caching optimizations.
    
    Key optimizations:
    1. Caches frequently used attribute conversions
    2. Pre-compiles common tag patterns
    3. Reuses ElementTree structures where possible
    """
    
    def __init__(self):
        self.element = ET.Element("fragment")
        self._current_element: ContextVar[ET.Element] = ContextVar('element')
        self._tag_cache: Dict[tuple, ET.Element] = {}
    
    @contextmanager
    def document(self):
        """Create a document context"""
        token = self._current_element.set(self.element)
        try:
            yield self
        finally:
            self._current_element.reset(token)
    
    def _create_cached_element(self, tag_name: str, attrs_tuple: tuple) -> ET.Element:
        """Create or reuse cached element"""
        cache_key = (tag_name, attrs_tuple)
        if cache_key in self._tag_cache:
            # Clone the cached element
            cached = self._tag_cache[cache_key]
            new_element = ET.Element(cached.tag, attrib=dict(cached.attrib))
            return new_element
        else:
            # Create new and cache
            attrs_dict = dict(attrs_tuple) if attrs_tuple else {}
            element = ET.Element(tag_name, attrib=attrs_dict)
            self._tag_cache[cache_key] = element
            return ET.Element(tag_name, attrib=attrs_dict)
    
    @contextmanager
    def tag(self, tag_name: str, **attrs):
        """Create a tag context manager with caching"""
        parent = self._current_element.get()
        
        # Process attributes efficiently
        processed_attrs = []
        for k, v in attrs.items():
            if v is None or v is False:
                continue
            xml_name = cached_attr_name_to_xml(k)
            if v is True:
                processed_attrs.append((xml_name, ""))
            else:
                processed_attrs.append((xml_name, str(v)))
        
        attrs_tuple = tuple(sorted(processed_attrs))
        element = self._create_cached_element(tag_name, attrs_tuple)
        parent.append(element)
        
        token = self._current_element.set(element)
        try:
            yield element
        finally:
            self._current_element.reset(token)
    
    def text(self, content: str):
        """Add text content"""
        current_el = self._current_element.get()
        if len(current_el) > 0:
            last_child = current_el[-1]
            old_tail = last_child.tail or ""
            last_child.tail = old_tail + content
        else:
            old_text = current_el.text or ""
            current_el.text = old_text + content
    
    def to_html(self) -> str:
        """Convert to HTML string"""
        if len(self.element) == 0:
            return ""
        return "".join(
            ET.tostring(child, encoding="unicode", method="html")
            for child in self.element
        )
    
    def __str__(self) -> str:
        return self.to_html()


# Convenience functions for each implementation
def create_optimized_static():
    """Create an optimized static Tagflow instance"""
    return OptimizedStaticTagflow()

def create_optimized_elementtree():
    """Create an optimized ElementTree Tagflow instance"""
    return OptimizedElementTreeTagflow()

def create_cached_tagflow():
    """Create a cached Tagflow instance"""
    return CachedTagflow()


if __name__ == "__main__":
    # Quick test of optimized implementations
    print("Testing optimized Tagflow implementations...")
    
    # Test static implementation
    static = create_optimized_static()
    with static.document():
        with static.tag("html"):
            with static.tag("body"):
                with static.tag("h1"):
                    static.text("Hello World")
    
    print("Static implementation works!")
    print(f"Output: {static}")
    
    # Test ElementTree implementation
    et = create_optimized_elementtree()
    with et.document():
        with et.tag("html"):
            with et.tag("body"):
                with et.tag("h1"):
                    et.text("Hello World")
    
    print("ElementTree implementation works!")
    print(f"Output: {et}")