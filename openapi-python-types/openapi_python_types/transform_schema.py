"""Transform OpenAPI Schema Objects to Python type annotations.

This module handles the conversion of OpenAPI Schema Objects (3.0/3.1) to Python
type annotations using the AST. It supports all schema types and compositions.

Reference: https://spec.openapis.org/oas/v3.1.0#schema-object
"""

import ast
from typing import Any

from .ast_utils import (
    any_type,
    bool_type,
    dict_type,
    float_type,
    int_type,
    list_type,
    literal_type,
    make_constant,
    make_name,
    optional_type,
    str_type,
    union_type,
)
from .context import TransformOptions


def transform_schema_object(schema: Any, options: TransformOptions) -> ast.expr:
    """Transform a Schema Object to a Python type annotation.
    
    Args:
        schema: The OpenAPI Schema Object or Reference Object
        options: Transform options with context
        
    Returns:
        An AST expression representing the Python type
    """
    # Handle missing or invalid schemas
    if schema is None or schema is False:
        # false schema accepts nothing (use Never in 3.11+, but we'll use Any for compatibility)
        return any_type()
    
    if schema is True:
        # true schema accepts anything
        return any_type()
    
    if not isinstance(schema, dict):
        return any_type()
    
    # Handle $ref
    if "$ref" in schema:
        ref_name = options.ctx.get_ref_name(schema["$ref"])
        return make_name(ref_name)
    
    # Handle const (any type can have const)
    if "const" in schema:
        return literal_type([make_constant(schema["const"])])
    
    # Handle enum (for non-object types)
    if "enum" in schema and isinstance(schema["enum"], list):
        # Check if this is an object enum (which should be handled differently)
        is_object_enum = (
            schema.get("type") == "object" 
            or "properties" in schema 
            or "additionalProperties" in schema
        )
        
        if not is_object_enum:
            options.ctx.add_import("Literal")
            enum_values = [make_constant(v) for v in schema["enum"]]
            base_type = literal_type(enum_values)
            return _handle_nullable(schema, base_type, options)
    
    # Handle allOf (intersection)
    if "allOf" in schema:
        return _transform_all_of(schema["allOf"], options)
    
    # Handle anyOf (union)
    if "anyOf" in schema:
        return _transform_any_of(schema["anyOf"], options)
    
    # Handle oneOf (union with discriminator support)
    if "oneOf" in schema:
        return _transform_one_of(schema["oneOf"], options)
    
    # Handle not (negation - we'll use Any as we can't express this in Python types)
    if "not" in schema:
        return any_type()
    
    # Get the type
    schema_type = schema.get("type")
    
    # Handle multiple types (OpenAPI 3.1 JSON Schema feature)
    if isinstance(schema_type, list):
        types = []
        for t in schema_type:
            type_schema = {**schema, "type": t}
            types.append(transform_schema_object(type_schema, options))
        
        if len(types) == 1:
            return types[0]
        
        # No import needed for X | Y syntax
        return union_type(types)
    
    # Handle specific types
    if schema_type == "string":
        return _transform_string_type(schema, options)
    elif schema_type == "integer":
        return _transform_integer_type(schema, options)
    elif schema_type == "number":
        return _transform_number_type(schema, options)
    elif schema_type == "boolean":
        return _transform_boolean_type(schema, options)
    elif schema_type == "array":
        return _transform_array_type(schema, options)
    elif schema_type == "object":
        return _transform_object_type(schema, options)
    elif schema_type == "null":
        return make_constant(None)
    elif schema_type is None:
        # No type specified - check for properties or additionalProperties
        if "properties" in schema or "additionalProperties" in schema:
            return _transform_object_type(schema, options)
        # Otherwise return Any
        return any_type()
    else:
        # Unknown type
        return any_type()


def _transform_string_type(schema: dict[str, Any], options: TransformOptions) -> ast.expr:
    """Transform a string type."""
    base_type = str_type()
    return _handle_nullable(schema, base_type, options)


def _transform_integer_type(schema: dict[str, Any], options: TransformOptions) -> ast.expr:
    """Transform an integer type."""
    base_type = int_type()
    return _handle_nullable(schema, base_type, options)


def _transform_number_type(schema: dict[str, Any], options: TransformOptions) -> ast.expr:
    """Transform a number type."""
    base_type = float_type()
    return _handle_nullable(schema, base_type, options)


def _transform_boolean_type(schema: dict[str, Any], options: TransformOptions) -> ast.expr:
    """Transform a boolean type."""
    base_type = bool_type()
    return _handle_nullable(schema, base_type, options)


def _transform_array_type(schema: dict[str, Any], options: TransformOptions) -> ast.expr:
    """Transform an array type."""
    # No import needed for list[X] syntax
    
    items = schema.get("items")
    if items is None:
        # No items specified, use Any
        item_type = any_type()
    else:
        item_type = transform_schema_object(items, options)
    
    base_type = list_type(item_type)
    return _handle_nullable(schema, base_type, options)


def _transform_object_type(schema: dict[str, Any], options: TransformOptions) -> ast.expr:
    """Transform an object type.
    
    For inline objects, we return dict[str, Any].
    Named objects are handled separately as TypedDict definitions.
    """
    properties = schema.get("properties", {})
    additional_properties = schema.get("additionalProperties")
    
    # If this is an empty object with no properties
    if not properties and additional_properties is None:
        if options.ctx.empty_objects_unknown:
            # No import needed for dict[str, Any] syntax
            options.ctx.add_import("Any")
            return dict_type(str_type(), any_type())
        else:
            # Empty object - will be handled as empty TypedDict if named
            # No import needed for dict[str, Any] syntax
            options.ctx.add_import("Any")
            return dict_type(str_type(), any_type())
    
    # For inline objects, use dict[str, Any]
    # (Named objects with properties will be converted to TypedDict at a higher level)
    # No import needed for dict[str, Any] syntax
    options.ctx.add_import("Any")
    base_type = dict_type(str_type(), any_type())
    
    return _handle_nullable(schema, base_type, options)


def _transform_all_of(schemas: list[Any], options: TransformOptions) -> ast.expr:
    """Transform allOf composition (intersection).
    
    In Python, we approximate this with a union since we can't express
    true intersections. For objects, this would ideally create a merged TypedDict.
    """
    if not schemas:
        return any_type()
    
    if len(schemas) == 1:
        return transform_schema_object(schemas[0], options)
    
    # For now, we'll just use the first schema
    # A proper implementation would merge object schemas
    return transform_schema_object(schemas[0], options)


def _transform_any_of(schemas: list[Any], options: TransformOptions) -> ast.expr:
    """Transform anyOf composition (union)."""
    if not schemas:
        return any_type()
    
    if len(schemas) == 1:
        return transform_schema_object(schemas[0], options)
    
    # No import needed for X | Y syntax
    types = [transform_schema_object(s, options) for s in schemas]
    return union_type(types)


def _transform_one_of(schemas: list[Any], options: TransformOptions) -> ast.expr:
    """Transform oneOf composition (union with discriminator).
    
    For now, we treat this the same as anyOf (union).
    A more sophisticated implementation would handle discriminators.
    """
    return _transform_any_of(schemas, options)


def _handle_nullable(schema: dict[str, Any], base_type: ast.expr, options: TransformOptions) -> ast.expr:
    """Handle nullable property for a type.
    
    Args:
        schema: The schema object
        base_type: The base type AST node
        options: Transform options
        
    Returns:
        The type, wrapped with X | None if nullable
    """
    # Check for nullable in OpenAPI 3.0
    is_nullable = schema.get("nullable", False)
    
    # Check for null in type array (OpenAPI 3.1)
    schema_type = schema.get("type")
    if isinstance(schema_type, list) and "null" in schema_type:
        is_nullable = True
    
    if is_nullable:
        # No import needed for X | None syntax
        return optional_type(base_type)
    
    return base_type
