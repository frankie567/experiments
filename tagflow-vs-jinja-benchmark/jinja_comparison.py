#!/usr/bin/env python3
"""
Comparison script showing the performance difference between:
1. Jinja2 with inline templates (Template class)
2. Jinja2 with proper Environment and file-based templates
"""

import time
import statistics
from typing import List
from jinja2 import Template, Environment, FileSystemLoader
import os


def benchmark_function(func, iterations=100):
    """Run a function multiple times and return average time"""
    times = []
    
    # Warmup
    for _ in range(5):
        func()
    
    # Benchmark
    for _ in range(iterations):
        start = time.perf_counter()
        func()
        end = time.perf_counter()
        times.append(end - start)
    
    return statistics.mean(times)


def jinja_inline_simple():
    """Simple page with inline template (old approach)"""
    template = Template("""<html><head><title>{{ title }}</title><meta charset="{{ charset }}"></head><body><header><h1>{{ heading }}</h1></header><main><p>{{ content1 }}</p><p>{{ content2 }}</p></main><footer><p>{{ footer }}</p></footer></body></html>""")
    return template.render(
        title="Simple Page",
        charset="utf-8", 
        heading="Welcome",
        content1="This is a simple page with basic HTML structure.",
        content2="It includes a header, main content, and footer.",
        footer="© 2024 Benchmark Test"
    )


def jinja_environment_simple(template):
    """Simple page with environment template (new approach)"""
    return template.render(
        title="Simple Page",
        charset="utf-8",
        heading="Welcome", 
        content1="This is a simple page with basic HTML structure.",
        content2="It includes a header, main content, and footer.",
        footer="© 2024 Benchmark Test"
    )


def jinja_inline_table():
    """Data table with inline template (old approach)"""
    template = Template("""
<html>
<head>
    <title>Data Table</title>
</head>
<body>
    <h1>Performance Data</h1>
    <table>
        <thead>
            <tr>
                {% for header in headers %}
                <th>{{ header }}</th>
                {% endfor %}
            </tr>
        </thead>
        <tbody>
            {% for row in data %}
            <tr>
                <td>{{ row.id }}</td>
                <td>{{ row.name }}</td>
                <td>{{ row.email }}</td>
                <td>{{ row.department }}</td>
                <td>{{ row.salary }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
    """.strip())
    
    data = []
    for i in range(100):
        data.append({
            "id": i + 1,
            "name": f"Employee {i + 1}",
            "email": f"emp{i + 1}@company.com",
            "department": f"Dept {(i % 5) + 1}",
            "salary": f"${50000 + (i * 1000):,}"
        })
    
    return template.render(
        headers=["ID", "Name", "Email", "Department", "Salary"],
        data=data
    )


def jinja_environment_table(template):
    """Data table with environment template (new approach)"""
    data = []
    for i in range(100):
        data.append({
            "id": i + 1,
            "name": f"Employee {i + 1}",
            "email": f"emp{i + 1}@company.com",
            "department": f"Dept {(i % 5) + 1}",
            "salary": f"${50000 + (i * 1000):,}"
        })
    
    return template.render(
        headers=["ID", "Name", "Email", "Department", "Salary"],
        data=data
    )


def main():
    print("Jinja2 Implementation Comparison")
    print("=" * 50)
    
    # Set up Jinja Environment
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(
        loader=FileSystemLoader(template_dir),
        cache_size=400,
        auto_reload=False,
        optimized=True,
        finalize=lambda x: x if x is not None else ''
    )
    
    simple_template = env.get_template('simple_page.jinja2')
    table_template = env.get_template('data_table.jinja2')
    
    print("\nRunning benchmarks...")
    
    # Simple page comparison
    inline_simple_time = benchmark_function(jinja_inline_simple, 200)
    env_simple_time = benchmark_function(lambda: jinja_environment_simple(simple_template), 200)
    
    # Table comparison  
    inline_table_time = benchmark_function(jinja_inline_table, 200)
    env_table_time = benchmark_function(lambda: jinja_environment_table(table_template), 200)
    
    print("\nRESULTS:")
    print("-" * 40)
    
    print(f"\nSimple Page:")
    print(f"  Inline Template:     {inline_simple_time*1000:.3f} ms")
    print(f"  Environment Template: {env_simple_time*1000:.3f} ms")
    improvement = inline_simple_time / env_simple_time
    print(f"  Environment is {improvement:.1f}x faster")
    
    print(f"\nData Table (100 rows):")
    print(f"  Inline Template:     {inline_table_time*1000:.3f} ms")
    print(f"  Environment Template: {env_table_time*1000:.3f} ms")
    improvement = inline_table_time / env_table_time
    print(f"  Environment is {improvement:.1f}x faster")
    
    print("\nConclusion:")
    print("Using Jinja Environment with FileSystemLoader and proper")
    print("caching provides significant performance improvements over")
    print("creating Template objects with inline strings.")


if __name__ == "__main__":
    main()