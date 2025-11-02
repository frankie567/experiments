# Architecture Overview

This document provides a visual overview of how the hatchling-pyo3-plugin works.

## Build Process Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         User runs build                         │
│                  python -m build --wheel                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Hatchling Build System                       │
│  1. Reads pyproject.toml                                        │
│  2. Discovers build hooks                                       │
│  3. Loads hatchling-pyo3-plugin                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              PyO3BuildHook.initialize() called                  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 1. Check if target is 'wheel' (skip for sdist)           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                   │
│                             ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 2. Look for Cargo.toml in project root                   │  │
│  │    (configurable via cargo-manifest option)              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                   │
│                             ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 3. Build Rust extension: _build_rust_extension()         │  │
│  │    - Run: cargo build --release --manifest-path ...      │  │
│  │    - Wait for compilation to complete                    │  │
│  │    - Handle build errors                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                   │
│                             ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 4. Find artifacts: _add_rust_artifacts()                 │  │
│  │    - Scan target/{profile}/ directory                    │  │
│  │    - Find .so/.dylib/.dll files                          │  │
│  │    - Platform-specific handling                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                   │
│                             ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 5. Add to wheel via build_data['force_include']          │  │
│  │    - Strip 'lib' prefix if present                       │  │
│  │    - Rename to Python extension format                   │  │
│  │    - Map: target/release/libname.so →                    │  │
│  │          package_name/name.so                            │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              Hatchling packages the wheel                       │
│  - Includes Python files from package                          │
│  - Includes compiled Rust extension from force_include         │
│  - Creates .whl file in dist/                                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Wheel ready for install                      │
│           demo_pyo3_extension-0.1.0-py3-none-any.whl           │
└─────────────────────────────────────────────────────────────────┘
```

## Component Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Project Structure                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  pyproject.toml ──────► Configures build system                │
│      │                  [build-system]                          │
│      │                  requires = ["hatchling",                │
│      │                              "hatchling-pyo3-plugin"]    │
│      │                  [tool.hatch.build.hooks.pyo3]           │
│      │                                                          │
│      │                                                          │
│  Cargo.toml ──────────► Rust project config                    │
│      │                  [package]                               │
│      │                  name = "my_extension"                   │
│      │                  [lib]                                   │
│      │                  crate-type = ["cdylib"]                 │
│      │                  [dependencies]                          │
│      │                  pyo3 = { version = "0.22",              │
│      │                          features = ["extension-module"]}│
│      │                                                          │
│      │                                                          │
│  src/lib.rs ──────────► PyO3 Rust code                         │
│      │                  #[pymodule]                             │
│      │                  fn my_extension(m: &Bound<PyModule>)    │
│      │                                                          │
│      │                                                          │
│  my_package/ ─────────► Python package                         │
│      │                  __init__.py                             │
│      │                  (imports extension)                     │
│      │                                                          │
└─────┴─────────────────────────────────────────────────────────┘
```

## Plugin Integration Points

```
Hatchling Core
      │
      │ discovers plugins via entry points
      ├─► [project.entry-points.hatch]
      │   pyo3 = "hatchling_pyo3_plugin.hooks"
      │
      │ calls build hooks
      ├─► BuildHookInterface.initialize()
      │        │
      │        └─► PyO3BuildHook.initialize()
      │                 │
      │                 ├─► _build_rust_extension()
      │                 │        │
      │                 │        └─► subprocess.run(["cargo", "build", ...])
      │                 │
      │                 └─► _add_rust_artifacts()
      │                          │
      │                          └─► build_data["force_include"][src] = dst
      │
      │ packages wheel with artifacts
      └─► Creates .whl with Python + Rust extensions
```

## Platform-Specific Handling

```
┌──────────────┬───────────────────┬─────────────────┬────────────────┐
│   Platform   │  Cargo Output     │  Plugin Action  │  Wheel Output  │
├──────────────┼───────────────────┼─────────────────┼────────────────┤
│   Linux      │  libname.so       │  Strip 'lib'    │  name.so       │
│   macOS      │  libname.dylib    │  Strip 'lib'    │  name.so       │
│              │                   │  Rename .dylib  │                │
│   Windows    │  name.dll         │  Rename to .pyd │  name.pyd      │
└──────────────┴───────────────────┴─────────────────┴────────────────┘
```

## Configuration Flow

```
pyproject.toml
    │
    └─► [tool.hatch.build.hooks.pyo3]
            │
            ├─► cargo-manifest: "Cargo.toml"    (where to find Cargo.toml)
            │
            ├─► profile: "release"              (cargo build profile)
            │        │
            │        └─► Affects: target/{profile}/ directory
            │
            ├─► target-dir: "target"            (cargo output directory)
            │        │
            │        └─► Where to find compiled artifacts
            │
            └─► cargo-args: ["--features", ...] (extra cargo arguments)
                     │
                     └─► Passed to: cargo build {cargo-args}
```

## Data Flow

```
Source Code                Compilation              Distribution
───────────                ───────────              ────────────

src/lib.rs    ──┐
                ├──► cargo build ──► libname.{so,dylib,dll}
Cargo.toml  ──┘                             │
                                            │
                                            ▼
                                    Plugin processes
                                            │
                                            │ strip prefix
                                            │ rename extension
                                            │
                                            ▼
                                    name.{so,pyd}
                                            │
                                            │
                                            ▼
my_package/     ──┐                         │
  __init__.py   ──┼──► Hatchling ───────────┘
  other.py      ──┘      build              │
                                            │
                                            ▼
                                    ┌───────────────┐
                                    │  .whl file    │
                                    ├───────────────┤
                                    │ my_package/   │
                                    │   __init__.py │
                                    │   name.so     │
                                    └───────────────┘
```

## Error Handling

```
Build Process                      Error Handling
─────────────                      ──────────────

Cargo.toml not found      ──►  Silent skip (optional dependency)
                               display_debug("No Cargo.toml found")

Cargo build fails         ──►  Raise exception with details
                               display_error(stdout, stderr)
                               Stops build process

No artifacts found        ──►  Display warning
                               display_warning("No libraries found")
                               Continues build (may fail at import time)

Import fails at runtime   ──►  User code handles
                               try/except ImportError
                               warnings.warn()
```
