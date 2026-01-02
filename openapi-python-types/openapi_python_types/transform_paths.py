"""Transform OpenAPI Paths Object to Request class with @overload methods.

This module handles the conversion of API operations to @overload methods on a 
Request class, with proper TypedDict for path and query parameters.

Reference: https://spec.openapis.org/oas/v3.1.0#paths-object
"""

import ast
import re
from typing import Any

from .ast_utils import (
    any_type,
    make_constant,
    make_name,
    make_overload_method,
    make_typed_dict,
    literal_type,
    not_required_type,
)
from .context import TransformOptions, GeneratorContext
from .transform_schema import transform_schema_object


def transform_paths_object(paths: dict[str, Any], ctx: GeneratorContext) -> list[ast.stmt]:
    """Transform the paths object to Request class with @overload methods.
    
    Args:
        paths: The paths object from OpenAPI spec
        ctx: Generator context
        
    Returns:
        List of TypedDict classes for parameters and Request class with overloads
    """
    nodes: list[ast.stmt] = []
    overload_methods: list[ast.FunctionDef] = []
    
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
            
            # Generate TypedDicts and overload method
            operation_nodes, overload_method = transform_operation_to_overload(
                path, method, operation, options
            )
            
            nodes.extend(operation_nodes)
            if overload_method:
                overload_methods.append(overload_method)
    
    # Create the Request class with all overload methods
    if overload_methods:
        ctx.add_import("overload")
        request_class = create_request_class(overload_methods, ctx)
        nodes.append(request_class)
    
    return nodes


def transform_operation_to_overload(
    path: str,
    method: str,
    operation: dict[str, Any],
    options: TransformOptions,
) -> tuple[list[ast.stmt], ast.FunctionDef | None]:
    """Transform an operation to TypedDicts and an @overload method.
    
    Args:
        path: The path (e.g., "/users/{id}")
        method: The HTTP method
        operation: The operation object
        options: Transform options
        
    Returns:
        Tuple of (list of TypedDict nodes, overload method)
    """
    nodes: list[ast.stmt] = []
    
    # Generate a base name for this operation
    operation_id = operation.get("operationId")
    if operation_id:
        base_name = "".join(word.capitalize() for word in re.split(r"[_\-]", operation_id))
    else:
        # Generate from path and method
        path_parts = [p for p in path.split("/") if p and not p.startswith("{")]
        path_name = "".join(word.capitalize() for word in path_parts)
        base_name = f"{method.capitalize()}{path_name}"
    
    # Collect path parameters
    path_params_dict = _generate_path_params_dict(base_name, path, operation, options)
    path_params_type = None
    if path_params_dict:
        nodes.append(path_params_dict)
        path_params_type = make_name(path_params_dict.name)
    
    # Collect query parameters
    query_params_dict = _generate_query_params_dict(base_name, operation, options)
    query_params_type = None
    if query_params_dict:
        nodes.append(query_params_dict)
        query_params_type = make_name(query_params_dict.name)
    
    # Get body type
    body_type = _get_body_type(operation, options)
    
    # Get response type
    response_type = _get_response_type(operation, options)
    
    # Create the overload method
    overload_method = _create_overload_for_operation(
        method, path, path_params_type, query_params_type, body_type, response_type, options
    )
    
    return nodes, overload_method


def _generate_path_params_dict(
    base_name: str,
    path: str,
    operation: dict[str, Any],
    options: TransformOptions,
) -> ast.ClassDef | None:
    """Generate TypedDict for path parameters."""
    # Extract path parameters from the path string
    path_param_names = set(re.findall(r'\{(\w+)\}', path))
    
    if not path_param_names:
        return None
    
    # Find parameter definitions
    parameters = operation.get("parameters", [])
    path_params = {}
    
    for param in parameters:
        if not isinstance(param, dict):
            continue
        
        # Handle $ref
        if "$ref" in param:
            param = options.ctx.resolve_ref(param["$ref"])
        
        param_name = param.get("name")
        param_in = param.get("in")
        
        if param_in == "path" and param_name in path_param_names:
            param_schema = param.get("schema", {})
            param_type = transform_schema_object(param_schema, options)
            path_params[param_name] = param_type
    
    # If we couldn't find types for all path params, use str as fallback
    for param_name in path_param_names:
        if param_name not in path_params:
            path_params[param_name] = make_name("str")
    
    if not path_params:
        return None
    
    options.ctx.add_import("TypedDict")
    
    fields = [(name, type_ann) for name, type_ann in path_params.items()]
    return make_typed_dict(f"{base_name}PathParams", fields)


def _generate_query_params_dict(
    base_name: str,
    operation: dict[str, Any],
    options: TransformOptions,
) -> ast.ClassDef | None:
    """Generate TypedDict for query parameters."""
    parameters = operation.get("parameters", [])
    query_params = []
    required_params = set()
    
    for param in parameters:
        if not isinstance(param, dict):
            continue
        
        # Handle $ref
        if "$ref" in param:
            param = options.ctx.resolve_ref(param["$ref"])
        
        param_name = param.get("name")
        param_in = param.get("in")
        param_required = param.get("required", False)
        
        if param_in == "query":
            param_schema = param.get("schema", {})
            param_type = transform_schema_object(param_schema, options)
            query_params.append((param_name, param_type))
            
            if param_required:
                required_params.add(param_name)
    
    if not query_params:
        return None
    
    options.ctx.add_import("TypedDict")
    
    # Wrap optional parameters with NotRequired
    fields = []
    for param_name, param_type in query_params:
        if param_name not in required_params:
            options.ctx.add_import("NotRequired")
            param_type = not_required_type(param_type)
        fields.append((param_name, param_type))
    
    return make_typed_dict(f"{base_name}QueryParams", fields)


def _get_body_type(operation: dict[str, Any], options: TransformOptions) -> ast.expr | None:
    """Get the body type for an operation."""
    request_body = operation.get("requestBody")
    if not request_body:
        return None
    
    # Handle $ref
    if "$ref" in request_body:
        request_body = options.ctx.resolve_ref(request_body["$ref"])
    
    content = request_body.get("content", {})
    
    # Look for application/json content type
    if "application/json" in content:
        body_schema = content["application/json"].get("schema", {})
        return transform_schema_object(body_schema, options)
    
    return None


def _get_response_type(operation: dict[str, Any], options: TransformOptions) -> ast.expr:
    """Get the response type for an operation.
    
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
            
            # 204 No Content returns None since there's no response body
            if status_code == "204":
                return make_constant(None)
            
            # Check for content
            content = response.get("content", {})
            
            # Look for application/json
            if "application/json" in content:
                response_schema = content["application/json"].get("schema", {})
                return transform_schema_object(response_schema, options)
            
            # No content type specified - return None
            return make_constant(None)
    
    # No success response found, use Any
    options.ctx.add_import("Any")
    return any_type()


def _create_overload_for_operation(
    method: str,
    path: str,
    path_params_type: ast.expr | None,
    query_params_type: ast.expr | None,
    body_type: ast.expr | None,
    response_type: ast.expr,
    options: TransformOptions,
) -> ast.FunctionDef:
    """Create an @overload method for an operation."""
    options.ctx.add_import("Literal")
    
    # Build parameters list
    params: list[tuple[str, ast.expr]] = []
    
    # Method parameter - Literal["GET"], etc.
    method_literal = literal_type([make_constant(method.upper())])
    params.append(("method", method_literal))
    
    # Path parameter - Literal["/users/{id}"]
    path_literal = literal_type([make_constant(path)])
    params.append(("path", path_literal))
    
    # Path params - either the TypedDict type or None
    if path_params_type:
        params.append(("path_params", path_params_type))
    else:
        params.append(("path_params", make_constant(None)))
    
    # Query params - either the TypedDict type or None
    if query_params_type:
        params.append(("query_params", query_params_type))
    else:
        params.append(("query_params", make_constant(None)))
    
    # Body - either the body type or None
    if body_type:
        params.append(("body", body_type))
    else:
        params.append(("body", make_constant(None)))
    
    # Return the response type (not None anymore!)
    return make_overload_method("__call__", params, response_type)


def create_request_class(overload_methods: list[ast.FunctionDef], ctx: GeneratorContext) -> ast.ClassDef:
    """Create the Request Protocol class with all @overload methods and an implementation."""
    # Ensure imports
    ctx.add_import("Any")
    ctx.add_import("Protocol")
    
    # Add the actual __call__ implementation after all overloads
    impl_method = ast.FunctionDef(
        name="__call__",
        args=ast.arguments(
            posonlyargs=[],
            args=[
                ast.arg(arg="self", annotation=None),
                ast.arg(arg="method", annotation=make_name("str")),
                ast.arg(arg="path", annotation=make_name("str")),
                ast.arg(arg="path_params", annotation=any_type()),
                ast.arg(arg="query_params", annotation=any_type()),
                ast.arg(arg="body", annotation=any_type()),
            ],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
        ),
        body=[ast.Expr(value=ast.Constant(value=...))],  # ... (Ellipsis)
        decorator_list=[],
        returns=any_type(),
    )
    
    # Create as Protocol instead of regular class
    return ast.ClassDef(
        name="Request",
        bases=[make_name("Protocol")],
        keywords=[],
        body=overload_methods + [impl_method],
        decorator_list=[],
    )
