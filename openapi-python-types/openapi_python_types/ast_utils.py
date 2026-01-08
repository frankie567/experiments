"""AST utilities for generating Python code."""

import ast
from typing import Any


def make_name(id: str) -> ast.Name:
    """Create a Name node."""
    return ast.Name(id=id, ctx=ast.Load())


def make_attribute(value: str, attr: str) -> ast.Attribute:
    """Create an Attribute node (e.g., typing.List)."""
    return ast.Attribute(value=make_name(value), attr=attr, ctx=ast.Load())


def make_subscript(value: ast.expr, slice: ast.expr) -> ast.Subscript:
    """Create a Subscript node (e.g., List[str])."""
    return ast.Subscript(value=value, slice=slice, ctx=ast.Load())


def make_constant(value: Any) -> ast.Constant:
    """Create a Constant node."""
    return ast.Constant(value=value)


def make_tuple(elts: list[ast.expr]) -> ast.Tuple:
    """Create a Tuple node."""
    return ast.Tuple(elts=elts, ctx=ast.Load())


# Common type nodes
def str_type() -> ast.Name:
    """Create str type."""
    return make_name("str")


def int_type() -> ast.Name:
    """Create int type."""
    return make_name("int")


def float_type() -> ast.Name:
    """Create float type."""
    return make_name("float")


def bool_type() -> ast.Name:
    """Create bool type."""
    return make_name("bool")


def any_type() -> ast.expr:
    """Create Any type."""
    return make_name("Any")


def list_type(item_type: ast.expr) -> ast.Subscript:
    """Create list[T] type (modern Python 3.9+ syntax)."""
    return make_subscript(make_name("list"), item_type)


def dict_type(key_type: ast.expr, value_type: ast.expr) -> ast.Subscript:
    """Create dict[K, V] type (modern Python 3.9+ syntax)."""
    tuple_node = make_tuple([key_type, value_type])
    return make_subscript(make_name("dict"), tuple_node)


def optional_type(item_type: ast.expr) -> ast.BinOp:
    """Create X | None type (modern Python 3.10+ syntax)."""
    return ast.BinOp(left=item_type, op=ast.BitOr(), right=make_name("None"))


def union_type(types: list[ast.expr]) -> ast.BinOp | ast.expr:
    """Create X | Y | Z type (modern Python 3.10+ syntax)."""
    if len(types) == 0:
        return any_type()
    if len(types) == 1:
        return types[0]

    # Build union using BinOp with BitOr
    result = types[0]
    for t in types[1:]:
        result = ast.BinOp(left=result, op=ast.BitOr(), right=t)
    return result


def literal_type(values: list[ast.expr]) -> ast.Subscript:
    """Create Literal[...] type."""
    # For single values, pass directly; for multiple, use tuple
    if len(values) == 1:
        slice_node = values[0]
    else:
        slice_node = make_tuple(values)
    return make_subscript(make_name("Literal"), slice_node)


def not_required_type(item_type: ast.expr) -> ast.Subscript:
    """Create NotRequired[T] type."""
    return make_subscript(make_name("NotRequired"), item_type)


def make_typed_dict(
    name: str,
    fields: list[tuple[str, ast.expr]],
    docstring: str | None = None,
    total: bool = True,
) -> ast.ClassDef:
    """Create a TypedDict class definition.

    Args:
        name: Name of the TypedDict class
        fields: List of (field_name, type_annotation) tuples
        docstring: Optional docstring
        total: Whether all fields are required by default
    """
    body: list[ast.stmt] = []

    # Add docstring if provided
    if docstring:
        body.append(ast.Expr(value=make_constant(docstring)))

    # Add fields as AnnAssign statements
    for field_name, field_type in fields:
        ann_assign = ast.AnnAssign(
            target=make_name(field_name),
            annotation=field_type,
            simple=1,
        )
        body.append(ann_assign)

    # If no fields and no docstring, add pass
    if not body:
        body.append(ast.Pass())

    # Create the class - use simple Name instead of Attribute to avoid "typing." prefix
    bases: list[ast.expr] = [make_name("TypedDict")]
    return ast.ClassDef(
        name=name,
        bases=bases,
        keywords=[],
        body=body,
        decorator_list=[],
    )


def make_dataclass(
    name: str,
    fields: list[tuple[str, ast.expr, bool]],  # (name, type, has_default)
    docstring: str | None = None,
) -> ast.ClassDef:
    """Create a dataclass definition.

    Args:
        name: Name of the dataclass
        fields: List of (field_name, type_annotation, has_default) tuples
        docstring: Optional docstring
        
    Returns:
        ClassDef with @dataclass decorator
    """
    body: list[ast.stmt] = []

    # Add docstring if provided
    if docstring:
        body.append(ast.Expr(value=make_constant(docstring)))

    # Add fields as AnnAssign statements
    for field_name, field_type, has_default in fields:
        # Create field with default if needed
        if has_default:
            # Use field(default=None) for optional fields
            ann_assign = ast.AnnAssign(
                target=make_name(field_name),
                annotation=field_type,
                value=ast.Call(
                    func=make_name("field"),
                    args=[],
                    keywords=[ast.keyword(arg="default", value=make_name("None"))],
                ),
                simple=1,
            )
        else:
            # Required field without default
            ann_assign = ast.AnnAssign(
                target=make_name(field_name),
                annotation=field_type,
                simple=1,
            )
        body.append(ann_assign)

    # If no fields and no docstring, add pass
    if not body:
        body.append(ast.Pass())

    # Create the class with @dataclass decorator
    return ast.ClassDef(
        name=name,
        bases=[],
        keywords=[],
        body=body,
        decorator_list=[make_name("dataclass")],
    )


def make_protocol(
    name: str,
    method_name: str,
    params: list[tuple[str, ast.expr, Any]],  # (name, type, default)
    return_type: ast.expr,
    docstring: str | None = None,
) -> ast.ClassDef:
    """Create a Protocol class definition.

    Args:
        name: Name of the Protocol class
        method_name: Name of the method (e.g., "__call__")
        params: List of (param_name, type_annotation, default_value) tuples
        return_type: Return type annotation
        docstring: Optional docstring
    """
    body: list[ast.stmt] = []

    # Add docstring if provided
    if docstring:
        body.append(ast.Expr(value=make_constant(docstring)))

    # Create function arguments
    args = []
    defaults: list[ast.expr] = []

    # Add 'self' parameter for __call__
    if method_name == "__call__":
        args.append(ast.arg(arg="self", annotation=None))

    # Add other parameters
    for param_name, param_type, default_value in params:
        args.append(ast.arg(arg=param_name, annotation=param_type))
        if default_value is not None:
            defaults.append(make_constant(default_value))

    # Create the function definition
    func_def = ast.FunctionDef(
        name=method_name,
        args=ast.arguments(
            posonlyargs=[],
            args=args,
            kwonlyargs=[],
            kw_defaults=[],
            defaults=defaults,
        ),
        body=[ast.Expr(value=ast.Constant(value=...))],  # ... (Ellipsis)
        decorator_list=[],
        returns=return_type,
    )
    body.append(func_def)

    # Create the class - use simple Name instead of Attribute
    bases: list[ast.expr] = [make_name("Protocol")]
    return ast.ClassDef(
        name=name,
        bases=bases,
        keywords=[],
        body=body,
        decorator_list=[],
    )


def make_type_alias(name: str, value: ast.expr) -> ast.Assign:
    """Create a type alias assignment."""
    return ast.Assign(
        targets=[make_name(name)],
        value=value,
    )


def make_overload_method(
    method_name: str,
    params: list[tuple[str, ast.expr]],  # (name, type_annotation)
    kwonly_params: list[
        tuple[str, ast.expr, bool]
    ],  # (name, type_annotation, has_default) for keyword-only
    return_type: ast.expr,
    async_def: bool = False,
) -> ast.FunctionDef | ast.AsyncFunctionDef:
    """Create an @overload decorated method.

    Args:
        method_name: Name of the method (e.g., "__init__")
        params: list of (param_name, type_annotation) tuples for positional params
        kwonly_params: list of (param_name, type_annotation, has_default) tuples for keyword-only params
        return_type: Return type annotation
        async_def: Whether to generate an async overload

    Returns:
        FunctionDef or AsyncFunctionDef with @overload decorator
    """
    # Create function arguments
    args = [ast.arg(arg="self", annotation=None)]  # Always include self

    # Add positional parameters
    for param_name, param_type in params:
        args.append(ast.arg(arg=param_name, annotation=param_type))

    # Add keyword-only parameters
    kwonlyargs = []
    kw_defaults: list[ast.expr | None] = []
    for param_name, param_type, has_default in kwonly_params:
        kwonlyargs.append(ast.arg(arg=param_name, annotation=param_type))
        # If has_default is True, use Ellipsis (...) as the default
        # If has_default is False, use None (meaning required)
        kw_defaults.append(ast.Constant(value=...) if has_default else None)

    func_cls = ast.AsyncFunctionDef if async_def else ast.FunctionDef

    # Create the function definition
    func_def = func_cls(
        name=method_name,
        args=ast.arguments(
            posonlyargs=[],
            args=args,
            kwonlyargs=kwonlyargs,
            kw_defaults=kw_defaults,
            defaults=[],
        ),
        body=[ast.Expr(value=ast.Constant(value=...))],  # ... (Ellipsis)
        decorator_list=[
            make_name("overload")
        ],  # Use simple name since 'overload' is imported directly
        returns=return_type,
        type_comment=None,
    )

    return func_def


def make_import_from(module: str, names: list[str]) -> ast.ImportFrom:
    """Create an import from statement."""
    return ast.ImportFrom(
        module=module,
        names=[ast.alias(name=name, asname=None) for name in names],
        level=0,
    )


def unparse_module(nodes: list[ast.stmt]) -> str:
    """Convert AST nodes to Python source code."""
    # Fix missing location information
    for node in nodes:
        ast.fix_missing_locations(node)

    module = ast.Module(body=nodes, type_ignores=[])
    return ast.unparse(module)
