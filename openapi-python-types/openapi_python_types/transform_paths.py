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
    literal_type,
    make_constant,
    make_dataclass,
    make_name,
    make_overload_method,
    make_subscript,
    make_typed_dict,
    not_required_type,
    union_type,
)
from .context import GeneratorContext, TransformOptions
from .transform_schema import transform_schema_object


def _sanitize_operation_name(operation_id: str) -> str:
    """Sanitize operation ID to create a valid Python class name.
    
    Converts special characters to underscores, splits on word boundaries,
    and capitalizes each word to create a PascalCase name.
    
    Examples:
        users:list -> UsersList
        api.v1.items -> ApiV1Items
        users/list -> UsersList
        users-list -> UsersList
        users_list -> UsersList
    
    Args:
        operation_id: The operationId from OpenAPI spec
        
    Returns:
        PascalCase name suitable for a Python class
    """
    # Replace special characters with word boundaries
    # This handles: : . / - _ and spaces
    sanitized = re.sub(r'[:\./\-_\s]+', '_', operation_id)
    
    # Split on underscores and capitalize each word
    words = [word.capitalize() for word in sanitized.split('_') if word]
    
    return ''.join(words)


def transform_paths_object(
    paths: dict[str, Any], ctx: GeneratorContext
) -> list[ast.stmt]:
    """Transform the paths object to Request class with @overload methods.

    Args:
        paths: The paths object from OpenAPI spec
        ctx: Generator context

    Returns:
        List of TypedDict classes for parameters and Request class with overloads
    """
    nodes: list[ast.stmt] = []
    sync_overload_methods: list[ast.FunctionDef] = []
    async_overload_methods: list[ast.AsyncFunctionDef] = []

    for path, path_item in paths.items():
        if not isinstance(path_item, dict):
            continue

        # Handle each HTTP method
        for method in [
            "get",
            "post",
            "put",
            "patch",
            "delete",
            "head",
            "options",
            "trace",
        ]:
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
            operation_nodes, sync_overload, async_overload = (
                transform_operation_to_overload(path, method, operation, options)
            )

            nodes.extend(operation_nodes)
            if sync_overload:
                # sync_overload is FunctionDef when async_def=False
                assert isinstance(sync_overload, ast.FunctionDef)
                sync_overload_methods.append(sync_overload)
            if async_overload:
                # async_overload is AsyncFunctionDef when async_def=True
                assert isinstance(async_overload, ast.AsyncFunctionDef)
                async_overload_methods.append(async_overload)

    # Create the Request classes with all overload methods
    if sync_overload_methods or async_overload_methods:
        ctx.add_import("overload")
        request_classes = create_request_classes(
            sync_overload_methods, async_overload_methods, ctx
        )
        nodes.extend(request_classes)

    return nodes


def transform_operation_to_overload(
    path: str,
    method: str,
    operation: dict[str, Any],
    options: TransformOptions,
) -> tuple[list[ast.stmt], ast.FunctionDef | ast.AsyncFunctionDef, ast.FunctionDef | ast.AsyncFunctionDef]:
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
        base_name = _sanitize_operation_name(operation_id)
    else:
        # Generate from path and method
        path_parts = [p for p in path.split("/") if p and not p.startswith("{")]
        path_name = "".join(word.capitalize() for word in path_parts)
        base_name = f"{method.capitalize()}{path_name}"

    # Collect path parameters - generate both TypedDict and dataclass
    path_params_nodes, path_params_type = _generate_path_params_types(base_name, path, operation, options)
    nodes.extend(path_params_nodes)

    # Collect query parameters - generate both TypedDict and dataclass
    query_params_nodes, query_params_type, query_params_all_optional = _generate_query_params_types(base_name, operation, options)
    nodes.extend(query_params_nodes)

    # Get body type
    body_type = _get_body_type(operation, options)

    # Get response type
    response_type = _get_response_type(operation, options)

    # Create the overload methods (sync and async)
    sync_overload, async_overload = _create_overload_for_operation(
        method,
        path,
        path_params_type,
        query_params_type,
        query_params_all_optional,
        body_type,
        response_type,
        options,
    )

    return nodes, sync_overload, async_overload


def _generate_path_params_types(
    base_name: str,
    path: str,
    operation: dict[str, Any],
    options: TransformOptions,
) -> tuple[list[ast.stmt], ast.expr | None]:
    """Generate both TypedDict and dataclass for path parameters.
    
    Returns:
        Tuple of (list of class definitions, union type for overload or None)
    """
    # Extract path parameters from the path string
    path_param_names = set(re.findall(r"\{(\w+)\}", path))

    if not path_param_names:
        return [], None

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
        return [], None

    options.ctx.add_import("TypedDict")
    options.ctx.add_dataclass_import("dataclass")

    # Generate TypedDict version (with Dict suffix)
    typed_dict_name = f"{base_name}PathParamsDict"
    fields_typed_dict = [(name, type_ann) for name, type_ann in path_params.items()]
    typed_dict_class = make_typed_dict(typed_dict_name, fields_typed_dict)

    # Generate dataclass version (without suffix)
    dataclass_name = f"{base_name}PathParams"
    # All path params are required, so has_default=False for all
    fields_dataclass = [(name, type_ann, False) for name, type_ann in path_params.items()]
    dataclass_class = make_dataclass(dataclass_name, fields_dataclass)

    # Create union type for overload: TypedDict | dataclass
    union_type_expr = union_type([make_name(typed_dict_name), make_name(dataclass_name)])

    return [typed_dict_class, dataclass_class], union_type_expr


def _generate_query_params_types(
    base_name: str,
    operation: dict[str, Any],
    options: TransformOptions,
) -> tuple[list[ast.stmt], ast.expr | None, bool]:
    """Generate both TypedDict and dataclass for query parameters.
    
    Args:
        base_name: Base name for the classes
        operation: The operation object from OpenAPI spec
        options: Transform options with context
    
    Returns:
        Tuple of (list of class definitions, union type for overload or None, all_optional bool):
        - List of TypedDict and dataclass class definitions
        - Union type expression for overload if params exist, None otherwise
        - True if all query parameters are optional (NotRequired), False if any are required
    """
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
        return [], None, False

    options.ctx.add_import("TypedDict")
    options.ctx.add_dataclass_import("dataclass")
    options.ctx.add_dataclass_import("field")

    # Generate TypedDict version (with Dict suffix)
    typed_dict_name = f"{base_name}QueryParamsDict"
    fields_typed_dict = []
    for param_name, param_type in query_params:
        if param_name not in required_params:
            options.ctx.add_import("NotRequired")
            param_type = not_required_type(param_type)
        fields_typed_dict.append((param_name, param_type))
    typed_dict_class = make_typed_dict(typed_dict_name, fields_typed_dict)

    # Generate dataclass version (without suffix)
    dataclass_name = f"{base_name}QueryParams"
    fields_dataclass = []
    for param_name, param_type_base in query_params:
        if param_name not in required_params:
            # Optional field: add | None and has_default=True
            param_type_dc = union_type([param_type_base, make_constant(None)])
            fields_dataclass.append((param_name, param_type_dc, True))
        else:
            # Required field
            fields_dataclass.append((param_name, param_type_base, False))
    dataclass_class = make_dataclass(dataclass_name, fields_dataclass)

    # Check if all fields are optional (no required params)
    all_optional = len(required_params) == 0

    # Create union type for overload: TypedDict | dataclass
    union_type_expr = union_type([make_name(typed_dict_name), make_name(dataclass_name)])

    return [typed_dict_class, dataclass_class], union_type_expr, all_optional


def _generate_path_params_dict(
    base_name: str,
    path: str,
    operation: dict[str, Any],
    options: TransformOptions,
) -> ast.ClassDef | None:
    """Generate TypedDict for path parameters."""
    # Extract path parameters from the path string
    path_param_names = set(re.findall(r"\{(\w+)\}", path))

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
) -> tuple[ast.ClassDef | None, bool]:
    """Generate TypedDict for query parameters.
    
    Args:
        base_name: Base name for the TypedDict class
        operation: The operation object from OpenAPI spec
        options: Transform options with context
    
    Returns:
        Tuple of (TypedDict class or None, bool):
        - TypedDict class definition if query parameters exist, None otherwise
        - True if all query parameters are optional (NotRequired), False if any are required
    """
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
        return None, False

    options.ctx.add_import("TypedDict")

    # Wrap optional parameters with NotRequired
    fields = []
    for param_name, param_type in query_params:
        if param_name not in required_params:
            options.ctx.add_import("NotRequired")
            param_type = not_required_type(param_type)
        fields.append((param_name, param_type))

    # Check if all fields are optional (no required params)
    all_optional = len(required_params) == 0

    return make_typed_dict(f"{base_name}QueryParams", fields), all_optional


def _get_body_type(
    operation: dict[str, Any], options: TransformOptions
) -> ast.expr | None:
    """Get the body type for an operation.
    
    Returns a union type that accepts both TypedDict and dataclass versions
    of the schema (e.g., UserCreateDict | UserCreate).
    """
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
        
        # Check if this is a reference to a schema
        if "$ref" in body_schema:
            # Get the schema name (dataclass version)
            schema_name = options.ctx.get_ref_name(body_schema["$ref"])
            # Create union: SchemaDict | Schema
            return union_type([make_name(f"{schema_name}Dict"), make_name(schema_name)])
        else:
            # Inline schema - just return the type
            return transform_schema_object(body_schema, options)

    return None


def _get_response_type(
    operation: dict[str, Any], options: TransformOptions
) -> ast.expr:
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
    query_params_all_optional: bool,
    body_type: ast.expr | None,
    response_type: ast.expr,
    options: TransformOptions,
) -> tuple[ast.FunctionDef | ast.AsyncFunctionDef, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Create @overload methods (sync and async) for an operation."""
    options.ctx.add_import("Literal")

    # Build positional parameters list (method and path)
    positional_params: list[tuple[str, ast.expr]] = []

    # Method parameter - Literal["GET"], etc.
    method_literal = literal_type([make_constant(method.upper())])
    positional_params.append(("method", method_literal))

    # Path parameter - Literal["/users/{id}"]
    path_literal = literal_type([make_constant(path)])
    positional_params.append(("path", path_literal))

    # Build keyword-only parameters (path_params, query_params, body, response_model)
    # Only include parameters that are actually needed (not None)
    # For each parameter, include a flag indicating if it has a default value
    kwonly_params: list[tuple[str, ast.expr, bool]] = []

    # Path params - only add if there are path parameters
    if path_params_type:
        kwonly_params.append(("path_params", path_params_type, False))

    # Query params - only add if there are query parameters
    # If all query params are optional (NotRequired), make the parameter itself optional
    if query_params_type:
        kwonly_params.append(("query_params", query_params_type, query_params_all_optional))

    # Body - only add if there's a request body
    if body_type:
        kwonly_params.append(("body", body_type, False))

    # Add response_model parameter (type[ResponseType])
    # This allows the implementation to instantiate the correct dataclass
    if not isinstance(response_type, ast.Constant) or response_type.value is not None:
        # Only add response_model if the response is not None
        response_model_type = make_subscript(make_name("type"), response_type)
        kwonly_params.append(("response_model", response_model_type, False))

    # Return the response type
    sync_method = make_overload_method(
        "__call__", positional_params, kwonly_params, response_type
    )

    async_method = make_overload_method(
        "__call__", positional_params, kwonly_params, response_type, async_def=True
    )

    return sync_method, async_method


def create_request_classes(
    sync_overloads: list[ast.FunctionDef],
    async_overloads: list[ast.AsyncFunctionDef],
    ctx: GeneratorContext,
) -> list[ast.ClassDef]:
    """Create BaseClient and AsyncBaseClient classes with @overload methods."""
    # Ensure imports
    ctx.add_import("Any")

    # Sync BaseClient
    make_request_method = ast.FunctionDef(
        name="make_request",
        args=ast.arguments(
            posonlyargs=[],
            args=[
                ast.arg(arg="self", annotation=None),
                ast.arg(arg="method", annotation=make_name("str")),
                ast.arg(arg="path", annotation=make_name("str")),
            ],
            kwonlyargs=[
                ast.arg(arg="path_params", annotation=union_type([any_type(), make_constant(None)])),
                ast.arg(arg="query_params", annotation=union_type([any_type(), make_constant(None)])),
                ast.arg(arg="body", annotation=union_type([any_type(), make_constant(None)])),
                ast.arg(arg="response_model", annotation=union_type([make_subscript(make_name("type"), any_type()), make_constant(None)])),
            ],
            kw_defaults=[make_constant(None), make_constant(None), make_constant(None), make_constant(None)],
            defaults=[],
        ),
        body=[
            ast.Raise(
                exc=ast.Call(
                    func=make_name("NotImplementedError"), args=[], keywords=[]
                )
            )
        ],
        decorator_list=[],
        returns=any_type(),
    )

    impl_method = ast.FunctionDef(
        name="__call__",
        args=ast.arguments(
            posonlyargs=[],
            args=[
                ast.arg(arg="self", annotation=None),
                ast.arg(arg="method", annotation=make_name("str")),
                ast.arg(arg="path", annotation=make_name("str")),
            ],
            kwonlyargs=[
                ast.arg(arg="path_params", annotation=union_type([any_type(), make_constant(None)])),
                ast.arg(arg="query_params", annotation=union_type([any_type(), make_constant(None)])),
                ast.arg(arg="body", annotation=union_type([any_type(), make_constant(None)])),
                ast.arg(arg="response_model", annotation=union_type([make_subscript(make_name("type"), any_type()), make_constant(None)])),
            ],
            kw_defaults=[make_constant(None), make_constant(None), make_constant(None), make_constant(None)],
            defaults=[],
        ),
        body=[
            ast.Return(
                value=ast.Call(
                    func=ast.Attribute(
                        value=make_name("self"), attr="make_request", ctx=ast.Load()
                    ),
                    args=[make_name("method"), make_name("path")],
                    keywords=[
                        ast.keyword(arg="path_params", value=make_name("path_params")),
                        ast.keyword(
                            arg="query_params", value=make_name("query_params")
                        ),
                        ast.keyword(arg="body", value=make_name("body")),
                        ast.keyword(arg="response_model", value=make_name("response_model")),
                    ],
                )
            )
        ],
        decorator_list=[],
        returns=any_type(),
    )

    body_list: list[ast.stmt] = [*sync_overloads, impl_method, make_request_method]
    base_client = ast.ClassDef(
        name="BaseClient",
        bases=[],
        keywords=[],
        body=body_list,
        decorator_list=[],
    )

    # Async AsyncBaseClient

    async_impl_method = ast.AsyncFunctionDef(
        name="__call__",
        args=ast.arguments(
            posonlyargs=[],
            args=[
                ast.arg(arg="self", annotation=None),
                ast.arg(arg="method", annotation=make_name("str")),
                ast.arg(arg="path", annotation=make_name("str")),
            ],
            kwonlyargs=[
                ast.arg(arg="path_params", annotation=union_type([any_type(), make_constant(None)])),
                ast.arg(arg="query_params", annotation=union_type([any_type(), make_constant(None)])),
                ast.arg(arg="body", annotation=union_type([any_type(), make_constant(None)])),
                ast.arg(arg="response_model", annotation=union_type([make_subscript(make_name("type"), any_type()), make_constant(None)])),
            ],
            kw_defaults=[make_constant(None), make_constant(None), make_constant(None), make_constant(None)],
            defaults=[],
        ),
        body=[
            ast.Return(
                value=ast.Await(
                    value=ast.Call(
                        func=ast.Attribute(
                            value=make_name("self"),
                            attr="make_request",
                            ctx=ast.Load(),
                        ),
                        args=[make_name("method"), make_name("path")],
                        keywords=[
                            ast.keyword(
                                arg="path_params", value=make_name("path_params")
                            ),
                            ast.keyword(
                                arg="query_params", value=make_name("query_params")
                            ),
                            ast.keyword(arg="body", value=make_name("body")),
                            ast.keyword(arg="response_model", value=make_name("response_model")),
                        ],
                    )
                )
            )
        ],
        decorator_list=[],
        returns=any_type(),
        type_comment=None,
    )

    async_make_request_method = ast.AsyncFunctionDef(
        name="make_request",
        args=ast.arguments(
            posonlyargs=[],
            args=[
                ast.arg(arg="self", annotation=None),
                ast.arg(arg="method", annotation=make_name("str")),
                ast.arg(arg="path", annotation=make_name("str")),
            ],
            kwonlyargs=[
                ast.arg(arg="path_params", annotation=union_type([any_type(), make_constant(None)])),
                ast.arg(arg="query_params", annotation=union_type([any_type(), make_constant(None)])),
                ast.arg(arg="body", annotation=union_type([any_type(), make_constant(None)])),
                ast.arg(arg="response_model", annotation=union_type([make_subscript(make_name("type"), any_type()), make_constant(None)])),
            ],
            kw_defaults=[make_constant(None), make_constant(None), make_constant(None), make_constant(None)],
            defaults=[],
        ),
        body=[
            ast.Raise(
                exc=ast.Call(
                    func=make_name("NotImplementedError"), args=[], keywords=[]
                )
            )
        ],
        decorator_list=[],
        returns=any_type(),
        type_comment=None,
    )

    async_body_list: list[ast.stmt] = [*async_overloads, async_impl_method, async_make_request_method]
    async_client = ast.ClassDef(
        name="AsyncBaseClient",
        bases=[],
        keywords=[],
        body=async_body_list,
        decorator_list=[],
    )

    return [base_client, async_client]
