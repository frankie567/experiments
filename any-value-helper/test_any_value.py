#!/usr/bin/env python3
"""
Tests for the AnyValue helper.

This module contains comprehensive tests demonstrating all features of AnyValue.
"""

import pytest
from any_value import AnyValue
from annotated_types import Ge, Le, Len, Gt, Lt, Predicate
from datetime import datetime
from unittest.mock import Mock


def test_basic_type_matching():
    """Test basic type matching with single types."""
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


def test_type_mismatch():
    """Test that type mismatches are correctly rejected."""
    # String vs int
    assert not ("hello" == AnyValue(int))
    
    # Int vs string
    assert not (42 == AnyValue(str))
    
    # Float vs int (note: isinstance(42, float) is False)
    # But isinstance(42.0, float) is True
    assert not (42 == AnyValue(float))


def test_union_types():
    """Test union types using the | operator."""
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


def test_none_support():
    """Test None type support."""
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


def test_annotated_types_ge():
    """Test annotated-types Ge (greater or equal) constraint."""
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


def test_annotated_types_le():
    """Test annotated-types Le (less or equal) constraint."""
    # Values <= 100
    assert 100 == AnyValue(int, Le(100))
    assert 50 == AnyValue(int, Le(100))
    assert 0 == AnyValue(int, Le(100))
    assert -10 == AnyValue(int, Le(100))
    
    # Should fail for greater
    assert not (101 == AnyValue(int, Le(100)))
    assert not (200 == AnyValue(int, Le(100)))


def test_annotated_types_len():
    """Test annotated-types Len constraint."""
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


def test_multiple_constraints():
    """Test multiple constraints together."""
    # Range: 0 <= x <= 100
    assert 0 == AnyValue(int, Ge(0), Le(100))
    assert 50 == AnyValue(int, Ge(0), Le(100))
    assert 100 == AnyValue(int, Ge(0), Le(100))
    
    # Out of range
    assert not (-1 == AnyValue(int, Ge(0), Le(100)))
    assert not (101 == AnyValue(int, Ge(0), Le(100)))


def test_predicate_validator():
    """Test annotated-types Predicate validator."""
    # Custom predicate - even numbers
    is_even = Predicate(lambda x: x % 2 == 0)
    assert 42 == AnyValue(int, is_even)
    assert 100 == AnyValue(int, is_even)
    assert not (43 == AnyValue(int, is_even))
    
    # Predicate for positive numbers
    is_positive = Predicate(lambda x: x > 0)
    assert 1 == AnyValue(int, is_positive)
    assert 100 == AnyValue(int, is_positive)
    assert not (0 == AnyValue(int, is_positive))
    assert not (-1 == AnyValue(int, is_positive))
    
    # String predicate - starts with specific prefix
    starts_with_hello = Predicate(lambda x: x.startswith("hello"))
    assert "hello world" == AnyValue(str, starts_with_hello)
    assert "hello there" == AnyValue(str, starts_with_hello)
    assert not ("goodbye" == AnyValue(str, starts_with_hello))
    
    # Combine predicate with other constraints
    assert 42 == AnyValue(int, Ge(0), is_even)
    assert not (43 == AnyValue(int, Ge(0), is_even))


def test_callable_validator():
    """Test custom callable validators."""
    # Simple callable validator
    def is_palindrome(s: str) -> bool:
        return s == s[::-1]
    
    assert "racecar" == AnyValue(str, is_palindrome)
    assert "level" == AnyValue(str, is_palindrome)
    assert not ("hello" == AnyValue(str, is_palindrome))
    
    # Callable for number validation
    def is_prime(n: int) -> bool:
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    assert 7 == AnyValue(int, is_prime)
    assert 13 == AnyValue(int, is_prime)
    assert not (4 == AnyValue(int, is_prime))
    assert not (10 == AnyValue(int, is_prime))
    
    # Combine callable with annotated-types constraints
    assert 7 == AnyValue(int, Ge(0), is_prime)
    assert not (-7 == AnyValue(int, Ge(0), is_prime))


def test_mock_integration():
    """Test integration with unittest.mock."""
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
    
    # Test with Predicate
    mock_func.reset_mock()
    is_even = Predicate(lambda x: x % 2 == 0)
    mock_func(42)
    
    mock_func.assert_called_once_with(
        AnyValue(int, is_even)
    )
    
    # Test with callable
    mock_func.reset_mock()
    def is_positive(x: int) -> bool:
        return x > 0
    mock_func(100)
    
    mock_func.assert_called_once_with(
        AnyValue(int, is_positive)
    )


def test_complex_scenarios():
    """Test complex real-world scenarios."""
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
    
    # Scenario 3: With custom validators
    mock_validator = Mock()
    is_valid_email = Predicate(lambda x: "@" in x and "." in x)
    mock_validator.send_email("user@example.com")
    
    mock_validator.send_email.assert_called_once_with(
        AnyValue(str, is_valid_email)
    )


def test_error_messages():
    """Test that error messages are descriptive."""
    # Test type mismatch error
    matcher = AnyValue(int)
    result = matcher == "hello"
    assert result is False
    assert hasattr(matcher, '_last_failure_reason')
    assert 'Expected type int' in matcher._last_failure_reason
    assert 'str' in matcher._last_failure_reason
    
    # Test validator failure error
    matcher = AnyValue(int, Ge(10))
    result = matcher == 5
    assert result is False
    assert 'Validator' in matcher._last_failure_reason
    assert 'not >= 10' in matcher._last_failure_reason
    
    # Test length validator error
    matcher = AnyValue(str, Len(5, 5))
    result = matcher == "hi"
    assert result is False
    assert 'length' in matcher._last_failure_reason
    
    # Test __ne__ works correctly
    matcher = AnyValue(int)
    assert matcher != "hello"
    assert not (matcher != 42)
