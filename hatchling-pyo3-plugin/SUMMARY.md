# Hatchling PyO3 Plugin Implementation Summary

## Overview

This experiment successfully implements a Hatchling build hook plugin for building PyO3 Rust extensions. The plugin enables developers to use Hatchling (the standard Python build backend) instead of Maturin for building PyO3 projects.

## Architecture

### Plugin Structure

```
hatchling_pyo3_plugin/
├── __init__.py          # Package initialization
└── hooks.py             # Main build hook implementation
```

### Key Components

1. **PyO3BuildHook Class**: Implements Hatchling's `BuildHookInterface`
   - Inherits from `BuildHookInterface`
   - Registers as "pyo3" plugin via entry point
   - Implements `initialize()` method called during build

2. **Build Process**:
   ```
   initialize() → _build_rust_extension() → _add_rust_artifacts()
   ```

   - **initialize()**: Entry point called by Hatchling
   - **_build_rust_extension()**: Runs `cargo build --release`
   - **_add_rust_artifacts()**: Copies compiled `.so`/`.pyd` to wheel

### Integration with Hatchling

The plugin registers via `pyproject.toml` entry points:

```toml
[project.entry-points.hatch]
pyo3 = "hatchling_pyo3_plugin.hooks"
```

Projects use it by:
1. Adding to `build-system.requires`
2. Enabling in `[tool.hatch.build.hooks.pyo3]`

## Demo Project

The `demo/` directory contains a working example:

### Rust Extension (`src/lib.rs`)
- Simple PyO3 module with three functions:
  - `add(a, b)` - Addition
  - `multiply(a, b)` - Multiplication  
  - `greet(name)` - String formatting

### Python Package
- Standard Python package structure
- Imports Rust extension functions
- Graceful fallback if extension not built

### Build Configuration
```toml
[build-system]
requires = ["hatchling", "hatchling-pyo3-plugin"]
build-backend = "hatchling.build"

[tool.hatch.build.hooks.pyo3]
# Plugin auto-detects Cargo.toml
```

## Build Process

1. **Detection**: Plugin looks for `Cargo.toml` in project root
2. **Compilation**: Runs `cargo build --release`
3. **Artifact Collection**: Finds compiled library in `target/release/`
4. **Packaging**: Adds `.so`/`.pyd` to wheel via `force_include`

## Platform Support

The plugin handles platform-specific library extensions:

- **Linux**: `.so` files
- **macOS**: `.dylib` → `.so`
- **Windows**: `.pyd` files

## Testing

Verified with:
- Build process completes successfully
- Wheel contains compiled extension
- Extension functions work correctly
- All tests pass

## Advantages Over Maturin

1. **Standard Build Backend**: Uses Hatchling (PEP 517 compliant)
2. **Familiar Workflow**: Standard Python packaging tools
3. **Flexibility**: Works with existing Hatchling projects
4. **Integration**: Seamless with Hatchling ecosystem

## Limitations

1. Currently requires `--no-isolation` for local development
2. Plugin needs to be published to PyPI for general use
3. Advanced Maturin features not yet implemented

## Future Enhancements

Potential improvements:
- Configuration options for Cargo features
- Custom target directory support
- Multiple extension support
- Conditional compilation
- Cross-compilation support
- Parallel builds

## Comparison with setuptools-rust

Similar to `setuptools-rust` but for Hatchling:
- Both wrap Cargo builds
- Both handle artifact copying
- Hatchling plugin is simpler (no C++ mixing)
- More modern packaging approach

## Key Learnings

1. **Hatchling Hooks**: Simple interface with `initialize()` + `build_data`
2. **PyO3 Output**: Produces platform-specific shared libraries
3. **Artifact Management**: `force_include` for adding compiled files
4. **Build Isolation**: Need to handle PyPI availability

## Conclusion

The plugin successfully demonstrates that PyO3 extensions can be built with Hatchling. It provides a viable alternative to Maturin for projects preferring a standard Python build backend.
