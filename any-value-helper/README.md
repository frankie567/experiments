# AnyValue Helper for Testing

A smarter alternative to `unittest.mock.ANY` that allows type checking and validation constraints.

## Overview

This experiment implements an `AnyValue` matcher for testing that extends the functionality of `unittest.mock.ANY` by supporting:

- **Type checking**: Accept specific types or union of types
- **None support**: Explicitly allow or disallow None values
- **Validation constraints**: Use `annotated-types` for advanced validation (length, ranges, patterns, etc.)
- **Mock integration**: Works seamlessly with `unittest.mock` for validating call arguments

## Problem Statement

In standard `unittest.mock`, the `ANY` matcher equals any value, which is useful but too permissive. Sometimes you need to verify that a value is of a specific type or meets certain constraints without checking the exact value.

## Solution

The `AnyValue` class provides a configurable matcher that can:

1. Match specific type(s) using Python's type system
2. Accept None values when explicitly specified
3. Apply validation constraints using `annotated-types`
4. Work transparently with mock assertions

## API Usage

```python
from any_value import AnyValue
from annotated_types import Ge, Le, Len, Gt, Predicate
from datetime import datetime
from unittest.mock import Mock

# Basic type matching
assert 42 == AnyValue(int)
assert "hello" == AnyValue(str)
assert datetime.now() == AnyValue(datetime)

# Multiple types with union operator
assert 42 == AnyValue(int | float)
assert "test" == AnyValue(str | bytes)

# None support
assert None == AnyValue(None)
assert None == AnyValue(str | None)
assert 42 == AnyValue(int | None)

# Validation constraints
assert 42 == AnyValue(int, Ge(0))  # Non-negative integer
assert "hello" == AnyValue(str, Len(5, 5))  # String of length 5
assert 99 == AnyValue(int, Ge(0), Le(100))  # Integer between 0 and 100

# Predicate validators
is_even = Predicate(lambda x: x % 2 == 0)
assert 42 == AnyValue(int, is_even)

# Custom callable validators
def is_palindrome(s: str) -> bool:
    return s == s[::-1]

assert "racecar" == AnyValue(str, is_palindrome)

# Integration with unittest.mock
mock_func = Mock()
mock_func(42, "test", datetime.now())

# Verify calls with flexible matching
mock_func.assert_called_once_with(
    AnyValue(int, Ge(0)),
    AnyValue(str, Len(4, 10)),
    AnyValue(datetime)
)
```

## Files

- `any_value.py` - Main implementation of the AnyValue class
- `test_any_value.py` - Comprehensive tests demonstrating all features
- `demo.py` - Interactive demo showing various use cases
- `pyproject.toml` - Dependencies and project configuration

## Running the Experiment

```bash
# Run tests with pytest
uv run pytest test_any_value.py -v

# Run demo
uv run demo.py
```

## Implementation Details

The `AnyValue` class implements the `__eq__` and `__ne__` methods to compare values against:

1. **Type constraints**: Checks if the value matches the specified type(s)
2. **None handling**: Special handling for None type in unions
3. **annotated-types validation**: Applies validation predicates from annotated-types (Ge, Le, Gt, Lt, Len, MultipleOf, Predicate)
4. **Custom callable validators**: Supports any callable that takes a value and returns a boolean
5. **Mock compatibility**: Works with mock's comparison mechanism

### Better Error Messages

The implementation provides descriptive error messages when assertions fail:

- **Type mismatches**: Shows expected type vs actual type with the value
- **Validator failures**: Indicates which validator failed and why
- **pytest integration**: Error messages are included in pytest's assertion output via `__repr__`

Example error output:
```
AssertionError: assert 'hello' == AnyValue(int)
  Reason: Expected type int, got str ('hello')

AssertionError: assert 5 == AnyValue(int, Ge(ge=10))
  Reason: Validator Ge(ge=10) failed: 5 is not >= 10
```

## Design Decisions

- **Class-based approach**: Instantiate with parameters rather than a global constant
- **Type-first API**: The first argument is always the type constraint
- **Union support**: Use Python's `|` operator for multiple types
- **Explicit None**: None must be explicitly included in the type union
- **annotated-types integration**: Leverage existing validation library for constraints
- **Hard dependency**: annotated-types is a required dependency (not optional)
- **Pytest for testing**: Tests use pytest framework for better test discovery and reporting
