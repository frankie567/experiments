#!/usr/bin/env python3
"""
AnyValue - A smarter ANY helper for testing.

This module provides the AnyValue class, which extends unittest.mock.ANY
with type checking and validation constraints using annotated-types.
"""

from typing import Any, get_args, get_origin
import types
from annotated_types import Ge, Le, Gt, Lt, Len, MultipleOf, Predicate


class AnyValue:
    """
    A matcher that accepts values matching specific type and validation constraints.
    
    This class can be used in place of unittest.mock.ANY when you want to verify
    that a value meets certain criteria without checking the exact value.
    
    Examples:
        >>> assert 42 == AnyValue(int)
        >>> assert "hello" == AnyValue(str, Len(5))
        >>> assert None == AnyValue(None)
        >>> assert 42 == AnyValue(int | None)
        
    Args:
        type_constraint: The type(s) to match. Can be a single type, a Union type
                        using the | operator, or None to match None values.
        *validators: Optional annotated-types validators (Ge, Le, Len, etc.)
    """
    
    def __init__(self, type_constraint: Any, *validators: Any) -> None:
        """
        Initialize the AnyValue matcher.
        
        Args:
            type_constraint: The type(s) to accept. Can be:
                - A single type (e.g., int, str, datetime)
                - A union of types using | (e.g., int | float, str | None)
                - None to match None values
            *validators: annotated-types validators to apply (Ge, Le, Len, etc.)
        """
        self.type_constraint = type_constraint
        self.validators = validators
        
        # Parse the type constraint to extract accepted types
        self._accepted_types = self._parse_type_constraint(type_constraint)
    
    def _parse_type_constraint(self, type_constraint: Any) -> tuple[type | None, ...]:
        """
        Parse the type constraint into a tuple of accepted types.
        
        Args:
            type_constraint: The type constraint to parse
            
        Returns:
            A tuple of types (or None) that are accepted
        """
        # Handle None type explicitly
        if type_constraint is None or type_constraint is type(None):
            return (None,)
        
        # Handle union types (Python 3.10+ syntax: int | str)
        origin = get_origin(type_constraint)
        if origin is types.UnionType:
            # Extract types from union
            args = get_args(type_constraint)
            return tuple(None if arg is type(None) else arg for arg in args)
        
        # Handle single type
        return (type_constraint,)
    
    def _check_type(self, other: Any) -> bool:
        """
        Check if the value matches the type constraint.
        
        Args:
            other: The value to check
            
        Returns:
            True if the value matches the type constraint, False otherwise
        """
        # Check if None is allowed
        if other is None:
            return None in self._accepted_types
        
        # Check if the value's type matches any accepted type
        for accepted_type in self._accepted_types:
            if accepted_type is not None and isinstance(other, accepted_type):
                return True
        
        return False
    
    def _check_validators(self, other: Any) -> bool:
        """
        Check if the value passes all validators.
        
        Args:
            other: The value to validate
            
        Returns:
            True if all validators pass, False otherwise
        """
        if not self.validators:
            return True
        
        # Apply each validator
        for validator in self.validators:
            try:
                # Handle annotated-types validators
                if isinstance(validator, Ge):
                    if not (other >= validator.ge):
                        return False
                elif isinstance(validator, Le):
                    if not (other <= validator.le):
                        return False
                elif isinstance(validator, Gt):
                    if not (other > validator.gt):
                        return False
                elif isinstance(validator, Lt):
                    if not (other < validator.lt):
                        return False
                elif isinstance(validator, Len):
                    # Check length constraints
                    try:
                        length = len(other)
                        if validator.min_length is not None and length < validator.min_length:
                            return False
                        if validator.max_length is not None and length > validator.max_length:
                            return False
                    except TypeError:
                        # Object doesn't have a length
                        return False
                elif isinstance(validator, MultipleOf):
                    if not (other % validator.multiple_of == 0):
                        return False
                elif isinstance(validator, Predicate):
                    if not validator.func(other):
                        return False
                elif callable(validator):
                    # Try calling the validator
                    if not validator(other):
                        return False
                else:
                    # Unknown validator type, skip
                    continue
            except Exception:
                # If validation fails with an exception, consider it failed
                return False
        
        return True
    
    def __eq__(self, other: Any) -> bool:
        """
        Compare the AnyValue matcher with another value.
        
        This method is called when comparing with ==, including in unittest.mock
        assertions like assert_called_with.
        
        Args:
            other: The value to compare against
            
        Returns:
            True if the value matches the type and validators, False otherwise
        """
        # Check type constraint
        if not self._check_type(other):
            return False
        
        # Check validators
        if not self._check_validators(other):
            return False
        
        return True
    
    def __repr__(self) -> str:
        """
        Return a string representation of the AnyValue matcher.
        
        Returns:
            A string describing the matcher
        """
        type_str = str(self.type_constraint)
        if self.validators:
            validator_strs = [str(v) for v in self.validators]
            return f"AnyValue({type_str}, {', '.join(validator_strs)})"
        return f"AnyValue({type_str})"
