"""
Demo application for Starlette OpenAPI Extension

This demonstrates how to use the extension to create type-safe API routes
with automatic OpenAPI schema generation.
"""

from typing import Literal
from pydantic import BaseModel, EmailStr
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount
from starlette_openapi import (
    APIRequest,
    APIResponse,
    APIRoute,
    generate_openapi_schema,
    get_all_routes,
)


# ============================================================================
# Pydantic Models for Requests and Responses
# ============================================================================

class UserCreate(BaseModel):
    """User creation payload."""
    email: EmailStr
    name: str
    age: int | None = None


class UserRead(BaseModel):
    """User read model."""
    id: int
    email: str
    name: str
    age: int | None = None


class UserListQuery(BaseModel):
    """Query parameters for listing users."""
    page: int = 1
    limit: int = 10


class UserPathParams(BaseModel):
    """Path parameters for user operations."""
    user_id: int


class ErrorDetail(BaseModel):
    """Error response model."""
    detail: str


class ValidationErrorDetail(BaseModel):
    """Validation error details."""
    field: str
    message: str


class ValidationError(BaseModel):
    """Validation error response."""
    detail: str
    errors: list[ValidationErrorDetail]


# ============================================================================
# Request Definitions
# ============================================================================

class CreateUserRequest(APIRequest):
    """Request for creating a user."""
    body: UserCreate


class ListUsersRequest(APIRequest):
    """Request for listing users."""
    query: UserListQuery


class GetUserRequest(APIRequest):
    """Request for getting a specific user."""
    path: UserPathParams


class UpdateUserRequest(APIRequest):
    """Request for updating a user."""
    path: UserPathParams
    body: UserCreate


# ============================================================================
# Response Definitions
# ============================================================================

class UserCreatedResponse(APIResponse):
    """Successful user creation response."""
    status: Literal[201] = 201
    content: UserRead


class UserReadResponse(APIResponse):
    """Successful user read response."""
    status: Literal[200] = 200
    content: UserRead


class UserListResponse(APIResponse):
    """Successful user list response."""
    status: Literal[200] = 200
    content: list[UserRead]


class NotFoundResponse(APIResponse):
    """Resource not found response."""
    status: Literal[404] = 404
    content: ErrorDetail


class BadRequestResponse(APIResponse):
    """Bad request response."""
    status: Literal[400] = 400
    content: ValidationError


class ForbiddenResponse(APIResponse):
    """Forbidden response."""
    status: Literal[403] = 403
    content: ErrorDetail


# ============================================================================
# Route Definitions
# ============================================================================

class CreateUserRoute(APIRoute):
    """Create a new user."""
    
    path = "/users"
    methods = ["POST"]
    operation_id = "create_user"
    summary = "Create a new user"
    description = "Create a new user with the provided information"
    tags = ["users"]
    
    async def endpoint(
        self, request: CreateUserRequest
    ) -> UserCreatedResponse | BadRequestResponse:
        """Handle user creation."""
        # Simulate user creation
        if request.body.age is not None and request.body.age < 0:
            return BadRequestResponse(
                content=ValidationError(
                    detail="Validation failed",
                    errors=[
                        ValidationErrorDetail(
                            field="age",
                            message="Age must be non-negative"
                        )
                    ]
                )
            )
        
        user = UserRead(
            id=1,
            email=request.body.email,
            name=request.body.name,
            age=request.body.age
        )
        
        return UserCreatedResponse(content=user)


class ListUsersRoute(APIRoute):
    """List all users with pagination."""
    
    path = "/users"
    methods = ["GET"]
    operation_id = "list_users"
    summary = "List users"
    description = "Get a paginated list of users"
    tags = ["users"]
    
    async def endpoint(self, request: ListUsersRequest) -> UserListResponse:
        """Handle user listing."""
        # Simulate fetching users
        users = [
            UserRead(id=1, email="alice@example.com", name="Alice", age=30),
            UserRead(id=2, email="bob@example.com", name="Bob", age=25),
        ]
        
        # Apply pagination (simplified)
        page = request.query.page if request.query else 1
        limit = request.query.limit if request.query else 10
        
        return UserListResponse(content=users)


class GetUserRoute(APIRoute):
    """Get a specific user by ID."""
    
    path = "/users/{user_id}"
    methods = ["GET"]
    operation_id = "get_user"
    summary = "Get user by ID"
    description = "Retrieve a specific user by their ID"
    tags = ["users"]
    
    async def endpoint(
        self, request: GetUserRequest
    ) -> UserReadResponse | NotFoundResponse:
        """Handle getting a specific user."""
        user_id = request.path.user_id if request.path else 0
        
        # Simulate user lookup
        if user_id == 1:
            user = UserRead(
                id=1,
                email="alice@example.com",
                name="Alice",
                age=30
            )
            return UserReadResponse(content=user)
        else:
            return NotFoundResponse(
                content=ErrorDetail(detail=f"User {user_id} not found")
            )


class UpdateUserRoute(APIRoute):
    """Update a user."""
    
    path = "/users/{user_id}"
    methods = ["PUT"]
    operation_id = "update_user"
    summary = "Update user"
    description = "Update an existing user's information"
    tags = ["users"]
    
    async def endpoint(
        self, request: UpdateUserRequest
    ) -> UserReadResponse | NotFoundResponse | ForbiddenResponse:
        """Handle user update."""
        user_id = request.path.user_id if request.path else 0
        
        # Simulate permission check
        if user_id == 999:
            return ForbiddenResponse(
                content=ErrorDetail(detail="You don't have permission to update this user")
            )
        
        # Simulate user lookup and update
        if user_id == 1:
            user = UserRead(
                id=user_id,
                email=request.body.email,
                name=request.body.name,
                age=request.body.age
            )
            return UserReadResponse(content=user)
        else:
            return NotFoundResponse(
                content=ErrorDetail(detail=f"User {user_id} not found")
            )


# ============================================================================
# Starlette Application Setup
# ============================================================================

async def openapi_schema(request):
    """Endpoint to serve OpenAPI schema."""
    schema = generate_openapi_schema(
        title="User Management API",
        version="1.0.0",
        description="A demo API for managing users using Starlette OpenAPI Extension",
        servers=[{"url": "http://localhost:8000", "description": "Local server"}]
    )
    return JSONResponse(schema)


async def homepage(request):
    """Homepage with API documentation link."""
    return JSONResponse({
        "message": "Welcome to the User Management API",
        "docs": "/openapi.json"
    })


# Convert all APIRoute subclasses to Starlette routes
api_routes = [route_cls.to_starlette_route() for route_cls in get_all_routes()]

# Create the Starlette app
app = Starlette(
    routes=[
        Route("/", homepage),
        Route("/openapi.json", openapi_schema),
        *api_routes
    ]
)


if __name__ == "__main__":
    import uvicorn
    
    print("Starting demo server...")
    print("OpenAPI schema available at: http://localhost:8000/openapi.json")
    print("\nExample requests:")
    print("  GET  http://localhost:8000/users")
    print("  POST http://localhost:8000/users")
    print("  GET  http://localhost:8000/users/1")
    print("  PUT  http://localhost:8000/users/1")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
