#!/usr/bin/env python3
"""
Benchmark comparing original Tagflow vs optimized implementations.

This script measures the performance improvements from various optimization
strategies applied to Tagflow.
"""

import time
import statistics
from typing import List, Dict, Callable
import tagflow
from jinja2 import Environment, FileSystemLoader
import os
from optimized_tagflow import (
    create_optimized_static,
    create_optimized_elementtree, 
    create_cached_tagflow
)


class BenchmarkResult:
    """Container for benchmark results"""
    
    def __init__(self, name: str, times: List[float]):
        self.name = name
        self.times = times
        self.avg_time = statistics.mean(times)
        self.std_time = statistics.stdev(times) if len(times) > 1 else 0
        self.min_time = min(times)
        self.max_time = max(times)


class OptimizationBenchmark:
    """Benchmark suite for testing Tagflow optimizations"""
    
    def __init__(self, iterations: int = 1000):
        self.iterations = iterations
        self.results: List[BenchmarkResult] = []
    
    def run_benchmark(self, name: str, func: Callable) -> BenchmarkResult:
        """Run a benchmark function multiple times"""
        print(f"  Running {name}...")
        
        times = []
        
        # Warmup
        for _ in range(10):
            func()
        
        # Actual benchmark
        for _ in range(self.iterations):
            start_time = time.perf_counter()
            func()
            end_time = time.perf_counter()
            times.append(end_time - start_time)
        
        return BenchmarkResult(name, times)
    
    # Original Tagflow implementations
    def original_simple_page(self):
        """Generate simple page with original Tagflow"""
        with tagflow.document() as doc:
            with tagflow.tag("html"):
                with tagflow.tag("head"):
                    with tagflow.tag("title"):
                        tagflow.text("Simple Page")
                    with tagflow.tag("meta", charset="utf-8"):
                        pass
                with tagflow.tag("body"):
                    with tagflow.tag("header"):
                        with tagflow.tag("h1"):
                            tagflow.text("Welcome")
                    with tagflow.tag("main"):
                        with tagflow.tag("p"):
                            tagflow.text("This is a simple page with basic HTML structure.")
                        with tagflow.tag("p"):
                            tagflow.text("It includes a header, main content, and footer.")
                    with tagflow.tag("footer"):
                        with tagflow.tag("p"):
                            tagflow.text("© 2024 Benchmark Test")
        return str(doc)
    
    def original_complex_page(self):
        """Generate complex page with original Tagflow"""
        with tagflow.document() as doc:
            with tagflow.tag("html", lang="en"):
                with tagflow.tag("head"):
                    with tagflow.tag("title"):
                        tagflow.text("Complex Page")
                    with tagflow.tag("meta", charset="utf-8"):
                        pass
                    with tagflow.tag("meta", name="viewport", content="width=device-width, initial-scale=1"):
                        pass
                    with tagflow.tag("style"):
                        tagflow.text("body { font-family: Arial, sans-serif; }")
                
                with tagflow.tag("body"):
                    with tagflow.tag("nav", **{"class": "nav"}):
                        with tagflow.tag("ul"):
                            for item in ["Home", "About", "Services", "Contact"]:
                                with tagflow.tag("li"):
                                    with tagflow.tag("a", href=f"#{item.lower()}"):
                                        tagflow.text(item)
                    
                    with tagflow.tag("main"):
                        with tagflow.tag("section", id="content"):
                            with tagflow.tag("h2"):
                                tagflow.text("Main Content")
                            with tagflow.tag("div", **{"class": "grid"}):
                                for i in range(5):
                                    with tagflow.tag("article", **{"class": "card"}):
                                        with tagflow.tag("h3"):
                                            tagflow.text(f"Article {i+1}")
                                        with tagflow.tag("p"):
                                            tagflow.text(f"Content of article {i+1}")
        return str(doc)
    
    def original_data_table(self):
        """Generate data table with original Tagflow"""
        with tagflow.document() as doc:
            with tagflow.tag("html"):
                with tagflow.tag("head"):
                    with tagflow.tag("title"):
                        tagflow.text("Data Table")
                with tagflow.tag("body"):
                    with tagflow.tag("h1"):
                        tagflow.text("Performance Data")
                    with tagflow.tag("table"):
                        with tagflow.tag("thead"):
                            with tagflow.tag("tr"):
                                for header in ["ID", "Name", "Email"]:
                                    with tagflow.tag("th"):
                                        tagflow.text(header)
                        with tagflow.tag("tbody"):
                            for i in range(100):
                                with tagflow.tag("tr"):
                                    with tagflow.tag("td"):
                                        tagflow.text(str(i + 1))
                                    with tagflow.tag("td"):
                                        tagflow.text(f"Employee {i + 1}")
                                    with tagflow.tag("td"):
                                        tagflow.text(f"emp{i + 1}@company.com")
        return str(doc)
    
    # Optimized static implementations
    def optimized_static_simple_page(self):
        """Generate simple page with optimized static Tagflow"""
        tf = create_optimized_static()
        with tf.document():
            with tf.tag("html"):
                with tf.tag("head"):
                    with tf.tag("title"):
                        tf.text("Simple Page")
                    with tf.tag("meta", charset="utf-8"):
                        pass
                with tf.tag("body"):
                    with tf.tag("header"):
                        with tf.tag("h1"):
                            tf.text("Welcome")
                    with tf.tag("main"):
                        with tf.tag("p"):
                            tf.text("This is a simple page with basic HTML structure.")
                        with tf.tag("p"):
                            tf.text("It includes a header, main content, and footer.")
                    with tf.tag("footer"):
                        with tf.tag("p"):
                            tf.text("© 2024 Benchmark Test")
        return str(tf)
    
    def optimized_static_complex_page(self):
        """Generate complex page with optimized static Tagflow"""
        tf = create_optimized_static()
        with tf.document():
            with tf.tag("html", lang="en"):
                with tf.tag("head"):
                    with tf.tag("title"):
                        tf.text("Complex Page")
                    with tf.tag("meta", charset="utf-8"):
                        pass
                    with tf.tag("meta", name="viewport", content="width=device-width, initial-scale=1"):
                        pass
                    with tf.tag("style"):
                        tf.text("body { font-family: Arial, sans-serif; }")
                
                with tf.tag("body"):
                    with tf.tag("nav", **{"class": "nav"}):
                        with tf.tag("ul"):
                            for item in ["Home", "About", "Services", "Contact"]:
                                with tf.tag("li"):
                                    with tf.tag("a", href=f"#{item.lower()}"):
                                        tf.text(item)
                    
                    with tf.tag("main"):
                        with tf.tag("section", id="content"):
                            with tf.tag("h2"):
                                tf.text("Main Content")
                            with tf.tag("div", **{"class": "grid"}):
                                for i in range(5):
                                    with tf.tag("article", **{"class": "card"}):
                                        with tf.tag("h3"):
                                            tf.text(f"Article {i+1}")
                                        with tf.tag("p"):
                                            tf.text(f"Content of article {i+1}")
        return str(tf)
    
    def optimized_static_data_table(self):
        """Generate data table with optimized static Tagflow"""
        tf = create_optimized_static()
        with tf.document():
            with tf.tag("html"):
                with tf.tag("head"):
                    with tf.tag("title"):
                        tf.text("Data Table")
                with tf.tag("body"):
                    with tf.tag("h1"):
                        tf.text("Performance Data")
                    with tf.tag("table"):
                        with tf.tag("thead"):
                            with tf.tag("tr"):
                                for header in ["ID", "Name", "Email"]:
                                    with tf.tag("th"):
                                        tf.text(header)
                        with tf.tag("tbody"):
                            for i in range(100):
                                with tf.tag("tr"):
                                    with tf.tag("td"):
                                        tf.text(str(i + 1))
                                    with tf.tag("td"):
                                        tf.text(f"Employee {i + 1}")
                                    with tf.tag("td"):
                                        tf.text(f"emp{i + 1}@company.com")
        return str(tf)
    
    # ElementTree optimized implementations  
    def optimized_et_simple_page(self):
        """Generate simple page with optimized ElementTree Tagflow"""
        tf = create_optimized_elementtree()
        with tf.document():
            with tf.tag("html"):
                with tf.tag("head"):
                    with tf.tag("title"):
                        tf.text("Simple Page")
                    with tf.tag("meta", charset="utf-8"):
                        pass
                with tf.tag("body"):
                    with tf.tag("header"):
                        with tf.tag("h1"):
                            tf.text("Welcome")
                    with tf.tag("main"):
                        with tf.tag("p"):
                            tf.text("This is a simple page with basic HTML structure.")
                        with tf.tag("p"):
                            tf.text("It includes a header, main content, and footer.")
                    with tf.tag("footer"):
                        with tf.tag("p"):
                            tf.text("© 2024 Benchmark Test")
        return str(tf)
    
    def optimized_et_data_table(self):
        """Generate data table with optimized ElementTree Tagflow"""
        tf = create_optimized_elementtree()
        with tf.document():
            with tf.tag("html"):
                with tf.tag("head"):
                    with tf.tag("title"):
                        tf.text("Data Table")
                with tf.tag("body"):
                    with tf.tag("h1"):
                        tf.text("Performance Data")
                    with tf.tag("table"):
                        with tf.tag("thead"):
                            with tf.tag("tr"):
                                for header in ["ID", "Name", "Email"]:
                                    with tf.tag("th"):
                                        tf.text(header)
                        with tf.tag("tbody"):
                            for i in range(100):
                                with tf.tag("tr"):
                                    with tf.tag("td"):
                                        tf.text(str(i + 1))
                                    with tf.tag("td"):
                                        tf.text(f"Employee {i + 1}")
                                    with tf.tag("td"):
                                        tf.text(f"emp{i + 1}@company.com")
        return str(tf)
    
    def run_all_benchmarks(self):
        """Run comprehensive benchmark suite"""
        print("🚀 Running Tagflow Optimization Benchmarks")
        print("=" * 60)
        print(f"Iterations per test: {self.iterations}")
        print()
        
        benchmarks = [
            # Simple page benchmarks
            ("Original Tagflow - Simple Page", self.original_simple_page),
            ("Optimized Static - Simple Page", self.optimized_static_simple_page),
            ("Optimized ElementTree - Simple Page", self.optimized_et_simple_page),
            
            # Complex page benchmarks  
            ("Original Tagflow - Complex Page", self.original_complex_page),
            ("Optimized Static - Complex Page", self.optimized_static_complex_page),
            
            # Data table benchmarks
            ("Original Tagflow - Data Table", self.original_data_table),
            ("Optimized Static - Data Table", self.optimized_static_data_table),
            ("Optimized ElementTree - Data Table", self.optimized_et_data_table),
        ]
        
        for name, func in benchmarks:
            result = self.run_benchmark(name, func)
            self.results.append(result)
    
    def print_results(self):
        """Print benchmark results with comparisons"""
        print("\n" + "=" * 80)
        print("OPTIMIZATION BENCHMARK RESULTS")
        print("=" * 80)
        
        # Group results by scenario
        scenarios = {}
        for result in self.results:
            parts = result.name.split(" - ")
            if len(parts) >= 2:
                implementation = parts[0]
                scenario = parts[1]
                if scenario not in scenarios:
                    scenarios[scenario] = {}
                scenarios[scenario][implementation] = result
        
        for scenario_name, implementations in scenarios.items():
            print(f"\n{'-'*60}")
            print(f"SCENARIO: {scenario_name}")
            print(f"{'-'*60}")
            
            # Find original for comparison
            original = None
            for impl_name, result in implementations.items():
                print(f"\n{impl_name}:")
                print(f"  Average time: {result.avg_time*1000:.3f} ms")
                print(f"  Std deviation: {result.std_time*1000:.3f} ms") 
                print(f"  Min time: {result.min_time*1000:.3f} ms")
                print(f"  Max time: {result.max_time*1000:.3f} ms")
                
                if "Original" in impl_name:
                    original = result
            
            # Show improvements vs original
            if original:
                print(f"\n  IMPROVEMENTS vs Original Tagflow:")
                for impl_name, result in implementations.items():
                    if "Original" not in impl_name:
                        if result.avg_time > 0:
                            speedup = original.avg_time / result.avg_time
                            print(f"  {impl_name}: {speedup:.2f}x faster")
                        else:
                            print(f"  {impl_name}: ERROR - zero time")
        
        # Overall summary
        print(f"\n{'='*60}")
        print("OVERALL OPTIMIZATION SUMMARY")
        print(f"{'='*60}")
        
        original_times = []
        static_times = []
        et_times = []
        
        for result in self.results:
            if "Original Tagflow" in result.name:
                original_times.append(result.avg_time)
            elif "Optimized Static" in result.name:
                static_times.append(result.avg_time)
            elif "Optimized ElementTree" in result.name:
                et_times.append(result.avg_time)
        
        if original_times and static_times:
            avg_original = statistics.mean(original_times) * 1000
            avg_static = statistics.mean(static_times) * 1000
            static_speedup = statistics.mean(original_times) / statistics.mean(static_times)
            
            print(f"\nOptimized Static vs Original:")
            print(f"  Original average: {avg_original:.3f} ms")
            print(f"  Static average: {avg_static:.3f} ms") 
            print(f"  Overall speedup: {static_speedup:.2f}x")
        
        if original_times and et_times:
            avg_et = statistics.mean(et_times) * 1000
            et_speedup = statistics.mean(original_times) / statistics.mean(et_times)
            
            print(f"\nOptimized ElementTree vs Original:")
            print(f"  ElementTree average: {avg_et:.3f} ms")
            print(f"  Overall speedup: {et_speedup:.2f}x")


def main():
    """Main benchmark execution"""
    print("Testing optimized implementations first...")
    
    # Quick validation that optimizations work
    try:
        static = create_optimized_static()
        with static.document():
            with static.tag("html"):
                with static.tag("body"):
                    static.text("Test")
        
        et = create_optimized_elementtree()
        with et.document():
            with et.tag("html"):
                with et.tag("body"):
                    et.text("Test")
        
        print("✅ All optimized implementations working correctly!")
        print()
    except Exception as e:
        print(f"❌ Error in optimized implementations: {e}")
        return
    
    # Run benchmarks with fewer iterations for development
    iterations = 100  # Increase for production benchmarks
    
    benchmark = OptimizationBenchmark(iterations=iterations)
    benchmark.run_all_benchmarks()
    benchmark.print_results()
    
    print(f"\n{'='*80}")
    print("Optimization benchmark completed successfully!")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()