"""Tests for openapi-python-types generator."""

import pytest

from openapi_python_types import generate_types


def test_simple_schema():
    """Test generating TypedDict for a simple schema."""
    spec = """
openapi: 3.0.0
info:
  title: Test API
  version: 1.0.0
components:
  schemas:
    Person:
      type: object
      required:
        - name
      properties:
        name:
          type: string
        age:
          type: integer
"""

    result = generate_types(spec)

    assert "class Person(TypedDict):" in result
    assert "name: str" in result
    assert "age: NotRequired[int]" in result


def test_enum_schema():
    """Test generating Literal for enum schemas."""
    spec = """
openapi: 3.0.0
info:
  title: Test API
  version: 1.0.0
components:
  schemas:
    Status:
      type: string
      enum:
        - active
        - inactive
        - pending
"""

    result = generate_types(spec)

    assert "Status = Literal['active', 'inactive', 'pending']" in result


def test_array_schema():
    """Test generating list types for arrays."""
    spec = """
openapi: 3.0.0
info:
  title: Test API
  version: 1.0.0
components:
  schemas:
    StringList:
      type: object
      properties:
        items:
          type: array
          items:
            type: string
"""

    result = generate_types(spec)

    assert "list[str]" in result


def test_operation_protocol():
    """Test generating Client Protocol with @overload methods."""
    spec = """
openapi: 3.0.0
info:
  title: Test API
  version: 1.0.0
paths:
  /items/{id}:
    get:
      operationId: getItem
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: object
"""

    result = generate_types(spec)

    # Check for BaseClient and AsyncBaseClient with @overload and delegation
    assert "class BaseClient:" in result
    assert "class AsyncBaseClient:" in result
    assert "def make_request" in result
    assert "async def make_request" in result
    assert "@overload" in result
    assert "def __call__" in result
    assert "async def __call__" in result
    assert "self.make_request(" in result
    assert "await self.make_request(" in result

    # Check for path params TypedDict
    assert "class GetitemPathParams(TypedDict):" in result
    assert "id: int" in result

    # Check for the overload with correct parameters and response type
    assert "method: Literal['GET']" in result
    assert "path: Literal['/items/{id}']" in result
    # Check for keyword-only marker
    assert "*, path_params: GetitemPathParams" in result
    assert (
        "-> dict[str, Any]:" in result
    )  # Response type for object schema (modern syntax)
    
    # Verify that query_params and body are NOT in the overload (since GET with path params doesn't have them)
    # The overload should end with just path_params
    assert "*, path_params: GetitemPathParams) -> dict[str, Any]:" in result
    
    # Verify that the implementation method has optional parameters
    assert "path_params: Any | None=None" in result
    assert "query_params: Any | None=None" in result
    assert "body: Any | None=None" in result


def test_json_format():
    """Test parsing JSON format specs."""
    spec = '{"openapi": "3.0.0", "info": {"title": "Test", "version": "1.0.0"}, "components": {"schemas": {}}}'

    result = generate_types(spec, format="json")

    # Should not raise an error
    assert isinstance(result, str)


def test_reference_handling():
    """Test handling of $ref references."""
    spec = """
openapi: 3.0.0
info:
  title: Test API
  version: 1.0.0
components:
  schemas:
    User:
      type: object
      properties:
        role:
          $ref: '#/components/schemas/Role'
    Role:
      type: string
      enum:
        - admin
        - user
"""

    result = generate_types(spec)

    assert "role: NotRequired[Role]" in result
    assert "Role = Literal['admin', 'user']" in result


def test_optional_query_params():
    """Test that query parameters are optional when all fields are NotRequired."""
    spec = """
openapi: 3.0.0
info:
  title: Test API
  version: 1.0.0
paths:
  /users:
    get:
      operationId: listUsers
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
        - name: offset
          in: query
          schema:
            type: integer
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
"""

    result = generate_types(spec)

    # Check that query params TypedDict is created with NotRequired fields
    assert "class ListusersQueryParams(TypedDict):" in result
    assert "limit: NotRequired[int]" in result
    assert "offset: NotRequired[int]" in result
    
    # Check that query_params parameter has a default value (=...) in the overload
    # This makes it optional to pass
    assert "query_params: ListusersQueryParams=..." in result
    
    # Verify the implementation still has the optional parameter
    assert "query_params: Any | None=None" in result


def test_operation_id_edge_cases():
    """Test that operationId with special characters is properly sanitized."""
    spec = """
openapi: 3.0.0
info:
  title: Test API
  version: 1.0.0
paths:
  /users:
    get:
      operationId: users:list
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
  /items:
    get:
      operationId: api.v1.items
      responses:
        '200':
          description: Success
  /products:
    get:
      operationId: products/search
      responses:
        '200':
          description: Success
  /orders:
    get:
      operationId: orders-list-all
      responses:
        '200':
          description: Success
"""

    result = generate_types(spec)

    # Check that special characters in operationId are properly handled
    # users:list -> UsersList
    assert "def __call__(self, method: Literal['GET'], path: Literal['/users'])" in result
    
    # api.v1.items -> ApiV1Items
    assert "def __call__(self, method: Literal['GET'], path: Literal['/items'])" in result
    
    # products/search -> ProductsSearch
    assert "def __call__(self, method: Literal['GET'], path: Literal['/products'])" in result
    
    # orders-list-all -> OrdersListAll
    assert "def __call__(self, method: Literal['GET'], path: Literal['/orders'])" in result
    
    # The main check: no invalid Python identifiers should be in the generated code
    # Check that none of the original operationIds with special chars appear as-is
    assert "users:list" not in result  # Colons should not appear in identifiers
    assert "api.v1.items" not in result  # Dots should not appear in identifiers (except in dict keys)
    assert "products/search" not in result  # Slashes should not appear except in path Literals
    assert "orders-list-all" not in result  # Hyphens should not appear in identifiers
