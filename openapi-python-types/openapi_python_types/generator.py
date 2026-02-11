"""Main generator module for converting OpenAPI specs to Python types.

This module provides the main entry point for generating Python type definitions
from OpenAPI specifications. It uses an AST-based approach inspired by openapi-typescript
to generate clean, type-safe Python code.
"""

import ast
import json
from typing import Any

import yaml

from .ast_utils import make_import_from, unparse_module
from .context import GeneratorContext
from .transform_components import transform_components_object
from .transform_paths import transform_paths_object


def generate_types(spec_content: str, format: str = "auto", **options) -> str:
    """Generate Python type definitions from an OpenAPI specification.
    
    Args:
        spec_content: The OpenAPI specification as a string (JSON or YAML)
        format: Format of the spec - "json", "yaml", or "auto" (default)
        **options: Additional options for the generator (passed to GeneratorContext)
        
    Returns:
        Generated Python code with type definitions
    """
    # Parse the spec
    spec = parse_spec(spec_content, format)
    
    # Create generator context
    ctx = GeneratorContext(spec=spec, **options)
    
    # Generate AST nodes
    nodes = generate_ast(spec, ctx)
    
    # Convert AST to Python code
    code = unparse_module(nodes)
    
    return code


def generate_ast(spec: dict[str, Any], ctx: GeneratorContext) -> list[ast.stmt]:
    """Generate AST nodes from an OpenAPI specification.
    
    Args:
        spec: The parsed OpenAPI specification
        ctx: Generator context
        
    Returns:
        List of AST statement nodes
    """
    nodes: list[ast.stmt] = []
    
    # Transform components (schemas, responses, etc.)
    components = spec.get("components", {})
    if components:
        component_nodes = transform_components_object(components, ctx)
        nodes.extend(component_nodes)
    
    # Transform paths (operations)
    paths = spec.get("paths", {})
    if paths:
        path_nodes = transform_paths_object(paths, ctx)
        nodes.extend(path_nodes)
    
    # Add imports at the beginning
    if ctx.imports:
        import_node = make_import_from("typing", sorted(ctx.imports))
        nodes.insert(0, import_node)
    
    # Add __future__ import at the very beginning for forward references
    future_import = make_import_from("__future__", ["annotations"])
    nodes.insert(0, future_import)
    
    return nodes


def parse_spec(content: str, format: str = "auto") -> dict[str, Any]:
    """Parse an OpenAPI specification from JSON or YAML.
    
    Args:
        content: The specification content as a string
        format: Format of the spec - "json", "yaml", or "auto"
        
    Returns:
        Parsed specification as a dictionary
    """
    if format == "auto":
        # Try to detect format
        content_stripped = content.strip()
        if content_stripped.startswith("{"):
            format = "json"
        else:
            format = "yaml"
    
    if format == "json":
        return json.loads(content)
    else:
        return yaml.safe_load(content)

