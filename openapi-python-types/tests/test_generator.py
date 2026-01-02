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
    """Test generating List types for arrays."""
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
    
    assert "List[str]" in result


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
    
    # Check for Client Protocol with @overload
    assert "class Client(Protocol):" in result
    assert "@overload" in result
    assert "def __call__" in result
    
    # Check for path params TypedDict
    assert "class GetitemPathParams(TypedDict):" in result
    assert "id: int" in result
    
    # Check for the overload with correct parameters and response type
    assert "method: Literal['GET']" in result
    assert "path: Literal['/items/{id}']" in result
    # Check for keyword-only marker
    assert "*, path_params: GetitemPathParams" in result
    assert "-> Dict[str, Any]:" in result  # Response type for object schema


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
