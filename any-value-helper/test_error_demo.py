#!/usr/bin/env python3
"""
Demo script to show improved error messages with pytest.
Run with: uv run pytest test_error_demo.py -v
"""

import pytest
from any_value import AnyValue
from annotated_types import Ge, Le, Len

def test_type_mismatch_error_message():
    """This test intentionally fails to show the error message."""
    matcher = AnyValue(int)
    # This will fail and show the error message
    assert "hello" == matcher

def test_validator_failure_error_message():
    """This test intentionally fails to show validator error."""
    matcher = AnyValue(int, Ge(10))
    # This will fail and show which validator failed
    assert 5 == matcher

def test_length_validator_error():
    """This test shows length validation error."""
    matcher = AnyValue(str, Len(5, 5))
    # This will fail and show length constraint violation
    assert "hi" == matcher

if __name__ == "__main__":
    # Run pytest programmatically
    pytest.main([__file__, "-v", "--tb=short"])
