use pyo3::prelude::*;
use pyo3::exceptions::PyRuntimeError;
use pyo3::types::{PyDict, PyString};
use std::collections::HashMap;
use regex::Regex;
use once_cell::sync::Lazy;

// Pre-compiled regex for attribute name conversion
static ATTR_NAME_PATTERN: Lazy<Regex> = Lazy::new(|| {
    Regex::new(r"(\w)_(\w)").unwrap()
});

/// Convert Python attribute names to HTML attribute names
fn convert_attr_name(name: &str) -> String {
    if name == "class_" || name == "classes" {
        "class".to_string()
    } else if name.ends_with('_') {
        // Remove trailing underscore for reserved keywords
        name[..name.len() - 1].to_string()
    } else {
        // Convert underscores to hyphens (e.g., data_value -> data-value)
        ATTR_NAME_PATTERN.replace_all(name, "$1-$2").to_string()
    }
}

/// Escape text content for safe HTML output
fn escape_text(text: &str) -> String {
    html_escape::encode_text(text).to_string()
}

/// Check if a tag is self-closing
fn is_self_closing(tag_name: &str) -> bool {
    matches!(tag_name.to_lowercase().as_str(), 
        "area" | "base" | "br" | "col" | "embed" | "hr" | "img" | "input" |
        "link" | "meta" | "param" | "source" | "track" | "wbr"
    )
}

/// Simple context manager for HTML tags
#[pyclass]
pub struct TagContext {
    pub tag_name: String,
    pub self_closing: bool,
}

#[pymethods]
impl TagContext {
    #[getter]
    fn self_closing(&self) -> bool {
        self.self_closing
    }

    fn __enter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }
    
    #[pyo3(signature = (_exc_type=None, _exc_val=None, _exc_tb=None))]
    fn __exit__(
        &self,
        _exc_type: Option<&Bound<'_, PyAny>>,
        _exc_val: Option<&Bound<'_, PyAny>>,
        _exc_tb: Option<&Bound<'_, PyAny>>,
    ) -> PyResult<bool> {
        Ok(false)
    }
}

/// Main document builder in Rust
#[pyclass]
pub struct Document {
    parts: Vec<String>,
    tag_stack: Vec<String>,
}

#[pymethods]
impl Document {
    #[new]
    fn new() -> Self {
        Document {
            parts: Vec::new(),
            tag_stack: Vec::new(),
        }
    }
    
    /// Create a tag context manager
    #[pyo3(signature = (tag_name, **kwargs))]
    fn tag(&mut self, tag_name: String, kwargs: Option<&Bound<'_, PyDict>>) -> PyResult<Py<TagContext>> {
        let mut attrs = HashMap::new();
        
        if let Some(kwargs) = kwargs {
            for item in kwargs.iter() {
                let (key, value) = item;
                let key_py_str = key.downcast::<PyString>()?;
                let key_str = key_py_str.to_str()?.to_string();
                let value_str = if value.is_none() {
                    String::new()
                } else {
                    let value_py_str = value.str()?;
                    value_py_str.to_str()?.to_string()
                };
                attrs.insert(key_str, value_str);
            }
        }
        
        let self_closing = is_self_closing(&tag_name);
        
        // Build the opening tag
        let mut attr_str = String::new();
        if !attrs.is_empty() {
            let attr_parts: Vec<String> = attrs.iter()
                .filter(|(_, v)| !v.is_empty())
                .map(|(k, v)| {
                    let converted_name = convert_attr_name(k);
                    format!("{}=\"{}\"", converted_name, html_escape::encode_double_quoted_attribute(v))
                })
                .collect();
            
            if !attr_parts.is_empty() {
                attr_str = format!(" {}", attr_parts.join(" "));
            }
        }
        
        let opening_tag = if self_closing {
            format!("<{}{} />", tag_name, attr_str)
        } else {
            format!("<{}{}>", tag_name, attr_str)
        };
        
        self.parts.push(opening_tag);
        
        if !self_closing {
            self.tag_stack.push(tag_name.clone());
        }
        
        Python::with_gil(|py| {
            Ok(Py::new(py, TagContext {
                tag_name,
                self_closing,
            })?)
        })
    }
    
    /// Add text content to the document
    fn text(&mut self, content: &Bound<'_, PyAny>) -> PyResult<()> {
        if !content.is_none() {
            let content_py_str = content.str()?;
            let content_str = content_py_str.to_str()?;
            let escaped = escape_text(content_str);
            self.parts.push(escaped);
        }
        Ok(())
    }
    
    /// Add raw HTML content to the document without escaping
    fn raw(&mut self, content: &Bound<'_, PyAny>) -> PyResult<()> {
        if !content.is_none() {
            let content_py_str = content.str()?;
            let content_str = content_py_str.to_str()?;
            self.parts.push(content_str.to_string());
        }
        Ok(())
    }
    
    /// Close the current tag
    fn close_tag(&mut self) -> PyResult<()> {
        if let Some(tag_name) = self.tag_stack.pop() {
            self.parts.push(format!("</{}>", tag_name));
        }
        Ok(())
    }
    
    /// Add an attribute to the current tag (simplified - not supported in this basic version)
    fn attr(&mut self, _name: String, _value: &Bound<'_, PyAny>) -> PyResult<()> {
        Err(PyRuntimeError::new_err(
            "Dynamic attributes not supported in this implementation. Use tag() arguments instead."
        ))
    }
    
    /// Render the document to an HTML string
    fn render(&self) -> PyResult<String> {
        if !self.tag_stack.is_empty() {
            let unclosed = self.tag_stack.join(", ");
            return Err(PyRuntimeError::new_err(format!("Unclosed tags: {}", unclosed)));
        }
        Ok(self.parts.join(""))
    }
    
    /// Clear the document content
    fn clear(&mut self) {
        self.parts.clear();
        self.tag_stack.clear();
    }
    
    fn __str__(&self) -> PyResult<String> {
        self.render()
    }
    
    // Tag shortcuts
    #[pyo3(signature = (**kwargs))]
    fn div(&mut self, kwargs: Option<&Bound<'_, PyDict>>) -> PyResult<Py<TagContext>> {
        self.tag("div".to_string(), kwargs)
    }
    
    #[pyo3(signature = (**kwargs))]
    fn p(&mut self, kwargs: Option<&Bound<'_, PyDict>>) -> PyResult<Py<TagContext>> {
        self.tag("p".to_string(), kwargs)
    }
    
    #[pyo3(signature = (**kwargs))]
    fn h1(&mut self, kwargs: Option<&Bound<'_, PyDict>>) -> PyResult<Py<TagContext>> {
        self.tag("h1".to_string(), kwargs)
    }
    
    #[pyo3(signature = (**kwargs))]
    fn h2(&mut self, kwargs: Option<&Bound<'_, PyDict>>) -> PyResult<Py<TagContext>> {
        self.tag("h2".to_string(), kwargs)
    }
    
    #[pyo3(signature = (**kwargs))]
    fn h3(&mut self, kwargs: Option<&Bound<'_, PyDict>>) -> PyResult<Py<TagContext>> {
        self.tag("h3".to_string(), kwargs)
    }
    
    #[pyo3(signature = (**kwargs))]
    fn span(&mut self, kwargs: Option<&Bound<'_, PyDict>>) -> PyResult<Py<TagContext>> {
        self.tag("span".to_string(), kwargs)
    }
    
    #[pyo3(signature = (**kwargs))]
    fn a(&mut self, kwargs: Option<&Bound<'_, PyDict>>) -> PyResult<Py<TagContext>> {
        self.tag("a".to_string(), kwargs)
    }
    
    #[pyo3(signature = (**kwargs))]
    fn ul(&mut self, kwargs: Option<&Bound<'_, PyDict>>) -> PyResult<Py<TagContext>> {
        self.tag("ul".to_string(), kwargs)
    }
    
    #[pyo3(signature = (**kwargs))]
    fn li(&mut self, kwargs: Option<&Bound<'_, PyDict>>) -> PyResult<Py<TagContext>> {
        self.tag("li".to_string(), kwargs)
    }
    
    #[pyo3(signature = (**kwargs))]
    fn table(&mut self, kwargs: Option<&Bound<'_, PyDict>>) -> PyResult<Py<TagContext>> {
        self.tag("table".to_string(), kwargs)
    }
    
    #[pyo3(signature = (**kwargs))]
    fn tr(&mut self, kwargs: Option<&Bound<'_, PyDict>>) -> PyResult<Py<TagContext>> {
        self.tag("tr".to_string(), kwargs)
    }
    
    #[pyo3(signature = (**kwargs))]
    fn td(&mut self, kwargs: Option<&Bound<'_, PyDict>>) -> PyResult<Py<TagContext>> {
        self.tag("td".to_string(), kwargs)
    }
    
    #[pyo3(signature = (**kwargs))]
    fn th(&mut self, kwargs: Option<&Bound<'_, PyDict>>) -> PyResult<Py<TagContext>> {
        self.tag("th".to_string(), kwargs)
    }
    
    #[pyo3(signature = (**kwargs))]
    fn thead(&mut self, kwargs: Option<&Bound<'_, PyDict>>) -> PyResult<Py<TagContext>> {
        self.tag("thead".to_string(), kwargs)
    }
    
    #[pyo3(signature = (**kwargs))]
    fn tbody(&mut self, kwargs: Option<&Bound<'_, PyDict>>) -> PyResult<Py<TagContext>> {
        self.tag("tbody".to_string(), kwargs)
    }
    
    // Self-closing tags
    #[pyo3(signature = (**kwargs))]
    fn img(&mut self, kwargs: Option<&Bound<'_, PyDict>>) -> PyResult<()> {
        self.tag("img".to_string(), kwargs)?;
        Ok(())
    }
    
    #[pyo3(signature = (**kwargs))]
    fn br(&mut self, kwargs: Option<&Bound<'_, PyDict>>) -> PyResult<()> {
        self.tag("br".to_string(), kwargs)?;
        Ok(())
    }
    
    #[pyo3(signature = (**kwargs))]
    fn hr(&mut self, kwargs: Option<&Bound<'_, PyDict>>) -> PyResult<()> {
        self.tag("hr".to_string(), kwargs)?;
        Ok(())
    }
}

/// Python module function
#[pymodule]
fn _tagflow_rust(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Document>()?;
    m.add_class::<TagContext>()?;
    
    // Convenience function for creating documents
    #[pyfn(m)]
    fn document() -> Document {
        Document::new()
    }
    
    Ok(())
}