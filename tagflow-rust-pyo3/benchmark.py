#!/usr/bin/env python3
"""
Simple performance comparison between Tagflow implementations.

This script tests the basic performance of the Rust+PyO3 implementation
compared to the Python reimplementation.
"""

import time
import sys
import os

# Add the Python reimplementation to the path
sys.path.insert(0, '../tagflow-reimplementation')

try:
    from tagflow_reimpl import Document as PythonDocument
    PYTHON_AVAILABLE = True
except ImportError:
    print("Warning: Python reimplementation not available")
    PYTHON_AVAILABLE = False

from tagflow_rust import Document as RustDocument


def benchmark_function(func, iterations=1000):
    """Benchmark a function over multiple iterations."""
    start_time = time.perf_counter()
    for _ in range(iterations):
        func()
    end_time = time.perf_counter()
    return end_time - start_time


def generate_simple_page_python():
    """Generate simple page using Python reimplementation."""
    doc = PythonDocument()
    with doc.tag("html"):
        with doc.tag("head"):
            with doc.tag("title"):
                doc.text("Simple Page")
            with doc.tag("meta", charset="utf-8"):
                pass
        with doc.tag("body"):
            with doc.tag("header"):
                with doc.tag("h1"):
                    doc.text("Welcome")
            with doc.tag("main"):
                with doc.tag("p"):
                    doc.text("This is a simple page.")
                with doc.tag("p"):
                    doc.text("It includes multiple paragraphs.")
            with doc.tag("footer"):
                with doc.tag("p"):
                    doc.text("© 2024 Test")
    return doc.render()


def generate_simple_page_rust():
    """Generate simple page using Rust implementation."""
    doc = RustDocument()
    with doc.tag("html"):
        with doc.tag("head"):
            with doc.tag("title"):
                doc.text("Simple Page")
            with doc.tag("meta", charset="utf-8"):
                pass
        with doc.tag("body"):
            with doc.tag("header"):
                with doc.tag("h1"):
                    doc.text("Welcome")
            with doc.tag("main"):
                with doc.tag("p"):
                    doc.text("This is a simple page.")
                with doc.tag("p"):
                    doc.text("It includes multiple paragraphs.")
            with doc.tag("footer"):
                with doc.tag("p"):
                    doc.text("© 2024 Test")
    return doc.render()


def generate_data_table_python():
    """Generate data table using Python implementation."""
    doc = PythonDocument()
    data = [["Name", "Age", "City"]] + [
        [f"Person {i}", str(20 + i), f"City {i}"] 
        for i in range(50)
    ]
    
    with doc.tag("html"):
        with doc.tag("body"):
            with doc.tag("table"):
                for row in data:
                    with doc.tag("tr"):
                        for cell in row:
                            with doc.tag("td"):
                                doc.text(cell)
    return doc.render()


def generate_data_table_rust():
    """Generate data table using Rust implementation."""
    doc = RustDocument()
    data = [["Name", "Age", "City"]] + [
        [f"Person {i}", str(20 + i), f"City {i}"] 
        for i in range(50)
    ]
    
    with doc.tag("html"):
        with doc.tag("body"):
            with doc.tag("table"):
                for row in data:
                    with doc.tag("tr"):
                        for cell in row:
                            with doc.tag("td"):
                                doc.text(cell)
    return doc.render()


def main():
    print("Tagflow Rust+PyO3 Performance Benchmark")
    print("=" * 40)
    
    iterations = 1000
    print(f"Running {iterations} iterations per test")
    print()
    
    # Test simple page generation
    print("=== Simple Page Generation ===")
    
    rust_time = benchmark_function(generate_simple_page_rust, iterations)
    print(f"Rust implementation: {rust_time:.4f}s ({rust_time * 1000 / iterations:.3f}ms per iteration)")
    
    if PYTHON_AVAILABLE:
        python_time = benchmark_function(generate_simple_page_python, iterations)
        print(f"Python implementation: {python_time:.4f}s ({python_time * 1000 / iterations:.3f}ms per iteration)")
        
        if python_time > 0:
            speedup = python_time / rust_time
            print(f"Speedup: {speedup:.2f}x")
    
    print()
    
    # Test data table generation
    print("=== Data Table Generation ===")
    
    rust_time = benchmark_function(generate_data_table_rust, iterations)
    print(f"Rust implementation: {rust_time:.4f}s ({rust_time * 1000 / iterations:.3f}ms per iteration)")
    
    if PYTHON_AVAILABLE:
        python_time = benchmark_function(generate_data_table_python, iterations)
        print(f"Python implementation: {python_time:.4f}s ({python_time * 1000 / iterations:.3f}ms per iteration)")
        
        if python_time > 0:
            speedup = python_time / rust_time
            print(f"Speedup: {speedup:.2f}x")
    
    print()
    
    # Verify that outputs are equivalent
    print("=== Output Verification ===")
    rust_output = generate_simple_page_rust()
    print(f"Rust output length: {len(rust_output)} characters")
    
    if PYTHON_AVAILABLE:
        python_output = generate_simple_page_python()
        print(f"Python output length: {len(python_output)} characters")
        
        # Basic verification (structure should be similar)
        if len(rust_output) > 0 and len(python_output) > 0:
            print("✓ Both implementations generate non-empty output")
            if "Welcome" in rust_output and "Welcome" in python_output:
                print("✓ Both outputs contain expected content")
    
    print("\nBenchmark complete!")


if __name__ == "__main__":
    main()