# Demo PyO3 Extension

This is a demo project showing how to use the hatchling-pyo3-plugin to build PyO3 Rust extensions with Hatchling.

## Project Structure

- `Cargo.toml` - Rust project configuration
- `src/lib.rs` - Rust source code with PyO3 bindings
- `demo_pyo3_extension/` - Python package directory
- `pyproject.toml` - Python project configuration using hatchling-pyo3-plugin

## Building

```bash
# Build the package (will compile Rust extension)
pip install build
python -m build

# Or install in editable mode (for development)
pip install -e .
```

## Usage

```python
from demo_pyo3_extension import add, multiply, greet

print(add(5, 3))           # 8
print(multiply(4, 7))      # 28
print(greet("World"))      # "Hello, World!"
```

## Testing

```bash
python test_demo.py
```
