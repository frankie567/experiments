"""
Starlette OpenAPI Extension

A lightweight extension for Starlette that enables automatic OpenAPI schema generation
using Pydantic models.
"""

from typing import Any, Literal, Type, Union, get_args, get_origin
from typing import Callable, ClassVar
from pydantic import BaseModel, ConfigDict
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route


def _unwrap_optional(type_hint: Any) -> Any:
    """Unwrap Optional[T] to get T, handling both Union[T, None] and T | None syntax."""
    import types
    origin = get_origin(type_hint)
    # Handle both Union from typing and types.UnionType from | operator
    if origin is Union or isinstance(type_hint, types.UnionType):
        args = get_args(type_hint)
        # Filter out NoneType
        non_none_args = [arg for arg in args if arg is not type(None)]
        if len(non_none_args) == 1:
            return non_none_args[0]
        return type_hint
    return type_hint


class APIRequest(BaseModel):
    """
    Base class for API request definitions.
    
    Subclasses can define:
    - query: Pydantic model for query parameters
    - path: Pydantic model for path parameters
    - body: Pydantic model for request body
    - headers: Pydantic model for headers
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    @classmethod
    def parse_from_request(cls, request: Request, path_params: dict[str, Any]) -> "APIRequest":
        """Parse and validate an incoming Starlette request."""
        data = {}
        
        # Parse query parameters
        if hasattr(cls, 'model_fields') and 'query' in cls.model_fields:
            query_type = cls.model_fields['query'].annotation
            query_type = _unwrap_optional(query_type)
            if query_type and query_type is not type(None):
                query_data = dict(request.query_params)
                data['query'] = query_type(**query_data)
        
        # Parse path parameters
        if hasattr(cls, 'model_fields') and 'path' in cls.model_fields:
            path_type = cls.model_fields['path'].annotation
            path_type = _unwrap_optional(path_type)
            if path_type and path_type is not type(None):
                data['path'] = path_type(**path_params)
        
        # Parse headers
        if hasattr(cls, 'model_fields') and 'headers' in cls.model_fields:
            headers_type = cls.model_fields['headers'].annotation
            headers_type = _unwrap_optional(headers_type)
            if headers_type and headers_type is not type(None):
                headers_data = dict(request.headers)
                data['headers'] = headers_type(**headers_data)
        
        return cls(**data)
    
    @classmethod
    async def parse_from_request_async(cls, request: Request, path_params: dict[str, Any]) -> "APIRequest":
        """Parse and validate an incoming Starlette request (async version for body parsing)."""
        data = {}
        
        # Parse query parameters
        if hasattr(cls, 'model_fields') and 'query' in cls.model_fields:
            query_type = cls.model_fields['query'].annotation
            query_type = _unwrap_optional(query_type)
            if query_type and query_type is not type(None):
                query_data = dict(request.query_params)
                data['query'] = query_type(**query_data)
        
        # Parse path parameters
        if hasattr(cls, 'model_fields') and 'path' in cls.model_fields:
            path_type = cls.model_fields['path'].annotation
            path_type = _unwrap_optional(path_type)
            if path_type and path_type is not type(None):
                data['path'] = path_type(**path_params)
        
        # Parse body
        if hasattr(cls, 'model_fields') and 'body' in cls.model_fields:
            body_type = cls.model_fields['body'].annotation
            body_type = _unwrap_optional(body_type)
            if body_type and body_type is not type(None):
                # Only parse body if request has content
                content_type = request.headers.get('content-type', '')
                if 'application/json' in content_type or request.method in ['POST', 'PUT', 'PATCH']:
                    try:
                        body_data = await request.json()
                        data['body'] = body_type(**body_data)
                    except:
                        # No body present or invalid JSON - that's ok for optional fields
                        pass
        
        # Parse headers
        if hasattr(cls, 'model_fields') and 'headers' in cls.model_fields:
            headers_type = cls.model_fields['headers'].annotation
            headers_type = _unwrap_optional(headers_type)
            if headers_type and headers_type is not type(None):
                headers_data = dict(request.headers)
                data['headers'] = headers_type(**headers_data)
        
        return cls(**data)


class APIResponse(BaseModel):
    """
    Base class for API response definitions.
    
    Subclasses should define:
    - status: HTTP status code (use Literal types for specific codes)
    - content: Pydantic model for response body
    - headers: Pydantic model or dict for response headers
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def to_starlette_response(self) -> Response:
        """Convert this APIResponse to a Starlette Response."""
        # Extract status from the class definition
        status_code = 200  # Default
        if hasattr(self.__class__, 'model_fields') and 'status' in self.__class__.model_fields:
            field = self.__class__.model_fields['status']
            # Try to extract from Literal type
            origin = get_origin(field.annotation)
            if origin is Literal:
                args = get_args(field.annotation)
                if args:
                    status_code = args[0]
        
        # Extract headers
        response_headers = {}
        if hasattr(self, 'headers') and self.headers is not None:
            if isinstance(self.headers, dict):
                response_headers = self.headers
            elif isinstance(self.headers, BaseModel):
                response_headers = self.headers.model_dump()
        
        # Extract content
        if hasattr(self, 'content') and self.content is not None:
            if isinstance(self.content, BaseModel):
                return JSONResponse(
                    content=self.content.model_dump(),
                    status_code=status_code,
                    headers=response_headers
                )
            elif isinstance(self.content, list):
                # Handle list of models
                content_data = [item.model_dump() if isinstance(item, BaseModel) else item for item in self.content]
                return JSONResponse(
                    content=content_data,
                    status_code=status_code,
                    headers=response_headers
                )
        
        return Response(
            status_code=status_code,
            headers=response_headers
        )


# Registry for all API routes
_route_registry: list[Type["APIRoute"]] = []


class APIRouteMeta(type):
    """Metaclass that registers all APIRoute subclasses."""
    
    def __new__(mcs, name: str, bases: tuple, namespace: dict):
        cls = super().__new__(mcs, name, bases, namespace)
        # Only register actual subclasses, not the base APIRoute class
        if bases and bases[0].__name__ == "APIRoute":
            _route_registry.append(cls)
        return cls


class APIRoute(metaclass=APIRouteMeta):
    """
    Base class for API routes.
    
    Subclasses should define:
    - path: The URL path
    - methods: List of HTTP methods (e.g., ["GET", "POST"])
    - operation_id: OpenAPI operation ID
    - summary: Short summary
    - description: Detailed description
    - tags: List of tags for grouping
    - endpoint: Async method that handles the request
    """
    
    path: ClassVar[str]
    methods: ClassVar[list[str]] = ["GET"]
    operation_id: ClassVar[str] = ""
    summary: ClassVar[str] = ""
    description: ClassVar[str] = ""
    tags: ClassVar[list[str]] = []
    
    # Type hints for request and response (extracted from endpoint signature)
    request_type: ClassVar[Type[APIRequest] | None] = None
    response_type: ClassVar[Type[APIResponse] | list[Type[APIResponse]] | None] = None
    
    async def endpoint(self, request: APIRequest) -> APIResponse:
        """Override this method to implement your route logic."""
        raise NotImplementedError("Subclasses must implement endpoint()")
    
    @classmethod
    def _extract_types(cls) -> None:
        """Extract request and response types from endpoint signature."""
        import inspect
        import types
        
        if hasattr(cls, 'endpoint'):
            sig = inspect.signature(cls.endpoint)
            
            # Extract request type
            params = list(sig.parameters.values())
            if len(params) > 1:  # Skip 'self'
                request_param = params[1]
                if request_param.annotation != inspect.Parameter.empty:
                    cls.request_type = request_param.annotation
            
            # Extract response type(s)
            if sig.return_annotation != inspect.Signature.empty:
                return_type = sig.return_annotation
                # Check if it's a Union type (handle both Union and | syntax)
                origin = get_origin(return_type)
                if origin is Union or isinstance(return_type, types.UnionType):
                    # Multiple possible responses
                    cls.response_type = list(get_args(return_type))
                else:
                    # Single response type
                    cls.response_type = return_type
    
    @classmethod
    async def _handle_request(cls, request: Request) -> Response:
        """Internal handler that wraps the endpoint."""
        # Extract types if not already done
        if cls.request_type is None:
            cls._extract_types()
        
        # Parse request
        path_params = request.path_params
        if cls.request_type:
            api_request = await cls.request_type.parse_from_request_async(request, path_params)
        else:
            api_request = APIRequest()
        
        # Call endpoint
        instance = cls()
        api_response = await instance.endpoint(api_request)
        
        # Convert to Starlette response
        return api_response.to_starlette_response()
    
    @classmethod
    def to_starlette_route(cls) -> Route:
        """Convert this APIRoute to a Starlette Route."""
        return Route(
            cls.path,
            endpoint=cls._handle_request,
            methods=cls.methods
        )


def get_all_routes() -> list[Type[APIRoute]]:
    """Get all registered APIRoute subclasses."""
    return _route_registry.copy()


def generate_openapi_schema(
    title: str,
    version: str,
    description: str = "",
    servers: list[dict[str, str]] | None = None
) -> dict[str, Any]:
    """
    Generate OpenAPI 3.0 schema from all registered APIRoute subclasses.
    
    Args:
        title: API title
        version: API version
        description: API description
        servers: List of server objects (optional)
    
    Returns:
        OpenAPI schema as a dictionary
    """
    schema: dict[str, Any] = {
        "openapi": "3.0.0",
        "info": {
            "title": title,
            "version": version,
            "description": description
        },
        "paths": {}
    }
    
    if servers:
        schema["servers"] = servers
    
    # Component schemas
    components: dict[str, Any] = {
        "schemas": {}
    }
    
    # Process all registered routes
    for route_cls in _route_registry:
        # Extract types from endpoint signature
        route_cls._extract_types()
        
        path = route_cls.path
        if path not in schema["paths"]:
            schema["paths"][path] = {}
        
        for method in route_cls.methods:
            operation: dict[str, Any] = {}
            
            if route_cls.operation_id:
                operation["operationId"] = route_cls.operation_id
            
            if route_cls.summary:
                operation["summary"] = route_cls.summary
            
            if route_cls.description:
                operation["description"] = route_cls.description
            
            if route_cls.tags:
                operation["tags"] = route_cls.tags
            
            # Parameters (query, path, header)
            parameters = []
            if route_cls.request_type:
                request_type = route_cls.request_type
                
                # Query parameters
                if hasattr(request_type, 'model_fields') and 'query' in request_type.model_fields:
                    query_field = request_type.model_fields['query']
                    query_type = _unwrap_optional(query_field.annotation)
                    if query_type and query_type is not type(None):
                        # Add to components
                        schema_name = query_type.__name__
                        if schema_name not in components["schemas"]:
                            components["schemas"][schema_name] = query_type.model_json_schema()
                        
                        # Add parameters
                        for field_name, field_info in query_type.model_fields.items():
                            param = {
                                "name": field_name,
                                "in": "query",
                                "required": field_info.is_required(),
                                "schema": {"type": _get_json_type(field_info.annotation)}
                            }
                            parameters.append(param)
                
                # Path parameters
                if hasattr(request_type, 'model_fields') and 'path' in request_type.model_fields:
                    path_field = request_type.model_fields['path']
                    path_type = _unwrap_optional(path_field.annotation)
                    if path_type and path_type is not type(None):
                        # Add to components
                        schema_name = path_type.__name__
                        if schema_name not in components["schemas"]:
                            components["schemas"][schema_name] = path_type.model_json_schema()
                        
                        # Add parameters
                        for field_name, field_info in path_type.model_fields.items():
                            param = {
                                "name": field_name,
                                "in": "path",
                                "required": True,  # Path params are always required
                                "schema": {"type": _get_json_type(field_info.annotation)}
                            }
                            parameters.append(param)
                
                # Request body
                if hasattr(request_type, 'model_fields') and 'body' in request_type.model_fields:
                    body_field = request_type.model_fields['body']
                    body_type = _unwrap_optional(body_field.annotation)
                    if body_type and body_type is not type(None):
                        # Add to components
                        schema_name = body_type.__name__
                        if schema_name not in components["schemas"]:
                            components["schemas"][schema_name] = body_type.model_json_schema()
                        
                        operation["requestBody"] = {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": f"#/components/schemas/{schema_name}"
                                    }
                                }
                            }
                        }
            
            if parameters:
                operation["parameters"] = parameters
            
            # Responses
            responses = {}
            if route_cls.response_type:
                response_types = route_cls.response_type if isinstance(route_cls.response_type, list) else [route_cls.response_type]
                
                for response_type in response_types:
                    # Get status code from Literal type in field definition
                    status_code = "200"  # Default
                    if hasattr(response_type, 'model_fields') and 'status' in response_type.model_fields:
                        field = response_type.model_fields['status']
                        # Try to extract from Literal type
                        origin = get_origin(field.annotation)
                        if origin is Literal:
                            args = get_args(field.annotation)
                            if args:
                                status_code = str(args[0])
                    
                    response_def: dict[str, Any] = {
                        "description": f"Response with status {status_code}"
                    }
                    
                    # Response content
                    if hasattr(response_type, 'model_fields') and 'content' in response_type.model_fields:
                        content_field = response_type.model_fields['content']
                        content_type = _unwrap_optional(content_field.annotation)
                        
                        # Handle list types
                        content_origin = get_origin(content_type)
                        if content_origin is list:
                            list_item_type = get_args(content_type)[0]
                            if hasattr(list_item_type, '__name__'):
                                schema_name = list_item_type.__name__
                                if schema_name not in components["schemas"]:
                                    components["schemas"][schema_name] = list_item_type.model_json_schema()
                                
                                response_def["content"] = {
                                    "application/json": {
                                        "schema": {
                                            "type": "array",
                                            "items": {
                                                "$ref": f"#/components/schemas/{schema_name}"
                                            }
                                        }
                                    }
                                }
                        elif content_type and content_type is not type(None) and hasattr(content_type, '__name__'):
                            # Add to components
                            schema_name = content_type.__name__
                            if schema_name not in components["schemas"]:
                                components["schemas"][schema_name] = content_type.model_json_schema()
                            
                            response_def["content"] = {
                                "application/json": {
                                    "schema": {
                                        "$ref": f"#/components/schemas/{schema_name}"
                                    }
                                }
                            }
                    
                    responses[status_code] = response_def
            
            if not responses:
                responses["200"] = {"description": "Successful response"}
            
            operation["responses"] = responses
            
            schema["paths"][path][method.lower()] = operation
    
    # Add components if there are any
    if components["schemas"]:
        schema["components"] = components
    
    return schema


def _get_json_type(python_type: Any) -> str:
    """Convert Python type to JSON schema type."""
    type_map = {
        int: "integer",
        str: "string",
        bool: "boolean",
        float: "number",
    }
    return type_map.get(python_type, "string")


__all__ = [
    "APIRequest",
    "APIResponse",
    "APIRoute",
    "get_all_routes",
    "generate_openapi_schema",
]
