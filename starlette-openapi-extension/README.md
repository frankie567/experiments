# Starlette OpenAPI Extension

A lightweight extension for [Starlette](https://starlette.dev/) that enables automatic OpenAPI schema generation using [Pydantic](https://pydantic.dev/) models. Similar in spirit to FastAPI but with a more minimal, explicit approach that stays close to the OpenAPI specification.

## Concept

The extension provides three main components:

### APIRequest

A base class for defining request schemas with Pydantic models for different parts of the HTTP request:

```python
from pydantic import BaseModel
from starlette_openapi import APIRequest

class MyQueryParams(BaseModel):
    page: int
    limit: int

class MyBody(BaseModel):
    email: str

class CreateUserRequest(APIRequest):
    query: MyQueryParams
    body: MyBody
```

### APIResponse

A base class for defining response schemas, including status codes, content, and headers:

```python
from pydantic import BaseModel
from typing import Literal
from starlette_openapi import APIResponse

class UserRead(BaseModel):
    id: int
    email: str

class SuccessResponse(APIResponse):
    status: Literal[200] = 200
    content: UserRead

class ForbiddenHeaders(BaseModel):
    x_foo: str

class ForbiddenSchema(BaseModel):
    detail: str

class ForbiddenResponse(APIResponse):
    status: Literal[403] = 403
    content: ForbiddenSchema
    headers: ForbiddenHeaders
```

### APIRoute

A route class that handles path, HTTP methods, endpoints, and OpenAPI metadata. Uses a metaclass to maintain a registry of all routes for schema generation:

```python
from starlette_openapi import APIRoute

class CreateUserRoute(APIRoute):
    path = "/users"
    methods = ["POST"]
    operation_id = "create_user"
    description = "Create a new user"

    async def endpoint(self, request: CreateUserRequest) -> SuccessResponse | ForbiddenResponse:
        # Your logic here
        return SuccessResponse(content=UserRead(id=1, email=request.body.email))
```

### OpenAPI Schema Generation

Generate the complete OpenAPI specification from all registered routes:

```python
from starlette_openapi import generate_openapi_schema

schema = generate_openapi_schema(
    title="My API",
    version="1.0.0",
    description="My awesome API"
)
```

## Key Features

- **Type-safe**: Full type annotations with Pydantic validation
- **Explicit**: Request/response definitions are clear and follow OpenAPI structure
- **Lightweight**: Minimal abstraction over Starlette
- **Automatic schema generation**: OpenAPI spec generated from route definitions
- **Union responses**: Support for multiple response types representing different outcomes

## Design Philosophy

This extension prioritizes:
1. **Staying close to OpenAPI spec**: The API design mirrors OpenAPI structure
2. **Explicitness over magic**: Clear, explicit definitions over implicit behavior
3. **Type safety**: Leveraging Python's type system and Pydantic for validation
4. **Minimal abstraction**: Thin layer over Starlette, not a new framework

## Usage

See `demo.py` for a complete working example.
