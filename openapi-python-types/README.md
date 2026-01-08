# OpenAPI Python Types

A Python implementation inspired by [openapi-typescript](https://github.com/openapi-ts/openapi-typescript) that converts OpenAPI 3.0/3.1 specifications to Python type definitions.

## Overview

This tool generates Python type definitions from OpenAPI specifications:
- **TypedDict** for schema objects
- **Protocol** for operations (endpoints)

Unlike openapi-typescript which generates TypeScript declaration files, this tool focuses on generating Python types that can be used for static type checking with tools like mypy and pyright.

## Features

- ✅ Parse OpenAPI 3.0 and 3.1 specifications (JSON and YAML)
- ✅ Generate TypedDict classes for all schemas
- ✅ Generate Protocol classes for API operations
- ✅ Support for common OpenAPI features:
  - Object types with properties
  - Array types
  - Enum types
  - Union types (anyOf, oneOf)
  - Nullable types
  - Required vs optional properties
  - References ($ref)
- ✅ CLI interface for easy usage

## Installation

```bash
uv pip install -e .
```

## Usage

### Command Line

```bash
# Generate types from an OpenAPI spec
uv run openapi-python-types spec.yaml > types.py

# Or with a JSON spec
uv run openapi-python-types spec.json > types.py
```

### Programmatic

```python
from openapi_python_types import generate_types

with open("spec.yaml") as f:
    spec_content = f.read()

types_code = generate_types(spec_content)
print(types_code)
```

## Example

Given an OpenAPI spec with a User schema:

```yaml
components:
  schemas:
    User:
      type: object
      required:
        - id
        - username
      properties:
        id:
          type: integer
        username:
          type: string
        email:
          type: string
```

The tool generates:

```python
from typing import TypedDict, NotRequired

class User(TypedDict):
    id: int
    username: str
    email: NotRequired[str]
```

## Implementation Notes

This tool is focused on **type generation only** - it does not include:
- HTTP client implementation
- Request/response handling
- Validation logic
- Authentication

The goal is to provide accurate type definitions that can be used with any HTTP client library.

## Comparison with openapi-typescript

| Feature | openapi-typescript | openapi-python-types |
|---------|-------------------|---------------------|
| Target Language | TypeScript | Python |
| Schema Types | TypeScript interfaces | TypedDict |
| Operation Types | TypeScript types | Protocol |
| Focus | Type declarations | Type annotations |
| Runtime validation | No | No |
