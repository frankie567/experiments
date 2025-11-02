#!/usr/bin/env python3
"""Comprehensive test suite for the hatchling-pyo3-plugin demo."""

import sys
import traceback


def test_imports():
    """Test that the extension can be imported."""
    print("Testing imports...")
    try:
        from demo_pyo3_extension import add, multiply, greet
        print("  ✓ Successfully imported: add, multiply, greet")
        return True
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        traceback.print_exc()
        return False


def test_add_function():
    """Test the add function."""
    print("\nTesting add function...")
    from demo_pyo3_extension import add
    
    tests = [
        ((5, 3), 8),
        ((0, 0), 0),
        ((-5, 5), 0),
        ((100, 200), 300),
        ((-10, -20), -30),
    ]
    
    for (a, b), expected in tests:
        result = add(a, b)
        if result == expected:
            print(f"  ✓ add({a}, {b}) = {result}")
        else:
            print(f"  ✗ add({a}, {b}) = {result}, expected {expected}")
            return False
    
    return True


def test_multiply_function():
    """Test the multiply function."""
    print("\nTesting multiply function...")
    from demo_pyo3_extension import multiply
    
    tests = [
        ((4, 7), 28),
        ((0, 100), 0),
        ((1, 1), 1),
        ((-5, 3), -15),
        ((10, 10), 100),
    ]
    
    for (a, b), expected in tests:
        result = multiply(a, b)
        if result == expected:
            print(f"  ✓ multiply({a}, {b}) = {result}")
        else:
            print(f"  ✗ multiply({a}, {b}) = {result}, expected {expected}")
            return False
    
    return True


def test_greet_function():
    """Test the greet function."""
    print("\nTesting greet function...")
    from demo_pyo3_extension import greet
    
    tests = [
        ("World", "Hello, World!"),
        ("Python", "Hello, Python!"),
        ("Rust", "Hello, Rust!"),
        ("PyO3", "Hello, PyO3!"),
        ("", "Hello, !"),
    ]
    
    for name, expected in tests:
        result = greet(name)
        if result == expected:
            print(f"  ✓ greet('{name}') = '{result}'")
        else:
            print(f"  ✗ greet('{name}') = '{result}', expected '{expected}'")
            return False
    
    return True


def test_type_checking():
    """Test that functions handle types correctly."""
    print("\nTesting type checking...")
    from demo_pyo3_extension import add, multiply, greet
    
    # Test that add/multiply work with large numbers
    try:
        result = add(2**62, 2**62)
        print(f"  ✓ Large number addition: {result}")
    except Exception as e:
        print(f"  ✗ Large number addition failed: {e}")
        return False
    
    # Test that greet handles different string types
    try:
        result = greet("Test 测试 🎉")
        print(f"  ✓ Unicode string handling: '{result}'")
    except Exception as e:
        print(f"  ✗ Unicode string handling failed: {e}")
        return False
    
    return True


def run_all_tests():
    """Run all tests and report results."""
    print("=" * 70)
    print("Hatchling PyO3 Plugin - Demo Extension Test Suite")
    print("=" * 70)
    
    tests = [
        ("Import Test", test_imports),
        ("Add Function", test_add_function),
        ("Multiply Function", test_multiply_function),
        ("Greet Function", test_greet_function),
        ("Type Checking", test_type_checking),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n✗ {test_name} crashed: {e}")
            traceback.print_exc()
            results.append((test_name, False))
    
    print("\n" + "=" * 70)
    print("Test Results Summary")
    print("=" * 70)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    print("=" * 70)
    print(f"Passed: {passed}/{total} tests")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
