# Configuration Examples

This document shows various configuration options for the hatchling-pyo3-plugin.

## Basic Configuration

Minimal setup that auto-detects `Cargo.toml`:

```toml
[build-system]
requires = ["hatchling", "hatchling-pyo3-plugin"]
build-backend = "hatchling.build"

[project]
name = "my-project"
version = "0.1.0"

[tool.hatch.build.hooks.pyo3]
```

## Custom Cargo Manifest Path

If your `Cargo.toml` is in a non-standard location:

```toml
[tool.hatch.build.hooks.pyo3]
cargo-manifest = "rust/Cargo.toml"
```

## Debug Build

Build in debug mode for faster compilation during development:

```toml
[tool.hatch.build.hooks.pyo3]
profile = "debug"
```

## Custom Target Directory

Use a custom Cargo target directory:

```toml
[tool.hatch.build.hooks.pyo3]
target-dir = "build/rust"
```

## Additional Cargo Arguments

Pass extra arguments to `cargo build`:

```toml
[tool.hatch.build.hooks.pyo3]
cargo-args = ["--features", "special-feature", "--verbose"]
```

## Complete Example

All options together:

```toml
[build-system]
requires = ["hatchling", "hatchling-pyo3-plugin"]
build-backend = "hatchling.build"

[project]
name = "advanced-pyo3-project"
version = "0.1.0"
description = "Advanced PyO3 project with custom configuration"
requires-python = ">=3.8"

[tool.hatch.build.hooks.pyo3]
cargo-manifest = "Cargo.toml"
profile = "release"
target-dir = "target"
cargo-args = ["--features", "optimization,simd"]
```

## Multi-Platform Builds

The plugin automatically handles platform-specific library extensions:

- **Linux**: `.so` files
- **macOS**: `.dylib` → `.so` (renamed)
- **Windows**: `.pyd` files

No additional configuration needed for cross-platform support!
