#!/bin/bash
set -e

echo "========================================="
echo "Testing all SQLAlchemy AsyncIO Anyio demos"
echo "========================================="
echo ""

# Clean up any existing databases
rm -f *.db

echo "1. Testing standard_demo.py..."
uv run standard_demo.py > /dev/null 2>&1 && echo "   ✓ Success" || echo "   ✗ Failed"

echo "2. Testing demo.py..."
uv run demo.py > /dev/null 2>&1 && echo "   ✓ Success" || echo "   ✗ Failed"

echo "3. Testing advanced_demo.py..."
uv run advanced_demo.py > /dev/null 2>&1 && echo "   ✓ Success" || echo "   ✗ Failed"

echo "4. Testing comparison.py..."
uv run comparison.py > /dev/null 2>&1 && echo "   ✓ Success" || echo "   ✗ Failed"

echo ""
echo "========================================="
echo "All tests completed!"
echo "========================================="
