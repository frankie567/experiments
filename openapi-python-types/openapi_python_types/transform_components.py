"""Transform OpenAPI Components Object.

This module handles the conversion of the components section, which includes
schemas, responses, parameters, etc.

Reference: https://spec.openapis.org/oas/v3.1.0#components-object
"""

import ast
import re
from typing import Any

from .ast_utils import (
    literal_type,
    make_constant,
    make_dataclass,
    make_typed_dict,
    make_type_alias,
    not_required_type,
    optional_type,
)
from .context import TransformOptions, GeneratorContext
from .transform_schema import transform_schema_object


def _sanitize_schema_name(name: str) -> str:
    """Sanitize schema name to create a valid Python identifier.
    
    Replaces hyphens and other invalid characters with underscores.
    
    Examples:
        CostMetadata-Input -> CostMetadataInput
        ProductPriceSeatTiers-Output -> ProductPriceSeatTiersOutput
        some-kebab-case -> SomeKebabCase
    
    Args:
        name: The schema name from OpenAPI spec
        
    Returns:
        Sanitized name suitable for a Python class/type
    """
    # Replace hyphens with underscores, then remove them for PascalCase
    # This handles: - and converts to PascalCase
    if '-' in name:
        parts = name.split('-')
        return ''.join(parts)
    
    return name


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
        
        schema_nodes = transform_schema_to_definition(name, schema, options)
        if schema_nodes:
            nodes.extend(schema_nodes)
    
    # TODO: Transform other components (responses, parameters, etc.)
    
    return nodes


def transform_schema_to_definition(
    name: str,
    schema: dict[str, Any],
    options: TransformOptions,
) -> list[ast.stmt]:
    """Transform a named schema to type definitions (TypedDict and dataclass).
    
    Args:
        name: Name of the schema
        schema: The schema object
        options: Transform options
        
    Returns:
        List of AST nodes for the type definitions
    """
    # Sanitize schema name to ensure valid Python identifier
    sanitized_name = _sanitize_schema_name(name)
    
    # Handle $ref (shouldn't happen at top level, but just in case)
    if "$ref" in schema:
        ref_type = transform_schema_object(schema, options)
        return [make_type_alias(sanitized_name, ref_type)]
    
    # Handle enum types (non-object)
    if "enum" in schema and isinstance(schema["enum"], list):
        is_object_enum = (
            schema.get("type") == "object" 
            or "properties" in schema 
            or "additionalProperties" in schema
        )
        
        if not is_object_enum:
            options.ctx.add_import("Literal")
            enum_values: list[ast.expr] = [make_constant(v) for v in schema["enum"]]
            enum_type = literal_type(enum_values)
            return [make_type_alias(sanitized_name, enum_type)]
    
    # Handle object types with properties - generate both TypedDict and dataclass
    if schema.get("type") == "object" or "properties" in schema:
        return _transform_object_schema_to_both(sanitized_name, schema, options)
    
    # Handle anyOf, oneOf, allOf
    if "anyOf" in schema or "oneOf" in schema or "allOf" in schema:
        union_type = transform_schema_object(schema, options)
        return [make_type_alias(sanitized_name, union_type)]
    
    # For other schemas, create a type alias
    schema_type = transform_schema_object(schema, options)
    return [make_type_alias(sanitized_name, schema_type)]


def _transform_object_schema_to_both(
    name: str,
    schema: dict[str, Any],
    options: TransformOptions,
) -> list[ast.stmt]:
    """Transform an object schema to both TypedDict and dataclass.
    
    Args:
        name: Base name for the types
        schema: The schema object
        options: Transform options
        
    Returns:
        List containing both TypedDict (with Dict suffix) and dataclass definitions
    """
    options.ctx.add_import("TypedDict")
    options.ctx.add_dataclass_import("dataclass")
    options.ctx.add_dataclass_import("field")
    
    properties = schema.get("properties", {})
    required = set(schema.get("required", []))
    
    # Check if we need NotRequired
    has_optional = any(prop_name not in required for prop_name in properties.keys())
    if has_optional:
        options.ctx.add_import("NotRequired")
    
    # Sort properties if alphabetize is enabled
    prop_items = sorted(properties.items()) if options.ctx.alphabetize else properties.items()
    
    # For TypedDict - fields with NotRequired wrapper
    typed_dict_fields: list[tuple[str, ast.expr]] = []
    # For dataclass - fields with has_default flag
    dataclass_fields: list[tuple[str, ast.expr, bool]] = []
    
    for prop_name, prop_schema in prop_items:
        # Transform the property schema to a type
        prop_type = transform_schema_object(prop_schema, options)
        
        is_required = prop_name in required
        
        # For TypedDict: wrap with NotRequired if not required
        if is_required:
            typed_dict_fields.append((prop_name, prop_type))
        else:
            typed_dict_fields.append((prop_name, not_required_type(prop_type)))
        
        # For dataclass: mark if optional, and make type nullable
        if is_required:
            dataclass_fields.append((prop_name, prop_type, False))
        else:
            # Optional fields should have X | None type and default
            nullable_type = optional_type(prop_type)
            dataclass_fields.append((prop_name, nullable_type, True))
    
    # Get description for docstring
    docstring = schema.get("description")
    
    # Generate TypedDict with Dict suffix
    typed_dict = make_typed_dict(f"{name}Dict", typed_dict_fields, docstring=docstring)
    
    # Generate dataclass with original name
    dataclass_def = make_dataclass(name, dataclass_fields, docstring=docstring)
    
    return [typed_dict, dataclass_def]


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
