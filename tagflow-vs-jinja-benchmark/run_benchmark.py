#!/usr/bin/env python3
"""
Script to run benchmark and save results to file
"""

import sys
from datetime import datetime
from benchmark import HTMLBenchmark
import platform

def main():
    """Run benchmark and save results"""
    print("Tagflow vs Jinja2 Performance Benchmark")
    print("=" * 50)
    
    # System info
    print(f"Python version: {platform.python_version()}")
    print(f"Platform: {platform.platform()}")
    print(f"Processor: {platform.processor()}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    # Run benchmark
    iterations = 1000
    benchmark = HTMLBenchmark(iterations=iterations)
    benchmark.run_all_benchmarks()
    
    # Print to console
    benchmark.print_results()
    
    # Save to file
    results_file = f"benchmark_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(results_file, 'w') as f:
        f.write("Tagflow vs Jinja2 Performance Benchmark Results\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"System Information:\n")
        f.write(f"  Python version: {platform.python_version()}\n")
        f.write(f"  Platform: {platform.platform()}\n")
        f.write(f"  Processor: {platform.processor()}\n")
        f.write(f"  Timestamp: {datetime.now().isoformat()}\n")
        f.write(f"  Iterations per test: {iterations}\n")
        f.write(f"  Warmup runs: 10\n\n")
        
        # Redirect print output to file
        original_stdout = sys.stdout
        sys.stdout = f
        benchmark.print_results()
        sys.stdout = original_stdout
    
    print(f"\nResults saved to: {results_file}")

if __name__ == "__main__":
    main()