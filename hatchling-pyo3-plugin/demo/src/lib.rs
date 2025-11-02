use pyo3::prelude::*;

/// A simple function that adds two numbers
#[pyfunction]
fn add(a: i64, b: i64) -> i64 {
    a + b
}

/// A simple function that multiplies two numbers
#[pyfunction]
fn multiply(a: i64, b: i64) -> i64 {
    a * b
}

/// Formats a greeting message
#[pyfunction]
fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

/// A Python module implemented in Rust using PyO3
#[pymodule]
fn demo_pyo3_extension(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(add, m)?)?;
    m.add_function(wrap_pyfunction!(multiply, m)?)?;
    m.add_function(wrap_pyfunction!(greet, m)?)?;
    Ok(())
}
