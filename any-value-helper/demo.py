#!/usr/bin/env python3
"""
Demo script showcasing AnyValue usage.

This script demonstrates various use cases of the AnyValue helper
in testing scenarios.
"""

from any_value import AnyValue
from annotated_types import Ge, Le, Len, Gt, Lt
from datetime import datetime
from unittest.mock import Mock


def demo_basic_usage():
    """Demonstrate basic type matching."""
    print("=" * 60)
    print("Basic Type Matching")
    print("=" * 60)
    
    print("\n1. Integer matching:")
    print(f"   42 == AnyValue(int) → {42 == AnyValue(int)}")
    print(f"   'hello' == AnyValue(int) → {'hello' == AnyValue(int)}")
    
    print("\n2. String matching:")
    print(f"   'hello' == AnyValue(str) → {'hello' == AnyValue(str)}")
    print(f"   42 == AnyValue(str) → {42 == AnyValue(str)}")
    
    print("\n3. Datetime matching:")
    now = datetime.now()
    print(f"   datetime.now() == AnyValue(datetime) → {now == AnyValue(datetime)}")
    

def demo_union_types():
    """Demonstrate union type matching."""
    print("\n" + "=" * 60)
    print("Union Types (Multiple Types)")
    print("=" * 60)
    
    print("\n1. int | float:")
    print(f"   42 == AnyValue(int | float) → {42 == AnyValue(int | float)}")
    print(f"   3.14 == AnyValue(int | float) → {3.14 == AnyValue(int | float)}")
    print(f"   'hello' == AnyValue(int | float) → {'hello' == AnyValue(int | float)}")
    
    print("\n2. str | bytes:")
    print(f"   'hello' == AnyValue(str | bytes) → {'hello' == AnyValue(str | bytes)}")
    print(f"   b'hello' == AnyValue(str | bytes) → {b'hello' == AnyValue(str | bytes)}")


def demo_none_support():
    """Demonstrate None type support."""
    print("\n" + "=" * 60)
    print("None Type Support")
    print("=" * 60)
    
    print("\n1. Explicit None:")
    print(f"   None == AnyValue(None) → {None == AnyValue(None)}")
    
    print("\n2. Optional types (with None):")
    print(f"   None == AnyValue(str | None) → {None == AnyValue(str | None)}")
    print(f"   'hello' == AnyValue(str | None) → {'hello' == AnyValue(str | None)}")
    print(f"   None == AnyValue(int | None) → {None == AnyValue(int | None)}")
    print(f"   42 == AnyValue(int | None) → {42 == AnyValue(int | None)}")
    
    print("\n3. None rejected when not specified:")
    print(f"   None == AnyValue(int) → {None == AnyValue(int)}")
    print(f"   None == AnyValue(str) → {None == AnyValue(str)}")


def demo_validation_constraints():
    """Demonstrate annotated-types validation constraints."""
    print("\n" + "=" * 60)
    print("Validation Constraints")
    print("=" * 60)
    
    print("\n1. Ge (Greater or Equal) - Non-negative integers:")
    print(f"   0 == AnyValue(int, Ge(0)) → {0 == AnyValue(int, Ge(0))}")
    print(f"   42 == AnyValue(int, Ge(0)) → {42 == AnyValue(int, Ge(0))}")
    print(f"   -1 == AnyValue(int, Ge(0)) → {-1 == AnyValue(int, Ge(0))}")
    
    print("\n2. Le (Less or Equal) - Values <= 100:")
    print(f"   50 == AnyValue(int, Le(100)) → {50 == AnyValue(int, Le(100))}")
    print(f"   100 == AnyValue(int, Le(100)) → {100 == AnyValue(int, Le(100))}")
    print(f"   101 == AnyValue(int, Le(100)) → {101 == AnyValue(int, Le(100))}")
    
    print("\n3. Len - String length:")
    print(f"   'hello' == AnyValue(str, Len(5, 5)) → {'hello' == AnyValue(str, Len(5, 5))}")
    print(f"   'hi' == AnyValue(str, Len(5, 5)) → {'hi' == AnyValue(str, Len(5, 5))}")
    
    print("\n4. Multiple constraints - Range 0 to 100:")
    print(f"   50 == AnyValue(int, Ge(0), Le(100)) → {50 == AnyValue(int, Ge(0), Le(100))}")
    print(f"   -1 == AnyValue(int, Ge(0), Le(100)) → {-1 == AnyValue(int, Ge(0), Le(100))}")
    print(f"   101 == AnyValue(int, Ge(0), Le(100)) → {101 == AnyValue(int, Ge(0), Le(100))}")


def demo_mock_integration():
    """Demonstrate integration with unittest.mock."""
    print("\n" + "=" * 60)
    print("Mock Integration")
    print("=" * 60)
    
    print("\n1. Simple mock call verification:")
    mock_func = Mock()
    mock_func(42, "test", datetime.now())
    
    try:
        mock_func.assert_called_once_with(
            AnyValue(int),
            AnyValue(str),
            AnyValue(datetime)
        )
        print("   ✓ Mock assertion passed with AnyValue matchers")
    except AssertionError as e:
        print(f"   ✗ Mock assertion failed: {e}")
    
    print("\n2. Mock with validation constraints:")
    mock_func.reset_mock()
    mock_func(100, "hello")
    
    try:
        mock_func.assert_called_once_with(
            AnyValue(int, Ge(0), Le(1000)),
            AnyValue(str, Len(5, 5))
        )
        print("   ✓ Mock assertion passed with constraints")
    except AssertionError as e:
        print(f"   ✗ Mock assertion failed: {e}")
    
    print("\n3. Mock with union types:")
    mock_func.reset_mock()
    mock_func(42, 3.14, "test")
    
    try:
        mock_func.assert_called_once_with(
            AnyValue(int | float),
            AnyValue(int | float),
            AnyValue(str | bytes)
        )
        print("   ✓ Mock assertion passed with union types")
    except AssertionError as e:
        print(f"   ✗ Mock assertion failed: {e}")


def demo_real_world_example():
    """Demonstrate a real-world testing scenario."""
    print("\n" + "=" * 60)
    print("Real-World Example: API Testing")
    print("=" * 60)
    
    print("\nScenario: Testing a user creation API")
    print("Code:")
    print("""
    mock_api = Mock()
    mock_api.create_user(
        user_id=12345,
        username="john_doe",
        email="john@example.com",
        age=25
    )
    
    # Verify the call with flexible matching
    mock_api.create_user.assert_called_once_with(
        user_id=AnyValue(int, Ge(1)),           # Positive user ID
        username=AnyValue(str, Len(1, 50)),      # Username 1-50 chars
        email=AnyValue(str),                     # Any string email
        age=AnyValue(int, Ge(0), Le(150))       # Age 0-150
    )
    """)
    
    # Execute the example
    mock_api = Mock()
    mock_api.create_user(
        user_id=12345,
        username="john_doe",
        email="john@example.com",
        age=25
    )
    
    try:
        mock_api.create_user.assert_called_once_with(
            user_id=AnyValue(int, Ge(1)),
            username=AnyValue(str, Len(1, 50)),
            email=AnyValue(str),
            age=AnyValue(int, Ge(0), Le(150))
        )
        print("\nResult: ✓ API call validated successfully")
        print("The call matches all constraints:")
        print("  - user_id is a positive integer")
        print("  - username is a string with 1-50 characters")
        print("  - email is a string")
        print("  - age is an integer between 0 and 150")
    except AssertionError as e:
        print(f"\nResult: ✗ Validation failed: {e}")


def main():
    """Run all demos."""
    print("\n" + "=" * 60)
    print(" AnyValue Demo - Smarter ANY Helper for Testing")
    print("=" * 60)
    
    demo_basic_usage()
    demo_union_types()
    demo_none_support()
    demo_validation_constraints()
    demo_mock_integration()
    demo_real_world_example()
    
    print("\n" + "=" * 60)
    print(" Demo Complete!")
    print("=" * 60)
    print("\nFor more examples, run: uv run test_any_value.py")
    print()


if __name__ == "__main__":
    main()
