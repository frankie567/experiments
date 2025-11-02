# Hatchling PyO3 Build Plugin

This experiment implements a [Hatchling](https://hatch.pypa.io/) build hook plugin for building [PyO3](https://github.com/PyO3/pyo3) Rust extensions.

## Overview

PyO3 is a popular framework for creating Python bindings to Rust code. While [Maturin](https://github.com/PyO3/maturin) is the recommended build backend for PyO3 projects, this plugin enables PyO3 extensions to be built using Hatchling as an alternative build backend.

This is inspired by [setuptools-rust](https://github.com/PyO3/setuptools-rust), which provides similar functionality for setuptools.

## Features

- ✅ Build PyO3 Rust extensions as part of the Hatchling build process
- ✅ Automatic detection of Cargo.toml
- ✅ Cross-platform support (Linux, macOS, Windows)
- ✅ Configurable build profiles (release/debug)
- ✅ Custom Cargo arguments support
- ✅ Integration with standard Python packaging workflow
- ✅ No need to learn Maturin - uses familiar Hatchling tools

## Usage

### Installation

Add the plugin to your `pyproject.toml`:

```toml
[build-system]
requires = ["hatchling", "hatchling-pyo3-plugin"]
build-backend = "hatchling.build"

[tool.hatch.build.hooks.pyo3]
# Plugin will automatically detect and build Rust extensions
```

### Project Structure

```
my-project/
├── pyproject.toml
├── Cargo.toml          # Rust project configuration
├── src/
│   └── lib.rs          # Rust source code with PyO3 bindings
└── my_package/
    └── __init__.py     # Python package
```

### Example pyproject.toml

```toml
[build-system]
requires = ["hatchling", "hatchling-pyo3-plugin"]
build-backend = "hatchling.build"

[project]
name = "my-pyo3-project"
version = "0.1.0"
description = "A project with PyO3 extensions"
requires-python = ">=3.8"

[tool.hatch.build.hooks.pyo3]
# Optional: specify Rust extensions explicitly
# If not specified, plugin will look for Cargo.toml in project root

# Optional configuration:
# cargo-manifest = "Cargo.toml"  # Path to Cargo.toml (default: "Cargo.toml")
# profile = "release"            # Build profile (default: "release", can be "debug")
# target-dir = "target"          # Cargo target directory (default: "target")
# cargo-args = ["--features", "special"]  # Additional cargo arguments
```

## Implementation Details

The plugin:
1. Implements Hatchling's `BuildHookInterface`
2. Detects Rust extensions via `Cargo.toml`
3. Builds Rust code using `cargo build --release` (or custom profile)
4. Automatically handles platform-specific naming (`.so`, `.dylib`, `.dll`, `.pyd`)
5. Copies the compiled libraries to the Python package in the wheel

Platform-specific handling:
- **Linux**: `libname.so` → `name.so`
- **macOS**: `libname.dylib` → `name.so`
- **Windows**: `name.dll` → `name.pyd`

## Demo

The `demo/` directory contains a working example with:
- Simple PyO3 functions: `add()`, `multiply()`, `greet()`
- Comprehensive test suite
- Example build output

To try it:
```bash
cd demo
python -m build --wheel --no-isolation
pip install dist/demo_pyo3_extension-*.whl
python test_comprehensive.py
```

## Documentation

- [CONFIGURATION.md](./CONFIGURATION.md) - Configuration options and examples
- [SUMMARY.md](./SUMMARY.md) - Implementation details and architecture
- [BUILD_OUTPUT.md](./BUILD_OUTPUT.md) - Example build and test output

## References

- [Hatchling Build Hook Reference](https://hatch.pypa.io/latest/plugins/build-hook/reference/)
- [PyO3 Documentation](https://pyo3.rs/)
- [setuptools-rust](https://github.com/PyO3/setuptools-rust)
