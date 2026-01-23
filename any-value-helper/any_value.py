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
        self._last_failure_reason: str | None = None
        
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
    
    def _format_type_constraint(self) -> str:
        """
        Format the type constraint as a readable string.
        
        Returns:
            A formatted string representation of the type constraint
        """
        if len(self._accepted_types) == 1:
            t = self._accepted_types[0]
            if t is None:
                return "None"
            return getattr(t, '__name__', str(t))
        else:
            type_names = []
            for t in self._accepted_types:
                if t is None:
                    type_names.append("None")
                else:
                    type_names.append(getattr(t, '__name__', str(t)))
            return " | ".join(type_names)
    
    def _check_type(self, other: Any) -> tuple[bool, str | None]:
        """
        Check if the value matches the type constraint.
        
        Args:
            other: The value to check
            
        Returns:
            A tuple of (passed, failure_reason). If passed is True, failure_reason is None.
        """
        # Check if None is allowed
        if other is None:
            if None in self._accepted_types:
                return (True, None)
            else:
                expected = self._format_type_constraint()
                return (False, f"Expected type {expected}, got None")
        
        # Check if the value's type matches any accepted type
        for accepted_type in self._accepted_types:
            if accepted_type is not None and isinstance(other, accepted_type):
                return (True, None)
        
        # Type mismatch
        actual_type = type(other).__name__
        expected = self._format_type_constraint()
        return (False, f"Expected type {expected}, got {actual_type} ({other!r})")
    
    def _check_validators(self, other: Any) -> tuple[bool, str | None]:
        """
        Check if the value passes all validators.
        
        Args:
            other: The value to validate
            
        Returns:
            A tuple of (passed, failure_reason). If passed is True, failure_reason is None.
        """
        if not self.validators:
            return (True, None)
        
        # Apply each validator
        for validator in self.validators:
            try:
                # Handle annotated-types validators
                if isinstance(validator, Ge):
                    if not (other >= validator.ge):
                        return (False, f"Validator {validator} failed: {other!r} is not >= {validator.ge}")
                elif isinstance(validator, Le):
                    if not (other <= validator.le):
                        return (False, f"Validator {validator} failed: {other!r} is not <= {validator.le}")
                elif isinstance(validator, Gt):
                    if not (other > validator.gt):
                        return (False, f"Validator {validator} failed: {other!r} is not > {validator.gt}")
                elif isinstance(validator, Lt):
                    if not (other < validator.lt):
                        return (False, f"Validator {validator} failed: {other!r} is not < {validator.lt}")
                elif isinstance(validator, Len):
                    # Check length constraints
                    try:
                        length = len(other)
                        if validator.min_length is not None and length < validator.min_length:
                            return (False, f"Validator {validator} failed: length {length} is less than min {validator.min_length}")
                        if validator.max_length is not None and length > validator.max_length:
                            return (False, f"Validator {validator} failed: length {length} exceeds max {validator.max_length}")
                    except TypeError:
                        # Object doesn't have a length
                        return (False, f"Validator {validator} failed: {other!r} has no length")
                elif isinstance(validator, MultipleOf):
                    if not (other % validator.multiple_of == 0):
                        return (False, f"Validator {validator} failed: {other!r} is not a multiple of {validator.multiple_of}")
                elif isinstance(validator, Predicate):
                    if not validator.func(other):
                        return (False, f"Predicate validator failed for {other!r}")
                elif callable(validator):
                    # Try calling the validator
                    if not validator(other):
                        validator_name = getattr(validator, '__name__', str(validator))
                        return (False, f"Custom validator '{validator_name}' failed for {other!r}")
                else:
                    # Unknown validator type, skip
                    continue
            except Exception as e:
                # If validation fails with an exception, consider it failed
                return (False, f"Validator {validator} raised exception: {e}")
        
        return (True, None)
    
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
        type_passed, type_reason = self._check_type(other)
        if not type_passed:
            self._last_failure_reason = type_reason
            return False
        
        # Check validators
        validator_passed, validator_reason = self._check_validators(other)
        if not validator_passed:
            self._last_failure_reason = validator_reason
            return False
        
        self._last_failure_reason = None
        return True
    
    def __ne__(self, other: Any) -> bool:
        """
        Check inequality. This enables better pytest assertion messages.
        
        Args:
            other: The value to compare against
            
        Returns:
            True if the value does NOT match the type and validators
        """
        return not self.__eq__(other)
    
    def __repr__(self) -> str:
        """
        Return a string representation of the AnyValue matcher.
        
        Returns:
            A string describing the matcher
        """
        type_str = self._format_type_constraint()
        if self.validators:
            validator_strs = [str(v) for v in self.validators]
            result = f"AnyValue({type_str}, {', '.join(validator_strs)})"
        else:
            result = f"AnyValue({type_str})"
        
        # Add failure reason if available (for better pytest output)
        if self._last_failure_reason:
            result += f"\n  Reason: {self._last_failure_reason}"
        
        return result
