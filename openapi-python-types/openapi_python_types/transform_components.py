"""Transform OpenAPI Components Object.

This module handles the conversion of the components section, which includes
schemas, responses, parameters, etc.

Reference: https://spec.openapis.org/oas/v3.1.0#components-object
"""

import ast
from typing import Any

from .ast_utils import (
    literal_type,
    make_constant,
    make_typed_dict,
    make_type_alias,
    not_required_type,
)
from .context import TransformOptions, GeneratorContext
from .transform_schema import transform_schema_object


def transform_components_object(components: dict[str, Any], ctx: GeneratorContext) -> list[ast.stmt]:
    """Transform the components object to Python type definitions.
    
    Args:
        components: The components object from OpenAPI spec
        ctx: Generator context
        
    Returns:
        List of AST statement nodes (class definitions, type aliases, etc.)
    """
    nodes: list[ast.stmt] = []
    
    # Transform schemas
    schemas = components.get("schemas", {})
    for name, schema in schemas.items():
        if ctx.exclude_deprecated and schema.get("deprecated", False):
            continue
        
        options = TransformOptions(
            ctx=ctx,
            path=f"#/components/schemas/{name}",
            schema=schema,
        )
        
        node = transform_schema_to_definition(name, schema, options)
        if node:
            nodes.append(node)
    
    # TODO: Transform other components (responses, parameters, etc.)
    
    return nodes


def transform_schema_to_definition(
    name: str,
    schema: dict[str, Any],
    options: TransformOptions,
) -> ast.stmt | None:
    """Transform a named schema to a type definition.
    
    Args:
        name: Name of the schema
        schema: The schema object
        options: Transform options
        
    Returns:
        AST node for the type definition (TypedDict, type alias, etc.)
    """
    # Handle $ref (shouldn't happen at top level, but just in case)
    if "$ref" in schema:
        ref_type = transform_schema_object(schema, options)
        return make_type_alias(name, ref_type)
    
    # Handle enum types (non-object)
    if "enum" in schema and isinstance(schema["enum"], list):
        is_object_enum = (
            schema.get("type") == "object" 
            or "properties" in schema 
            or "additionalProperties" in schema
        )
        
        if not is_object_enum:
            options.ctx.add_import("Literal")
            enum_values = [make_constant(v) for v in schema["enum"]]
            enum_type = literal_type(enum_values)
            return make_type_alias(name, enum_type)
    
    # Handle object types with properties
    if schema.get("type") == "object" or "properties" in schema:
        return _transform_object_schema_to_typed_dict(name, schema, options)
    
    # Handle anyOf, oneOf, allOf
    if "anyOf" in schema or "oneOf" in schema or "allOf" in schema:
        union_type = transform_schema_object(schema, options)
        return make_type_alias(name, union_type)
    
    # For other schemas, create a type alias
    schema_type = transform_schema_object(schema, options)
    return make_type_alias(name, schema_type)


def _transform_object_schema_to_typed_dict(
    name: str,
    schema: dict[str, Any],
    options: TransformOptions,
) -> ast.ClassDef:
    """Transform an object schema to a TypedDict class.
    
    Args:
        name: Name of the TypedDict
        schema: The schema object
        options: Transform options
        
    Returns:
        TypedDict class definition
    """
    options.ctx.add_import("TypedDict")
    
    properties = schema.get("properties", {})
    required = set(schema.get("required", []))
    
    # Check if we need NotRequired
    has_optional = any(prop_name not in required for prop_name in properties.keys())
    if has_optional:
        options.ctx.add_import("NotRequired")
    
    # Transform each property
    fields: list[tuple[str, ast.expr]] = []
    
    # Sort properties if alphabetize is enabled
    prop_items = sorted(properties.items()) if options.ctx.alphabetize else properties.items()
    
    for prop_name, prop_schema in prop_items:
        # Transform the property schema to a type
        prop_type = transform_schema_object(prop_schema, options)
        
        # Wrap with NotRequired if not in required list
        if prop_name not in required:
            prop_type = not_required_type(prop_type)
        
        fields.append((prop_name, prop_type))
    
    # Get description for docstring
    docstring = schema.get("description")
    
    return make_typed_dict(name, fields, docstring=docstring)
