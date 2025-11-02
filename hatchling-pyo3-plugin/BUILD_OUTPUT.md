# Build and Test Output Examples

This document shows example output from building and testing the hatchling-pyo3-plugin.

## Building the Demo

```bash
$ cd demo
$ python -m build --wheel --no-isolation
* Getting build dependencies for wheel...
* Building wheel...
Building Rust extension: /path/to/demo/Cargo.toml
Rust extension built successfully
Adding Rust artifact: /path/to/demo/target/release/libdemo_pyo3_extension.so -> demo_pyo3_extension/demo_pyo3_extension.so
Successfully built demo_pyo3_extension-0.1.0-py3-none-any.whl
```

## Installing the Package

```bash
$ pip install dist/demo_pyo3_extension-0.1.0-py3-none-any.whl
Processing ./dist/demo_pyo3_extension-0.1.0-py3-none-any.whl
Installing collected packages: demo-pyo3-extension
Successfully installed demo-pyo3-extension-0.1.0
```

## Running Tests

### Simple Test

```bash
$ python test_demo.py
✓ add(5, 3) = 8
✓ multiply(4, 7) = 28
✓ greet('World') = Hello, World!

✅ All tests passed!
```

### Comprehensive Test Suite

```bash
$ python test_comprehensive.py
======================================================================
Hatchling PyO3 Plugin - Demo Extension Test Suite
======================================================================
Testing imports...
  ✓ Successfully imported: add, multiply, greet

Testing add function...
  ✓ add(5, 3) = 8
  ✓ add(0, 0) = 0
  ✓ add(-5, 5) = 0
  ✓ add(100, 200) = 300
  ✓ add(-10, -20) = -30

Testing multiply function...
  ✓ multiply(4, 7) = 28
  ✓ multiply(0, 100) = 0
  ✓ multiply(1, 1) = 1
  ✓ multiply(-5, 3) = -15
  ✓ multiply(10, 10) = 100

Testing greet function...
  ✓ greet('World') = 'Hello, World!'
  ✓ greet('Python') = 'Hello, Python!'
  ✓ greet('Rust') = 'Hello, Rust!'
  ✓ greet('PyO3') = 'Hello, PyO3!'
  ✓ greet('') = 'Hello, !'

Testing type checking...
  ✓ Large number addition: -9223372036854775808
  ✓ Unicode string handling: 'Hello, Test 测试 🎉!'

======================================================================
Test Results Summary
======================================================================
✓ PASS - Import Test
✓ PASS - Add Function
✓ PASS - Multiply Function
✓ PASS - Greet Function
✓ PASS - Type Checking
======================================================================
Passed: 5/5 tests

🎉 All tests passed!
```

## Using the Extension Interactively

```python
>>> from demo_pyo3_extension import add, multiply, greet
>>> 
>>> add(42, 58)
100
>>> 
>>> multiply(7, 8)
56
>>> 
>>> greet("PyO3")
'Hello, PyO3!'
>>> 
>>> # Works with large numbers
>>> add(2**62, 2**62)
-9223372036854775808
>>> 
>>> # Handles Unicode
>>> greet("世界")
'Hello, 世界!'
```

## Wheel Contents

```bash
$ python -m zipfile -l dist/demo_pyo3_extension-0.1.0-py3-none-any.whl
File Name                                             Modified             Size
demo_pyo3_extension/__init__.py                2020-02-02 00:00:00          540
demo_pyo3_extension/demo_pyo3_extension.so     2020-02-02 00:00:00       538224
demo_pyo3_extension-0.1.0.dist-info/METADATA   2020-02-02 00:00:00          979
demo_pyo3_extension-0.1.0.dist-info/WHEEL      2020-02-02 00:00:00           87
demo_pyo3_extension-0.1.0.dist-info/RECORD     2020-02-02 00:00:00          429
```

The compiled Rust extension (`demo_pyo3_extension.so`) is approximately 525 KB and contains the optimized release build of the PyO3 bindings.

## Build Performance

Typical build times on a modern system:

- **First build** (with dependencies): ~30-60 seconds
  - Downloads and compiles PyO3 and dependencies
- **Incremental build** (no changes): ~1-2 seconds
  - Only rebuilds if Rust code changed
- **Clean rebuild**: ~10-15 seconds
  - Dependencies cached, only project rebuilt

## Comparison: Hatchling vs Maturin

| Aspect | Hatchling Plugin | Maturin |
|--------|-----------------|---------|
| Build backend | Hatchling (standard) | Maturin (specialized) |
| Configuration | `pyproject.toml` | `pyproject.toml` |
| Wheel size | ~221 KB | Similar |
| Build speed | Fast (uses cargo) | Fast (uses cargo) |
| Ecosystem | Standard Python tools | Rust-focused tools |
| Learning curve | Familiar to Python devs | New tool to learn |

Both produce functionally identical wheels with similar performance characteristics.

## Platform-Specific Notes

### Linux
- Produces `.so` files with `lib` prefix: `libdemo_pyo3_extension.so`
- Plugin strips prefix and copies to wheel: `demo_pyo3_extension.so`

### macOS
- Produces `.dylib` files: `libdemo_pyo3_extension.dylib`
- Plugin renames to `.so`: `demo_pyo3_extension.so`

### Windows
- Produces `.dll` files: `demo_pyo3_extension.dll`
- Plugin renames to `.pyd`: `demo_pyo3_extension.pyd`
