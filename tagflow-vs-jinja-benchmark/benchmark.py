#!/usr/bin/env python3
"""
Performance benchmark comparing tagflow vs Jinja2 for HTML generation.

This script tests various scenarios and provides statistical analysis of the results.
"""

import time
import statistics
from typing import List, Dict, Any, Callable
from memory_profiler import memory_usage
import tagflow
from jinja2 import Environment, FileSystemLoader
import os


class BenchmarkResult:
    """Container for benchmark results"""
    
    def __init__(self, name: str, library: str, times: List[float], memory_usage: float = None):
        self.name = name
        self.library = library
        self.times = times
        self.memory_usage = memory_usage
        self.avg_time = statistics.mean(times)
        self.std_time = statistics.stdev(times) if len(times) > 1 else 0
        self.min_time = min(times)
        self.max_time = max(times)


class HTMLBenchmark:
    """HTML generation benchmark suite"""
    
    def __init__(self, iterations: int = 1000):
        self.iterations = iterations
        self.results: List[BenchmarkResult] = []
        
        # Set up Jinja Environment with proper optimizations
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_dir),
            # Enable template caching and optimizations
            cache_size=400,  # Cache up to 400 templates
            auto_reload=False,  # Disable auto-reloading for performance
            optimized=True,  # Enable optimizations
            finalize=lambda x: x if x is not None else ''  # Handle None values
        )
        
        # Pre-load and compile templates for fair comparison
        self.templates = {
            'simple_page': self.jinja_env.get_template('simple_page.jinja2'),
            'complex_page': self.jinja_env.get_template('complex_page.jinja2'),
            'data_table': self.jinja_env.get_template('data_table.jinja2'),
        }
    
    def run_benchmark(self, name: str, func: Callable, measure_memory: bool = True) -> BenchmarkResult:
        """Run a benchmark function multiple times and collect statistics"""
        print(f"Running {name}...")
        
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
        
        # Memory usage test (single run)
        mem_usage = None
        if measure_memory:
            try:
                mem_usage = max(memory_usage((func, (), {}), interval=0.01))
            except Exception:
                pass
        
        return BenchmarkResult(name, func.__name__.split('_')[0], times, mem_usage)
    
    def generate_simple_page_tagflow(self):
        """Generate a simple HTML page using tagflow"""
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
    
    def generate_simple_page_jinja(self):
        """Generate a simple HTML page using Jinja2 with proper environment"""
        return self.templates['simple_page'].render(
            title="Simple Page",
            charset="utf-8",
            heading="Welcome",
            content1="This is a simple page with basic HTML structure.",
            content2="It includes a header, main content, and footer.",
            footer="© 2024 Benchmark Test"
        )
    
    def generate_complex_page_tagflow(self):
        """Generate a complex HTML page using tagflow"""
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
                        tagflow.text("body { font-family: Arial, sans-serif; } .nav { background: #333; } .nav a { color: white; }")
                
                with tagflow.tag("body"):
                    with tagflow.tag("nav", **{"class": "nav"}):
                        with tagflow.tag("ul"):
                            for item in ["Home", "About", "Services", "Contact"]:
                                with tagflow.tag("li"):
                                    with tagflow.tag("a", href=f"#{item.lower()}"):
                                        tagflow.text(item)
                    
                    with tagflow.tag("header"):
                        with tagflow.tag("h1"):
                            tagflow.text("Complex Web Page")
                        with tagflow.tag("p", **{"class": "subtitle"}):
                            tagflow.text("Demonstrating complex HTML structure")
                    
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
                                            tagflow.text(f"This is the content of article {i+1}. It contains some text and demonstrates nested structures.")
                                        with tagflow.tag("div", **{"class": "meta"}):
                                            with tagflow.tag("span", **{"class": "date"}):
                                                tagflow.text("2024-01-01")
                                            with tagflow.tag("span", **{"class": "author"}):
                                                tagflow.text(f"Author {i+1}")
                        
                        with tagflow.tag("aside"):
                            with tagflow.tag("h3"):
                                tagflow.text("Sidebar")
                            with tagflow.tag("ul"):
                                for item in ["Link 1", "Link 2", "Link 3"]:
                                    with tagflow.tag("li"):
                                        with tagflow.tag("a", href="#"):
                                            tagflow.text(item)
                    
                    with tagflow.tag("footer"):
                        with tagflow.tag("p"):
                            tagflow.text("© 2024 Complex Page Benchmark")
        return str(doc)
    
    def generate_complex_page_jinja(self):
        """Generate a complex HTML page using Jinja2 with proper environment"""
        return self.templates['complex_page'].render(
            title="Complex Page",
            styles="body { font-family: Arial, sans-serif; } .nav { background: #333; } .nav a { color: white; }",
            nav_items=["Home", "About", "Services", "Contact"],
            heading="Complex Web Page",
            subtitle="Demonstrating complex HTML structure",
            articles=[
                {
                    "title": f"Article {i+1}",
                    "content": f"This is the content of article {i+1}. It contains some text and demonstrates nested structures.",
                    "date": "2024-01-01",
                    "author": f"Author {i+1}"
                } for i in range(5)
            ],
            sidebar_links=["Link 1", "Link 2", "Link 3"],
            footer="© 2024 Complex Page Benchmark"
        )
    
    def generate_table_tagflow(self):
        """Generate a table with many rows using tagflow"""
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
                                for header in ["ID", "Name", "Email", "Department", "Salary"]:
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
                                    with tagflow.tag("td"):
                                        tagflow.text(f"Dept {(i % 5) + 1}")
                                    with tagflow.tag("td"):
                                        tagflow.text(f"${50000 + (i * 1000):,}")
        return str(doc)
    
    def generate_table_jinja(self):
        """Generate a table with many rows using Jinja2 with proper environment"""
        data = []
        for i in range(100):
            data.append({
                "id": i + 1,
                "name": f"Employee {i + 1}",
                "email": f"emp{i + 1}@company.com",
                "department": f"Dept {(i % 5) + 1}",
                "salary": f"${50000 + (i * 1000):,}"
            })
        
        return self.templates['data_table'].render(
            headers=["ID", "Name", "Email", "Department", "Salary"],
            data=data
        )
    
    def run_all_benchmarks(self):
        """Run all benchmark scenarios"""
        scenarios = [
            ("Simple Page (Tagflow)", self.generate_simple_page_tagflow),
            ("Simple Page (Jinja Environment)", self.generate_simple_page_jinja),
            ("Complex Page (Tagflow)", self.generate_complex_page_tagflow),
            ("Complex Page (Jinja Environment)", self.generate_complex_page_jinja),
            ("Data Table (Tagflow)", self.generate_table_tagflow),
            ("Data Table (Jinja Environment)", self.generate_table_jinja),
        ]
        
        for name, func in scenarios:
            result = self.run_benchmark(name, func)
            self.results.append(result)
    
    def print_results(self):
        """Print benchmark results in a readable format"""
        print("\n" + "="*80)
        print("BENCHMARK RESULTS")
        print("="*80)
        
        print(f"\nIterations per test: {self.iterations}")
        print(f"Warmup runs: 10")
        
        # Group results by scenario
        scenarios = {}
        for result in self.results:
            scenario = result.name.split(' (')[0]
            if scenario not in scenarios:
                scenarios[scenario] = {}
            library = result.name.split(' (')[1].rstrip(')')
            scenarios[scenario][library] = result
        
        for scenario_name, libraries in scenarios.items():
            print(f"\n{'-'*60}")
            print(f"SCENARIO: {scenario_name}")
            print(f"{'-'*60}")
            
            # Print detailed stats for each library
            for lib_name, result in libraries.items():
                print(f"\n{lib_name}:")
                print(f"  Average time: {result.avg_time*1000:.3f} ms")
                print(f"  Std deviation: {result.std_time*1000:.3f} ms")
                print(f"  Min time: {result.min_time*1000:.3f} ms")
                print(f"  Max time: {result.max_time*1000:.3f} ms")
                if result.memory_usage:
                    print(f"  Peak memory: {result.memory_usage:.2f} MB")
            
            # Compare performance
            if len(libraries) == 2:
                lib_names = list(libraries.keys())
                result1, result2 = libraries[lib_names[0]], libraries[lib_names[1]]
                
                if result1.avg_time < result2.avg_time:
                    faster, slower = result1, result2
                    faster_name, slower_name = lib_names[0], lib_names[1]
                else:
                    faster, slower = result2, result1
                    faster_name, slower_name = lib_names[1], lib_names[0]
                
                ratio = slower.avg_time / faster.avg_time
                print(f"\n  COMPARISON:")
                print(f"  {faster_name} is {ratio:.2f}x faster than {slower_name}")
                print(f"  {faster_name}: {faster.avg_time*1000:.3f} ms avg")
                print(f"  {slower_name}: {slower.avg_time*1000:.3f} ms avg")
        
        # Overall summary
        print(f"\n{'='*60}")
        print("OVERALL SUMMARY")
        print(f"{'='*60}")
        
        tagflow_times = [r.avg_time for r in self.results if 'Tagflow' in r.name]
        jinja_times = [r.avg_time for r in self.results if 'Jinja Environment' in r.name]
        
        if tagflow_times and jinja_times:
            avg_tagflow = statistics.mean(tagflow_times)
            avg_jinja = statistics.mean(jinja_times)
            
            print(f"\nAverage across all scenarios:")
            print(f"  Tagflow: {avg_tagflow*1000:.3f} ms")
            print(f"  Jinja: {avg_jinja*1000:.3f} ms")
            
            if avg_tagflow < avg_jinja:
                ratio = avg_jinja / avg_tagflow
                print(f"  Tagflow is {ratio:.2f}x faster on average")
            else:
                ratio = avg_tagflow / avg_jinja
                print(f"  Jinja is {ratio:.2f}x faster on average")


def main():
    """Main benchmark execution"""
    print("Tagflow vs Jinja2 Performance Benchmark")
    print("="*50)
    
    # Run with fewer iterations for development, more for production
    iterations = 1000
    
    benchmark = HTMLBenchmark(iterations=iterations)
    benchmark.run_all_benchmarks()
    benchmark.print_results()
    
    print(f"\n{'='*80}")
    print("Benchmark completed successfully!")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()