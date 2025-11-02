"""Test script for the demo PyO3 extension."""

def test_extension():
    """Test the Rust extension functions."""
    try:
        from demo_pyo3_extension import add, multiply, greet
        
        # Test add function
        result = add(5, 3)
        assert result == 8, f"Expected 8, got {result}"
        print(f"✓ add(5, 3) = {result}")
        
        # Test multiply function
        result = multiply(4, 7)
        assert result == 28, f"Expected 28, got {result}"
        print(f"✓ multiply(4, 7) = {result}")
        
        # Test greet function
        result = greet("World")
        assert result == "Hello, World!", f"Expected 'Hello, World!', got {result}"
        print(f"✓ greet('World') = {result}")
        
        print("\n✅ All tests passed!")
        
    except ImportError as e:
        print(f"❌ Failed to import extension: {e}")
        print("Make sure the extension is built first.")
        return False
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True


if __name__ == "__main__":
    import sys
    success = test_extension()
    sys.exit(0 if success else 1)
