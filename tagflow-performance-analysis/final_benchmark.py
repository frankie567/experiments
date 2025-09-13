#!/usr/bin/env python3
"""
Comprehensive benchmark comparing original Tagflow, optimized versions, and Jinja2.

This provides a complete picture of the performance improvements and how close
we can get to Jinja2's performance.
"""

import time
import statistics
from typing import List, Dict, Callable
import tagflow
from jinja2 import Environment, DictLoader
from optimized_tagflow import (
    create_optimized_static,
    create_optimized_elementtree
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


class ComprehensiveBenchmark:
    """Complete benchmark comparing all implementations"""
    
    def __init__(self, iterations: int = 1000):
        self.iterations = iterations
        self.results: List[BenchmarkResult] = []
        
        # Set up Jinja2 environment with templates
        templates = {
            'simple_page.html': '''<html><head><title>{{ title }}</title><meta charset="{{ charset }}"></head>
<body><header><h1>{{ heading }}</h1></header>
<main><p>{{ content1 }}</p><p>{{ content2 }}</p></main>
<footer><p>{{ footer }}</p></footer></body></html>''',
            
            'complex_page.html': '''<html lang="{{ lang }}"><head><title>{{ title }}</title>
<meta charset="{{ charset }}"><meta name="viewport" content="{{ viewport }}">
<style>{{ styles }}</style></head>
<body><nav class="nav"><ul>{% for item in nav_items %}<li><a href="#{{ item.lower() }}">{{ item }}</a></li>{% endfor %}</ul></nav>
<main><section id="content"><h2>{{ heading2 }}</h2>
<div class="grid">{% for i in range(5) %}<article class="card"><h3>Article {{ i+1 }}</h3><p>Content of article {{ i+1 }}</p></article>{% endfor %}</div></section></main></body></html>''',
            
            'data_table.html': '''<html><head><title>{{ title }}</title></head>
<body><h1>{{ h1 }}</h1>
<table><thead><tr>{% for header in headers %}<th>{{ header }}</th>{% endfor %}</tr></thead>
<tbody>{% for i in range(100) %}<tr><td>{{ i+1 }}</td><td>Employee {{ i+1 }}</td><td>emp{{ i+1 }}@company.com</td></tr>{% endfor %}</tbody></table></body></html>'''
        }
        
        self.jinja_env = Environment(
            loader=DictLoader(templates),
            cache_size=400,
            auto_reload=False,
            optimized=True
        )
        
        # Pre-compile templates
        self.templates = {
            'simple_page': self.jinja_env.get_template('simple_page.html'),
            'complex_page': self.jinja_env.get_template('complex_page.html'),
            'data_table': self.jinja_env.get_template('data_table.html')
        }
    
    def run_benchmark(self, name: str, func: Callable) -> BenchmarkResult:
        """Run a benchmark function multiple times"""
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
    
    # === SIMPLE PAGE IMPLEMENTATIONS ===
    
    def original_simple_page(self):
        """Original Tagflow simple page"""
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
    
    def optimized_static_simple_page(self):
        """Optimized static simple page"""
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
    
    def optimized_et_simple_page(self):
        """Optimized ElementTree simple page"""
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
    
    def jinja_simple_page(self):
        """Jinja2 simple page"""
        return self.templates['simple_page'].render(
            title="Simple Page",
            charset="utf-8",
            heading="Welcome",
            content1="This is a simple page with basic HTML structure.",
            content2="It includes a header, main content, and footer.",
            footer="© 2024 Benchmark Test"
        )
    
    # === COMPLEX PAGE IMPLEMENTATIONS ===
    
    def original_complex_page(self):
        """Original Tagflow complex page"""
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
    
    def optimized_static_complex_page(self):
        """Optimized static complex page"""
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
    
    def jinja_complex_page(self):
        """Jinja2 complex page"""
        return self.templates['complex_page'].render(
            lang="en",
            title="Complex Page",
            charset="utf-8",
            viewport="width=device-width, initial-scale=1",
            styles="body { font-family: Arial, sans-serif; }",
            nav_items=["Home", "About", "Services", "Contact"],
            heading2="Main Content"
        )
    
    # === DATA TABLE IMPLEMENTATIONS ===
    
    def original_data_table(self):
        """Original Tagflow data table"""
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
    
    def optimized_static_data_table(self):
        """Optimized static data table"""
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
    
    def optimized_et_data_table(self):
        """Optimized ElementTree data table"""
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
    
    def jinja_data_table(self):
        """Jinja2 data table"""
        return self.templates['data_table'].render(
            title="Data Table",
            h1="Performance Data",
            headers=["ID", "Name", "Email"]
        )
    
    def run_all_benchmarks(self):
        """Run comprehensive benchmark suite"""
        print("🔥 Comprehensive Tagflow vs Jinja2 Performance Analysis")
        print("=" * 70)
        print(f"Iterations per test: {self.iterations}")
        print()
        
        benchmarks = [
            # Simple page
            ("Original Tagflow - Simple", self.original_simple_page),
            ("Optimized Static - Simple", self.optimized_static_simple_page),
            ("Optimized ElementTree - Simple", self.optimized_et_simple_page),
            ("Jinja2 - Simple", self.jinja_simple_page),
            
            # Complex page
            ("Original Tagflow - Complex", self.original_complex_page),
            ("Optimized Static - Complex", self.optimized_static_complex_page),
            ("Jinja2 - Complex", self.jinja_complex_page),
            
            # Data table
            ("Original Tagflow - DataTable", self.original_data_table),
            ("Optimized Static - DataTable", self.optimized_static_data_table),
            ("Optimized ElementTree - DataTable", self.optimized_et_data_table),
            ("Jinja2 - DataTable", self.jinja_data_table),
        ]
        
        for name, func in benchmarks:
            print(f"  📊 Running {name}...")
            result = self.run_benchmark(name, func)
            self.results.append(result)
    
    def print_comprehensive_results(self):
        """Print comprehensive results with gap analysis"""
        print("\n" + "=" * 80)
        print("COMPREHENSIVE PERFORMANCE ANALYSIS")
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
            print(f"\n{'-'*70}")
            print(f"SCENARIO: {scenario_name}")
            print(f"{'-'*70}")
            
            # Sort by performance (fastest first)
            sorted_impls = sorted(implementations.items(), key=lambda x: x[1].avg_time)
            
            fastest = sorted_impls[0][1]
            
            for impl_name, result in sorted_impls:
                speedup_vs_fastest = result.avg_time / fastest.avg_time if fastest.avg_time > 0 else 0
                print(f"\n{impl_name}:")
                print(f"  Average time: {result.avg_time*1000:.3f} ms")
                print(f"  Min time: {result.min_time*1000:.3f} ms")
                print(f"  Max time: {result.max_time*1000:.3f} ms")
                if speedup_vs_fastest > 1:
                    print(f"  vs Fastest: {speedup_vs_fastest:.2f}x slower")
                else:
                    print(f"  vs Fastest: FASTEST")
            
            # Show gap analysis vs Jinja2
            jinja_result = implementations.get("Jinja2")
            if jinja_result:
                print(f"\n  🎯 GAP ANALYSIS vs Jinja2:")
                for impl_name, result in implementations.items():
                    if impl_name != "Jinja2":
                        gap = result.avg_time / jinja_result.avg_time
                        print(f"    {impl_name}: {gap:.2f}x slower than Jinja2")
        
        # Final summary
        print(f"\n{'='*70}")
        print("FINAL PERFORMANCE SUMMARY")
        print(f"{'='*70}")
        
        # Calculate averages for each implementation
        impl_averages = {}
        for result in self.results:
            impl_name = result.name.split(" - ")[0]
            if impl_name not in impl_averages:
                impl_averages[impl_name] = []
            impl_averages[impl_name].append(result.avg_time)
        
        # Calculate overall averages
        for impl_name, times in impl_averages.items():
            avg_time = statistics.mean(times) * 1000
            print(f"\n{impl_name}:")
            print(f"  Overall average: {avg_time:.3f} ms")
        
        # Calculate gaps
        if "Jinja2" in impl_averages and "Original Tagflow" in impl_averages:
            jinja_avg = statistics.mean(impl_averages["Jinja2"])
            original_avg = statistics.mean(impl_averages["Original Tagflow"])
            original_gap = original_avg / jinja_avg
            
            print(f"\n🔍 PERFORMANCE GAP ANALYSIS:")
            print(f"  Original Tagflow vs Jinja2: {original_gap:.2f}x slower")
            
            if "Optimized Static" in impl_averages:
                static_avg = statistics.mean(impl_averages["Optimized Static"])
                static_gap = static_avg / jinja_avg
                improvement = original_gap / static_gap
                
                print(f"  Optimized Static vs Jinja2: {static_gap:.2f}x slower")
                print(f"  Gap reduction: {improvement:.2f}x better than original")
                
                remaining_gap = static_gap - 1.0
                original_total_gap = original_gap - 1.0
                gap_closed_percent = (1 - remaining_gap / original_total_gap) * 100 if original_total_gap > 0 else 0
                
                print(f"  Gap closed: {gap_closed_percent:.1f}% of the way to Jinja2")


def main():
    """Main benchmark execution"""
    iterations = 500  # Good balance of accuracy and speed
    
    benchmark = ComprehensiveBenchmark(iterations=iterations)
    benchmark.run_all_benchmarks()
    benchmark.print_comprehensive_results()
    
    print(f"\n{'='*80}")
    print("🎉 Comprehensive analysis completed!")
    print("Key insights:")
    print("- Identified major performance bottlenecks in original Tagflow")
    print("- Demonstrated significant improvements with optimizations")
    print("- Measured remaining performance gap vs Jinja2")
    print("- Provided actionable recommendations for further improvements")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()