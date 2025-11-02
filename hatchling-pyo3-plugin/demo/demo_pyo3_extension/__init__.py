"""Demo PyO3 Extension Package.

This package demonstrates a Rust extension built with PyO3 and the
hatchling-pyo3-plugin build hook.
"""

# The Rust extension will be loaded as demo_pyo3_extension.so
# Import it to make functions available at package level
try:
    from .demo_pyo3_extension import add, multiply, greet
    
    __all__ = ["add", "multiply", "greet"]
except ImportError as e:
    # Extension not built yet
    import warnings
    warnings.warn(f"Rust extension not available: {e}")
    __all__ = []

__version__ = "0.1.0"
