"""Transform OpenAPI Paths Object to Protocol definitions.

This module handles the conversion of API operations to Python Protocol classes.

Reference: https://spec.openapis.org/oas/v3.1.0#paths-object
"""

import ast
import re
from typing import Any

from .ast_utils import (
    any_type,
    make_constant,
    make_protocol,
    optional_type,
)
from .context import TransformOptions, GeneratorContext
from .transform_schema import transform_schema_object


def transform_paths_object(paths: dict[str, Any], ctx: GeneratorContext) -> list[ast.stmt]:
    """Transform the paths object to Protocol definitions.
    
    Args:
        paths: The paths object from OpenAPI spec
        ctx: Generator context
        
    Returns:
        List of Protocol class definitions
    """
    nodes: list[ast.stmt] = []
    
    for path, path_item in paths.items():
        if not isinstance(path_item, dict):
            continue
        
        # Handle each HTTP method
        for method in ["get", "post", "put", "patch", "delete", "head", "options", "trace"]:
            if method not in path_item:
                continue
            
            operation = path_item[method]
            if not isinstance(operation, dict):
                continue
            
            if ctx.exclude_deprecated and operation.get("deprecated", False):
                continue
            
            options = TransformOptions(
                ctx=ctx,
                path=f"#/paths/{path}/{method}",
                schema=operation,
            )
            
            node = transform_operation_to_protocol(path, method, operation, options)
            if node:
                nodes.append(node)
    
    return nodes


def transform_operation_to_protocol(
    path: str,
    method: str,
    operation: dict[str, Any],
    options: TransformOptions,
) -> ast.ClassDef | None:
    """Transform an operation to a Protocol class.
    
    Args:
        path: The path (e.g., "/users/{id}")
        method: The HTTP method
        operation: The operation object
        options: Transform options
        
    Returns:
        Protocol class definition
    """
    options.ctx.add_import("Protocol")
    
    # Generate protocol name
    protocol_name = _generate_protocol_name(path, method, operation)
    
    # Generate docstring
    docstring = _generate_protocol_docstring(path, method, operation)
    
    # Generate parameters
    params = _generate_protocol_params(operation, options)
    
    # Generate return type
    return_type = _generate_return_type(operation, options)
    
    return make_protocol(
        name=protocol_name,
        method_name="__call__",
        params=params,
        return_type=return_type,
        docstring=docstring,
    )


def _generate_protocol_name(path: str, method: str, operation: dict[str, Any]) -> str:
    """Generate a name for the Protocol class.
    
    Priority:
    1. Use operationId if present
    2. Generate from path and method
    """
    if "operationId" in operation:
        # Convert operationId to PascalCase
        operation_id = operation["operationId"]
        # Convert snake_case or camelCase to PascalCase
        name = "".join(word.capitalize() for word in re.split(r"[_\-]", operation_id))
        return f"{name}Protocol"
    
    # Generate from path and method
    # Remove leading/trailing slashes and path parameters
    path_parts = [p for p in path.split("/") if p and not p.startswith("{")]
    path_name = "".join(word.capitalize() for word in path_parts)
    method_name = method.capitalize()
    
    return f"{method_name}{path_name}Protocol"


def _generate_protocol_docstring(path: str, method: str, operation: dict[str, Any]) -> str:
    """Generate docstring for the Protocol."""
    parts = []
    
    # Add summary or description
    if "summary" in operation:
        parts.append(operation["summary"])
    elif "description" in operation:
        parts.append(operation["description"])
    
    # Add HTTP method and path
    parts.append(f"{method.upper()} {path}")
    
    return "\n\n".join(parts)


def _generate_protocol_params(
    operation: dict[str, Any],
    options: TransformOptions,
) -> list[tuple[str, ast.expr, Any]]:
    """Generate parameters for the Protocol's __call__ method.
    
    Returns:
        List of (param_name, type_annotation, default_value) tuples
    """
    params: list[tuple[str, ast.expr, Any]] = []
    
    # Handle parameters (path, query, header, cookie)
    parameters = operation.get("parameters", [])
    for param in parameters:
        if not isinstance(param, dict):
            continue
        
        # Handle $ref
        if "$ref" in param:
            param = options.ctx.resolve_ref(param["$ref"])
        
        param_name = param.get("name")
        param_in = param.get("in")
        param_required = param.get("required", False)
        param_schema = param.get("schema", {})
        
        if not param_name:
            continue
        
        # Generate type annotation
        param_type = transform_schema_object(param_schema, options)
        
        # Make optional if not required
        if not param_required and param_in != "path":  # path params are always required
            options.ctx.add_import("Optional")
            param_type = optional_type(param_type)
            default_value = None
        else:
            default_value = None  # No default for required params
        
        params.append((param_name, param_type, default_value))
    
    # Handle request body
    request_body = operation.get("requestBody")
    if request_body:
        # Handle $ref
        if "$ref" in request_body:
            request_body = options.ctx.resolve_ref(request_body["$ref"])
        
        content = request_body.get("content", {})
        body_required = request_body.get("required", False)
        
        # Look for application/json content type
        if "application/json" in content:
            body_schema = content["application/json"].get("schema", {})
            body_type = transform_schema_object(body_schema, options)
            
            if not body_required:
                options.ctx.add_import("Optional")
                body_type = optional_type(body_type)
                default_value = None
            else:
                default_value = None
            
            params.append(("body", body_type, default_value))
    
    return params


def _generate_return_type(operation: dict[str, Any], options: TransformOptions) -> ast.expr:
    """Generate return type annotation for the operation.
    
    Looks at the success response (200, 201, 204, etc.) and generates
    the appropriate type.
    """
    responses = operation.get("responses", {})
    
    # Try common success status codes in order of preference
    for status_code in ["200", "201", "202", "204"]:
        if status_code in responses:
            response = responses[status_code]
            
            # Handle $ref
            if "$ref" in response:
                response = options.ctx.resolve_ref(response["$ref"])
            
            # 204 No Content has no body
            if status_code == "204":
                return make_constant(None)
            
            # Check for content
            content = response.get("content", {})
            
            # Look for application/json
            if "application/json" in content:
                response_schema = content["application/json"].get("schema", {})
                return transform_schema_object(response_schema, options)
            
            # No content type specified
            return any_type()
    
    # No success response found, use Any
    options.ctx.add_import("Any")
    return any_type()
