#!/usr/bin/env python3
"""
Profile Tagflow execution to identify performance bottlenecks.

This script uses cProfile to analyze where time is spent during HTML generation
with Tagflow, helping identify the most significant performance issues.
"""

import cProfile
import pstats
import time
import tagflow
from io import StringIO


def profile_simple_page():
    """Generate a simple HTML page using tagflow for profiling"""
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


def profile_complex_page():
    """Generate a complex HTML page using tagflow for profiling"""
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


def profile_data_table():
    """Generate a data table using tagflow for profiling"""
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


def run_profiling():
    """Run profiling on different scenarios"""
    
    print("Profiling Tagflow Performance")
    print("=" * 50)
    
    # Profile each scenario
    scenarios = [
        ("Simple Page", profile_simple_page),
        ("Complex Page", profile_complex_page),
        ("Data Table", profile_data_table),
    ]
    
    for scenario_name, func in scenarios:
        print(f"\n📊 Profiling {scenario_name}...")
        
        # Create profiler
        profiler = cProfile.Profile()
        
        # Profile multiple iterations to get meaningful data
        profiler.enable()
        for _ in range(100):  # Run 100 iterations for better statistics
            func()
        profiler.disable()
        
        # Save and analyze results
        profile_file = f"tagflow_profile_{scenario_name.lower().replace(' ', '_')}.prof"
        profiler.dump_stats(profile_file)
        
        # Print top functions
        print(f"   Saved profile to: {profile_file}")
        
        # Analyze results
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        
        print(f"   Top 10 functions by cumulative time:")
        # Capture output
        import sys
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        stats.print_stats(10)
        captured = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        # Extract just the function lines for cleaner output
        lines = captured.split('\n')
        for line in lines:
            if 'tagflow' in line or 'ET.' in line or 'xml.etree' in line or line.strip().endswith('.py'):
                print(f"     {line.strip()}")
    
    # Create overall profile
    print(f"\n📊 Creating comprehensive profile...")
    overall_profiler = cProfile.Profile()
    
    overall_profiler.enable()
    # Run a mix of all scenarios
    for _ in range(50):
        profile_simple_page()
    for _ in range(20):
        profile_complex_page()
    for _ in range(10):
        profile_data_table()
    overall_profiler.disable()
    
    overall_profiler.dump_stats("tagflow_profile_comprehensive.prof")
    print("   Saved comprehensive profile to: tagflow_profile_comprehensive.prof")
    
    # Generate readable report
    stats = pstats.Stats("tagflow_profile_comprehensive.prof")
    
    print(f"\n📈 Performance Analysis Summary")
    print("-" * 50)
    
    # Top functions by cumulative time
    print("\nTop 15 functions by cumulative time:")
    stats.sort_stats('cumulative')
    import sys
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    stats.print_stats(15)
    captured = sys.stdout.getvalue()
    sys.stdout = old_stdout
    print(captured)
    
    # Top functions by time per call
    print("\nTop 15 functions by time per call:")
    stats.sort_stats('tottime')
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    stats.print_stats(15)
    captured = sys.stdout.getvalue()
    sys.stdout = old_stdout
    print(captured)
    
    print(f"\n✅ Profiling completed!")
    print(f"📋 Analysis:")
    print(f"   - Profile files saved for detailed analysis")
    print(f"   - Run 'python -m pstats tagflow_profile_comprehensive.prof' for interactive analysis")
    print(f"   - Look for high cumulative times in tagflow, xml.etree, and context variable operations")


if __name__ == "__main__":
    run_profiling()