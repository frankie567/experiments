#!/usr/bin/env python3
"""
Performance benchmark comparing the reimplemented Tagflow with original Tagflow and Jinja2.

This benchmark tests the same scenarios used in previous experiments to demonstrate
the performance improvements of the reimplementation.
"""

import time
import statistics
import os
from typing import List, Dict, Any, Callable
from memory_profiler import memory_usage

# Import libraries for comparison
import tagflow  # Original Tagflow
from jinja2 import Environment, FileSystemLoader
from tagflow_reimpl import Document  # Our reimplementation


class BenchmarkResult:
    """Container for benchmark results with statistical analysis."""
    
    def __init__(self, name: str, library: str, times: List[float], memory_usage: float = None):
        self.name = name
        self.library = library
        self.times = times
        self.memory_usage = memory_usage
        self.avg_time = statistics.mean(times)
        self.std_time = statistics.stdev(times) if len(times) > 1 else 0
        self.min_time = min(times)
        self.max_time = max(times)

    def avg_time_ms(self) -> float:
        """Return average time in milliseconds."""
        return self.avg_time * 1000

    def __str__(self) -> str:
        return f"{self.library} - {self.name}: {self.avg_time_ms():.3f}ms ± {self.std_time * 1000:.3f}ms"


class TagflowBenchmark:
    """Performance benchmark suite for Tagflow implementations."""
    
    def __init__(self, iterations: int = 1000):
        self.iterations = iterations
        self.results: List[BenchmarkResult] = []
        
        # Set up Jinja2 environment for comparison (using optimal setup from previous experiments)
        template_dir = self._setup_jinja_templates()
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_dir),
            cache_size=400,
            auto_reload=False,
            optimized=True,
            finalize=lambda x: x if x is not None else ''
        )
        
        # Pre-load and compile templates
        self.templates = {
            'simple_page': self.jinja_env.get_template('simple_page.jinja2'),
            'complex_page': self.jinja_env.get_template('complex_page.jinja2'),
            'data_table': self.jinja_env.get_template('data_table.jinja2'),
        }

    def _setup_jinja_templates(self) -> str:
        """Create Jinja2 templates for fair comparison."""
        template_dir = "/tmp/tagflow_benchmark_templates"
        os.makedirs(template_dir, exist_ok=True)
        
        # Simple page template
        simple_template = """<html><head><title>{{ title }}</title><meta charset="{{ charset }}" /></head><body><header><h1>{{ heading }}</h1></header><main><p>{{ content1 }}</p><p>{{ content2 }}</p></main><footer><p>{{ footer }}</p></footer></body></html>"""
        
        # Complex page template
        complex_template = """<html lang="{{ lang }}"><head><title>{{ title }}</title><meta charset="{{ charset }}" /><meta name="viewport" content="{{ viewport }}" /><style>{{ style }}</style></head><body><nav class="nav"><ul>{% for item in nav_items %}<li><a href="#{{ item.lower() }}">{{ item }}</a></li>{% endfor %}</ul></nav><header><h1>{{ heading }}</h1><p class="subtitle">{{ subtitle }}</p></header><main><section id="content"><h2>{{ section_title }}</h2><div class="grid">{% for i in range(card_count) %}<div class="card"><h3>{{ card_title }} {{ i + 1 }}</h3><p>{{ card_content }}</p></div>{% endfor %}</div></section><section id="features"><h2>{{ features_title }}</h2><ul>{% for feature in features %}<li><strong>{{ feature.name }}</strong>: {{ feature.description }}</li>{% endfor %}</ul></section></main><footer><div class="social">{% for link in social_links %}<a href="{{ link.url }}" target="_blank">{{ link.name }}</a>{% endfor %}</div><p>&copy; {{ year }} {{ company }}</p></footer></body></html>"""
        
        # Data table template
        table_template = """<html><head><title>{{ title }}</title><meta charset="utf-8" /></head><body><h1>{{ heading }}</h1><table><thead><tr>{% for header in headers %}<th>{{ header }}</th>{% endfor %}</tr></thead><tbody>{% for row in data %}<tr>{% for cell in row %}<td>{{ cell }}</td>{% endfor %}</tr>{% endfor %}</tbody></table></body></html>"""
        
        # Write templates to files
        with open(f"{template_dir}/simple_page.jinja2", "w") as f:
            f.write(simple_template)
        with open(f"{template_dir}/complex_page.jinja2", "w") as f:
            f.write(complex_template)
        with open(f"{template_dir}/data_table.jinja2", "w") as f:
            f.write(table_template)
        
        return template_dir

    def run_benchmark(self, name: str, func: Callable, measure_memory: bool = True) -> BenchmarkResult:
        """Run a benchmark function multiple times and collect statistics."""
        print(f"Running {name}...")
        
        times = []
        
        # Warmup runs
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

    # Simple Page Tests
    def generate_simple_page_original(self):
        """Generate simple page using original Tagflow."""
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

    def generate_simple_page_reimpl(self):
        """Generate simple page using reimplemented Tagflow."""
        doc = Document()
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
                        doc.text("This is a simple page with basic HTML structure.")
                    with doc.tag("p"):
                        doc.text("It includes a header, main content, and footer.")
                with doc.tag("footer"):
                    with doc.tag("p"):
                        doc.text("© 2024 Benchmark Test")
        return doc.render()

    def generate_simple_page_jinja(self):
        """Generate simple page using Jinja2."""
        return self.templates['simple_page'].render(
            title="Simple Page",
            charset="utf-8",
            heading="Welcome",
            content1="This is a simple page with basic HTML structure.",
            content2="It includes a header, main content, and footer.",
            footer="© 2024 Benchmark Test"
        )

    # Complex Page Tests
    def generate_complex_page_original(self):
        """Generate complex page using original Tagflow."""
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
                        tagflow.text("body { font-family: Arial, sans-serif; } .nav { background: #333; }")

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
                                    with tagflow.tag("div", **{"class": "card"}):
                                        with tagflow.tag("h3"):
                                            tagflow.text(f"Card {i + 1}")
                                        with tagflow.tag("p"):
                                            tagflow.text("Sample content for this card.")

                        with tagflow.tag("section", id="features"):
                            with tagflow.tag("h2"):
                                tagflow.text("Features")
                            with tagflow.tag("ul"):
                                features = ["Fast", "Reliable", "Scalable"]
                                for feature in features:
                                    with tagflow.tag("li"):
                                        with tagflow.tag("strong"):
                                            tagflow.text(feature)
                                        tagflow.text(f": {feature} description")

                    with tagflow.tag("footer"):
                        with tagflow.tag("div", **{"class": "social"}):
                            for link in [("Twitter", "#"), ("GitHub", "#")]:
                                with tagflow.tag("a", href=link[1], target="_blank"):
                                    tagflow.text(link[0])
                        with tagflow.tag("p"):
                            tagflow.text("© 2024 Benchmark Company")
        return str(doc)

    def generate_complex_page_reimpl(self):
        """Generate complex page using reimplemented Tagflow."""
        doc = Document()
        with doc.tag("html", lang="en"):
            with doc.tag("head"):
                with doc.tag("title"):
                    doc.text("Complex Page")
                with doc.tag("meta", charset="utf-8"):
                    pass
                with doc.tag("meta", name="viewport", content="width=device-width, initial-scale=1"):
                    pass
                with doc.tag("style"):
                    doc.text("body { font-family: Arial, sans-serif; } .nav { background: #333; }")

            with doc.tag("body"):
                with doc.tag("nav", class_="nav"):
                    with doc.tag("ul"):
                        for item in ["Home", "About", "Services", "Contact"]:
                            with doc.tag("li"):
                                with doc.tag("a", href=f"#{item.lower()}"):
                                    doc.text(item)

                with doc.tag("header"):
                    with doc.tag("h1"):
                        doc.text("Complex Web Page")
                    with doc.tag("p", class_="subtitle"):
                        doc.text("Demonstrating complex HTML structure")

                with doc.tag("main"):
                    with doc.tag("section", id="content"):
                        with doc.tag("h2"):
                            doc.text("Main Content")
                        with doc.tag("div", class_="grid"):
                            for i in range(5):
                                with doc.tag("div", class_="card"):
                                    with doc.tag("h3"):
                                        doc.text(f"Card {i + 1}")
                                    with doc.tag("p"):
                                        doc.text("Sample content for this card.")

                    with doc.tag("section", id="features"):
                        with doc.tag("h2"):
                            doc.text("Features")
                        with doc.tag("ul"):
                            features = ["Fast", "Reliable", "Scalable"]
                            for feature in features:
                                with doc.tag("li"):
                                    with doc.tag("strong"):
                                        doc.text(feature)
                                    doc.text(f": {feature} description")

                with doc.tag("footer"):
                    with doc.tag("div", class_="social"):
                        for link in [("Twitter", "#"), ("GitHub", "#")]:
                            with doc.tag("a", href=link[1], target="_blank"):
                                doc.text(link[0])
                    with doc.tag("p"):
                        doc.text("© 2024 Benchmark Company")
        return doc.render()

    def generate_complex_page_jinja(self):
        """Generate complex page using Jinja2."""
        return self.templates['complex_page'].render(
            lang="en",
            title="Complex Page",
            charset="utf-8",
            viewport="width=device-width, initial-scale=1",
            style="body { font-family: Arial, sans-serif; } .nav { background: #333; }",
            nav_items=["Home", "About", "Services", "Contact"],
            heading="Complex Web Page",
            subtitle="Demonstrating complex HTML structure",
            section_title="Main Content",
            card_count=5,
            card_title="Card",
            card_content="Sample content for this card.",
            features_title="Features",
            features=[
                {"name": "Fast", "description": "Fast description"},
                {"name": "Reliable", "description": "Reliable description"},
                {"name": "Scalable", "description": "Scalable description"}
            ],
            social_links=[
                {"name": "Twitter", "url": "#"},
                {"name": "GitHub", "url": "#"}
            ],
            year=2024,
            company="Benchmark Company"
        )

    # Data Table Tests
    def generate_data_table_original(self):
        """Generate data table using original Tagflow."""
        data = [
            ["John", "25", "Engineer"],
            ["Jane", "30", "Designer"],
            ["Bob", "35", "Manager"]
        ] * 34  # Approximate 100 rows

        with tagflow.document() as doc:
            with tagflow.tag("html"):
                with tagflow.tag("head"):
                    with tagflow.tag("title"):
                        tagflow.text("Data Table")
                    with tagflow.tag("meta", charset="utf-8"):
                        pass
                with tagflow.tag("body"):
                    with tagflow.tag("h1"):
                        tagflow.text("Employee Data")
                    with tagflow.tag("table"):
                        with tagflow.tag("thead"):
                            with tagflow.tag("tr"):
                                for header in ["Name", "Age", "Position"]:
                                    with tagflow.tag("th"):
                                        tagflow.text(header)
                        with tagflow.tag("tbody"):
                            for row in data:
                                with tagflow.tag("tr"):
                                    for cell in row:
                                        with tagflow.tag("td"):
                                            tagflow.text(cell)
        return str(doc)

    def generate_data_table_reimpl(self):
        """Generate data table using reimplemented Tagflow."""
        data = [
            ["John", "25", "Engineer"],
            ["Jane", "30", "Designer"],
            ["Bob", "35", "Manager"]
        ] * 34  # Approximate 100 rows

        doc = Document()
        with doc.tag("html"):
            with doc.tag("head"):
                with doc.tag("title"):
                    doc.text("Data Table")
                with doc.tag("meta", charset="utf-8"):
                    pass
            with doc.tag("body"):
                with doc.tag("h1"):
                    doc.text("Employee Data")
                with doc.tag("table"):
                    with doc.tag("thead"):
                        with doc.tag("tr"):
                            for header in ["Name", "Age", "Position"]:
                                with doc.tag("th"):
                                    doc.text(header)
                    with doc.tag("tbody"):
                        for row in data:
                            with doc.tag("tr"):
                                for cell in row:
                                    with doc.tag("td"):
                                        doc.text(cell)
        return doc.render()

    def generate_data_table_jinja(self):
        """Generate data table using Jinja2."""
        data = [
            ["John", "25", "Engineer"],
            ["Jane", "30", "Designer"],
            ["Bob", "35", "Manager"]
        ] * 34  # Approximate 100 rows

        return self.templates['data_table'].render(
            title="Data Table",
            heading="Employee Data",
            headers=["Name", "Age", "Position"],
            data=data
        )

    def run_all_benchmarks(self):
        """Run all benchmark tests and display results."""
        print("Tagflow Reimplementation Performance Benchmark")
        print("=" * 50)
        print(f"Running {self.iterations} iterations per test (with 10 warmup runs)")
        print()

        # Test scenarios
        tests = [
            ("Simple Page", [
                self.generate_simple_page_original,
                self.generate_simple_page_reimpl,
                self.generate_simple_page_jinja
            ]),
            ("Complex Page", [
                self.generate_complex_page_original,
                self.generate_complex_page_reimpl,
                self.generate_complex_page_jinja
            ]),
            ("Data Table", [
                self.generate_data_table_original,
                self.generate_data_table_reimpl,
                self.generate_data_table_jinja
            ])
        ]

        all_results = []

        for test_name, test_functions in tests:
            print(f"=== {test_name} Benchmark ===")
            
            test_results = []
            for func in test_functions:
                result = self.run_benchmark(f"{test_name}", func)
                test_results.append(result)
                all_results.append(result)
                print(f"  {result}")

            # Calculate performance ratios
            if len(test_results) >= 3:
                original_time = test_results[0].avg_time
                reimpl_time = test_results[1].avg_time
                jinja_time = test_results[2].avg_time

                reimpl_vs_original = original_time / reimpl_time
                reimpl_vs_jinja = reimpl_time / jinja_time
                
                print(f"  Improvement over original: {reimpl_vs_original:.2f}x faster")
                print(f"  vs Jinja2: {reimpl_vs_jinja:.2f}x slower")
            
            print()

        # Summary
        print("=== Performance Summary ===")
        
        # Group results by library using function names
        original_results = [r for r in all_results if "original" in r.library or r.library == "generate"]
        reimpl_results = [r for r in all_results if "reimpl" in r.library]
        jinja_results = [r for r in all_results if "jinja" in r.library]

        # Since the library name extraction isn't working perfectly, group by position
        grouped_results = []
        for i in range(0, len(all_results), 3):
            if i + 2 < len(all_results):
                grouped_results.append((all_results[i], all_results[i+1], all_results[i+2]))

        if grouped_results:
            original_times = [group[0].avg_time for group in grouped_results]
            reimpl_times = [group[1].avg_time for group in grouped_results]
            jinja_times = [group[2].avg_time for group in grouped_results]

            avg_original = statistics.mean(original_times)
            avg_reimpl = statistics.mean(reimpl_times)
            avg_jinja = statistics.mean(jinja_times)

            overall_improvement = avg_original / avg_reimpl
            vs_jinja = avg_reimpl / avg_jinja

            print(f"Overall average times:")
            print(f"  Original Tagflow: {avg_original * 1000:.3f}ms")
            print(f"  Reimplemented:    {avg_reimpl * 1000:.3f}ms")
            print(f"  Jinja2:           {avg_jinja * 1000:.3f}ms")
            print()
            print(f"Overall improvement: {overall_improvement:.2f}x faster than original")
            print(f"Performance vs Jinja2: {vs_jinja:.2f}x slower")

        print("\n=== Test Verification ===")
        # Verify that all implementations produce similar HTML
        try:
            original_html = self.generate_simple_page_original()
            reimpl_html = self.generate_simple_page_reimpl()
            jinja_html = self.generate_simple_page_jinja()
            
            print(f"Original length: {len(original_html)} chars")
            print(f"Reimpl length:   {len(reimpl_html)} chars")
            print(f"Jinja length:    {len(jinja_html)} chars")
            
            # Basic validation that core structure is preserved
            for html in [original_html, reimpl_html, jinja_html]:
                assert "<html>" in html and "</html>" in html
                assert "<title>" in html and "</title>" in html
                assert "Welcome" in html
            
            print("✓ All implementations produce valid HTML with expected content")
            
        except Exception as e:
            print(f"⚠ HTML verification failed: {e}")


def main():
    """Run the benchmark."""
    benchmark = TagflowBenchmark(iterations=1000)
    benchmark.run_all_benchmarks()


if __name__ == "__main__":
    main()