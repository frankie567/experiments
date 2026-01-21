#!/usr/bin/env python3
"""
Tests for the AnyValue helper.

This module contains comprehensive tests demonstrating all features of AnyValue.
"""

from any_value import AnyValue
from annotated_types import Ge, Le, Len, Gt, Lt
from datetime import datetime
from unittest.mock import Mock


def test_basic_type_matching():
    """Test basic type matching with single types."""
    print("Testing basic type matching...")
    
    # Integer matching
    assert 42 == AnyValue(int)
    assert -10 == AnyValue(int)
    assert 0 == AnyValue(int)
    
    # String matching
    assert "hello" == AnyValue(str)
    assert "" == AnyValue(str)
    
    # Float matching
    assert 3.14 == AnyValue(float)
    assert -2.5 == AnyValue(float)
    
    # Boolean matching (note: bool is a subclass of int)
    assert True == AnyValue(bool)
    assert False == AnyValue(bool)
    
    # Datetime matching
    assert datetime.now() == AnyValue(datetime)
    
    print("✓ Basic type matching passed")


def test_type_mismatch():
    """Test that type mismatches are correctly rejected."""
    print("Testing type mismatches...")
    
    # String vs int
    assert not ("hello" == AnyValue(int))
    
    # Int vs string
    assert not (42 == AnyValue(str))
    
    # Float vs int (note: isinstance(42, float) is False)
    # But isinstance(42.0, float) is True
    assert not (42 == AnyValue(float))
    
    print("✓ Type mismatch detection passed")


def test_union_types():
    """Test union types using the | operator."""
    print("Testing union types...")
    
    # int | float
    assert 42 == AnyValue(int | float)
    assert 3.14 == AnyValue(int | float)
    
    # str | bytes
    assert "hello" == AnyValue(str | bytes)
    assert b"hello" == AnyValue(str | bytes)
    
    # Multiple types
    assert 42 == AnyValue(int | float | str)
    assert 3.14 == AnyValue(int | float | str)
    assert "test" == AnyValue(int | float | str)
    
    print("✓ Union types passed")


def test_none_support():
    """Test None type support."""
    print("Testing None support...")
    
    # None type explicitly
    assert None == AnyValue(None)
    
    # None in union
    assert None == AnyValue(str | None)
    assert None == AnyValue(int | None)
    assert None == AnyValue(int | str | None)
    
    # Actual values still work with None in union
    assert 42 == AnyValue(int | None)
    assert "test" == AnyValue(str | None)
    
    # None should not match when not specified
    assert not (None == AnyValue(int))
    assert not (None == AnyValue(str))
    
    print("✓ None support passed")


def test_annotated_types_ge():
    """Test annotated-types Ge (greater or equal) constraint."""
    print("Testing Ge constraint...")
    
    # Non-negative integers
    assert 0 == AnyValue(int, Ge(0))
    assert 42 == AnyValue(int, Ge(0))
    assert 1000 == AnyValue(int, Ge(0))
    
    # Should fail for negative
    assert not (-1 == AnyValue(int, Ge(0)))
    assert not (-100 == AnyValue(int, Ge(0)))
    
    # With different thresholds
    assert 10 == AnyValue(int, Ge(10))
    assert 100 == AnyValue(int, Ge(10))
    assert not (9 == AnyValue(int, Ge(10)))
    
    print("✓ Ge constraint passed")


def test_annotated_types_le():
    """Test annotated-types Le (less or equal) constraint."""
    print("Testing Le constraint...")
    
    # Values <= 100
    assert 100 == AnyValue(int, Le(100))
    assert 50 == AnyValue(int, Le(100))
    assert 0 == AnyValue(int, Le(100))
    assert -10 == AnyValue(int, Le(100))
    
    # Should fail for greater
    assert not (101 == AnyValue(int, Le(100)))
    assert not (200 == AnyValue(int, Le(100)))
    
    print("✓ Le constraint passed")


def test_annotated_types_len():
    """Test annotated-types Len constraint."""
    print("Testing Len constraint...")
    
    # String length
    assert "hello" == AnyValue(str, Len(5, 5))  # Exact length 5
    assert "test" == AnyValue(str, Len(4, 4))
    
    # Should fail for different lengths
    assert not ("hello" == AnyValue(str, Len(4, 4)))
    assert not ("test" == AnyValue(str, Len(5, 5)))
    
    # Range of lengths
    assert "hi" == AnyValue(str, Len(1, 10))
    assert "hello" == AnyValue(str, Len(1, 10))
    assert "123456789" == AnyValue(str, Len(1, 10))
    
    # List length
    assert [1, 2, 3] == AnyValue(list, Len(3, 3))
    assert [1, 2, 3, 4, 5] == AnyValue(list, Len(1, 10))
    
    print("✓ Len constraint passed")


def test_multiple_constraints():
    """Test multiple constraints together."""
    print("Testing multiple constraints...")
    
    # Range: 0 <= x <= 100
    assert 0 == AnyValue(int, Ge(0), Le(100))
    assert 50 == AnyValue(int, Ge(0), Le(100))
    assert 100 == AnyValue(int, Ge(0), Le(100))
    
    # Out of range
    assert not (-1 == AnyValue(int, Ge(0), Le(100)))
    assert not (101 == AnyValue(int, Ge(0), Le(100)))
    
    print("✓ Multiple constraints passed")


def test_mock_integration():
    """Test integration with unittest.mock."""
    print("Testing unittest.mock integration...")
    
    # Create a mock function
    mock_func = Mock()
    
    # Call it with some values
    mock_func(42, "test", datetime.now())
    
    # Verify with AnyValue matchers
    mock_func.assert_called_once_with(
        AnyValue(int),
        AnyValue(str),
        AnyValue(datetime)
    )
    
    # Reset and test with constraints
    mock_func.reset_mock()
    mock_func(100, "hello")
    
    mock_func.assert_called_once_with(
        AnyValue(int, Ge(0), Le(1000)),
        AnyValue(str, Len(5, 5))
    )
    
    # Test with union types
    mock_func.reset_mock()
    mock_func(42, 3.14, "test")
    
    mock_func.assert_called_once_with(
        AnyValue(int | float),
        AnyValue(int | float),
        AnyValue(str | bytes)
    )
    
    # Test with None
    mock_func.reset_mock()
    mock_func(None, "test")
    
    mock_func.assert_called_once_with(
        AnyValue(int | None),
        AnyValue(str)
    )
    
    print("✓ Mock integration passed")


def test_complex_scenarios():
    """Test complex real-world scenarios."""
    print("Testing complex scenarios...")
    
    # Scenario 1: API response validation
    mock_api = Mock()
    mock_api.create_user(
        user_id=12345,
        username="john_doe",
        email="john@example.com",
        age=25
    )
    
    mock_api.create_user.assert_called_once_with(
        user_id=AnyValue(int, Ge(1)),  # Positive user ID
        username=AnyValue(str, Len(1, 50)),  # Username between 1-50 chars
        email=AnyValue(str),  # Any string email
        age=AnyValue(int, Ge(0), Le(150))  # Age between 0-150
    )
    
    # Scenario 2: Optional parameters
    mock_service = Mock()
    mock_service.process(data="test", timestamp=datetime.now(), metadata=None)
    
    mock_service.process.assert_called_once_with(
        data=AnyValue(str),
        timestamp=AnyValue(datetime),
        metadata=AnyValue(dict | None)  # Optional metadata
    )
    
    print("✓ Complex scenarios passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Running AnyValue Tests")
    print("=" * 60)
    print()
    
    test_basic_type_matching()
    test_type_mismatch()
    test_union_types()
    test_none_support()
    test_annotated_types_ge()
    test_annotated_types_le()
    test_annotated_types_len()
    test_multiple_constraints()
    test_mock_integration()
    test_complex_scenarios()
    
    print()
    print("=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
