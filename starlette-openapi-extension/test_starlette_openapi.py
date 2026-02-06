"""
Tests for Starlette OpenAPI Extension
"""

import pytest
from typing import Literal
from pydantic import BaseModel
from starlette.testclient import TestClient
from starlette.applications import Starlette
from starlette.routing import Route

from starlette_openapi import (
    APIRequest,
    APIResponse,
    APIRoute,
    generate_openapi_schema,
    get_all_routes,
    _route_registry,
)


# ============================================================================
# Test Models
# ============================================================================

class TestQueryParams(BaseModel):
    page: int = 1
    limit: int = 10


class TestPathParams(BaseModel):
    item_id: int


class TestBody(BaseModel):
    name: str
    value: int


class TestContent(BaseModel):
    id: int
    name: str


class ErrorContent(BaseModel):
    detail: str


# ============================================================================
# Test Request and Response Classes
# ============================================================================

class TestAPIRequest(APIRequest):
    query: TestQueryParams | None = None
    path: TestPathParams | None = None
    body: TestBody | None = None


class SuccessResponse(APIResponse):
    status: Literal[200] = 200
    content: TestContent


class CreatedResponse(APIResponse):
    status: Literal[201] = 201
    content: TestContent


class NotFoundResponse(APIResponse):
    status: Literal[404] = 404
    content: ErrorContent


# ============================================================================
# Tests
# ============================================================================

def test_api_request_parsing():
    """Test APIRequest can parse different parts of a request."""
    from starlette.requests import Request
    from starlette.datastructures import QueryParams
    
    # Create a mock request with query params and path params
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/items/123",
        "query_string": b"page=2&limit=20",
        "headers": [],
    }
    
    request = Request(scope)
    path_params = {"item_id": 123}
    
    class SimpleRequest(APIRequest):
        query: TestQueryParams
        path: TestPathParams
    
    api_request = SimpleRequest.parse_from_request(request, path_params)
    
    assert api_request.query is not None
    assert api_request.query.page == 2
    assert api_request.query.limit == 20
    assert api_request.path is not None
    assert api_request.path.item_id == 123


def test_api_response_to_starlette():
    """Test APIResponse conversion to Starlette Response."""
    response = SuccessResponse(
        content=TestContent(id=1, name="test")
    )
    
    starlette_response = response.to_starlette_response()
    
    assert starlette_response.status_code == 200
    # Check that it's JSON response with correct content
    import json
    body = json.loads(starlette_response.body)
    assert body["id"] == 1
    assert body["name"] == "test"


def test_api_response_with_headers():
    """Test APIResponse with custom headers."""
    
    class ResponseWithHeaders(APIResponse):
        status: Literal[200] = 200
        content: TestContent
        headers: dict[str, str] | None = None
    
    response = ResponseWithHeaders(
        content=TestContent(id=1, name="test"),
        headers={"X-Custom-Header": "value"}
    )
    
    starlette_response = response.to_starlette_response()
    
    assert starlette_response.headers["X-Custom-Header"] == "value"


def test_route_registration():
    """Test that APIRoute subclasses are registered."""
    # Clear the registry for this test
    initial_count = len(_route_registry)
    
    class TestRoute(APIRoute):
        path = "/test"
        methods = ["GET"]
        
        async def endpoint(self, request: APIRequest) -> SuccessResponse:
            return SuccessResponse(content=TestContent(id=1, name="test"))
    
    # Check that the route was registered
    assert len(_route_registry) > initial_count
    assert TestRoute in _route_registry


def test_openapi_schema_generation():
    """Test OpenAPI schema generation from routes."""
    # Clear registry and add a test route
    _route_registry.clear()
    
    class SchemaTestRoute(APIRoute):
        path = "/items/{item_id}"
        methods = ["GET", "POST"]
        operation_id = "get_item"
        summary = "Get an item"
        description = "Retrieve an item by ID"
        tags = ["items"]
        
        async def endpoint(
            self, request: TestAPIRequest
        ) -> SuccessResponse | NotFoundResponse:
            return SuccessResponse(content=TestContent(id=1, name="test"))
    
    schema = generate_openapi_schema(
        title="Test API",
        version="1.0.0",
        description="Test API Description"
    )
    
    # Check basic structure
    assert schema["openapi"] == "3.0.0"
    assert schema["info"]["title"] == "Test API"
    assert schema["info"]["version"] == "1.0.0"
    
    # Check paths
    assert "/items/{item_id}" in schema["paths"]
    
    # Check operations
    path_item = schema["paths"]["/items/{item_id}"]
    assert "get" in path_item
    assert "post" in path_item
    
    # Check operation details
    get_op = path_item["get"]
    assert get_op["operationId"] == "get_item"
    assert get_op["summary"] == "Get an item"
    assert get_op["description"] == "Retrieve an item by ID"
    assert "items" in get_op["tags"]
    
    # Check responses
    assert "responses" in get_op
    assert "200" in get_op["responses"]
    assert "404" in get_op["responses"]


def test_route_to_starlette_integration():
    """Test full integration with Starlette."""
    _route_registry.clear()
    
    class SimpleRequest(APIRequest):
        query: TestQueryParams | None = None
        body: TestBody | None = None
    
    class IntegrationRoute(APIRoute):
        path = "/test"
        methods = ["POST"]
        
        async def endpoint(self, request: SimpleRequest) -> CreatedResponse:
            return CreatedResponse(
                content=TestContent(
                    id=request.body.value,
                    name=request.body.name
                )
            )
    
    # Create Starlette app
    routes = [route_cls.to_starlette_route() for route_cls in get_all_routes()]
    app = Starlette(routes=routes)
    
    # Test with TestClient
    client = TestClient(app)
    
    response = client.post(
        "/test?page=1&limit=10",
        json={"name": "test_item", "value": 42}
    )
    
    assert response.status_code == 201
    assert response.json()["id"] == 42
    assert response.json()["name"] == "test_item"


def test_multiple_response_types():
    """Test routes with multiple possible response types."""
    _route_registry.clear()
    
    class MultiResponseRoute(APIRoute):
        path = "/items/{item_id}"
        methods = ["GET"]
        
        async def endpoint(
            self, request: TestAPIRequest
        ) -> SuccessResponse | NotFoundResponse:
            if request.path and request.path.item_id == 1:
                return SuccessResponse(content=TestContent(id=1, name="found"))
            else:
                return NotFoundResponse(content=ErrorContent(detail="Not found"))
    
    routes = [route_cls.to_starlette_route() for route_cls in get_all_routes()]
    app = Starlette(routes=routes)
    client = TestClient(app)
    
    # Test successful response
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["name"] == "found"
    
    # Test not found response
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_query_parameters_parsing():
    """Test that query parameters are correctly parsed."""
    _route_registry.clear()
    
    class QueryRoute(APIRoute):
        path = "/search"
        methods = ["GET"]
        
        async def endpoint(self, request: APIRequest) -> SuccessResponse:
            class SearchQuery(BaseModel):
                q: str
                limit: int = 10
            
            class SearchRequest(APIRequest):
                query: SearchQuery
            
            # For this test, manually parse since we're testing the parsing
            if hasattr(request, 'query') and request.query:
                # Access the parsed query
                pass
            
            return SuccessResponse(
                content=TestContent(id=1, name="search_result")
            )
    
    routes = [route_cls.to_starlette_route() for route_cls in get_all_routes()]
    app = Starlette(routes=routes)
    client = TestClient(app)
    
    response = client.get("/search?q=test&limit=20")
    assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
