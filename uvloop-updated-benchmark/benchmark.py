#!/usr/bin/env python3
"""
Benchmark script to compare asyncio and uvloop performance on Python 3.13.

This script runs the uvloop echo server benchmark with different configurations
to measure the performance difference between asyncio and uvloop.
"""

import subprocess
import time
import platform
import sys
from datetime import datetime


class BenchmarkRunner:
    """Orchestrates the echo server benchmark tests."""
    
    def __init__(self):
        self.results = []
        
    def run_server(self, use_uvloop: bool, mode: str):
        """Start echo server in background."""
        cmd = [sys.executable, "echoserver.py"]
        
        if use_uvloop:
            cmd.append("--uvloop")
        
        if mode == "streams":
            cmd.append("--streams")
        elif mode == "protocol":
            cmd.append("--proto")
        # else: default sock_recv/sock_sendall mode
        
        return subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    
    def run_client(self, message_size: int, num_messages: int = 100000, workers: int = 3):
        """Run echo client benchmark."""
        cmd = [
            sys.executable, "echoclient.py",
            "--msize", str(message_size),
            "--num", str(num_messages),
            "--workers", str(workers),
            "--times", "1"
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Parse requests/sec from output
        for line in result.stdout.split('\n'):
            if 'requests/sec' in line:
                rps = float(line.split()[0])
                return rps
        
        return 0
    
    def run_benchmark(self, use_uvloop: bool, mode: str, message_size: int):
        """Run a complete benchmark test."""
        loop_type = "uvloop" if use_uvloop else "asyncio"
        test_name = f"{loop_type} - {mode} - {message_size}B"
        
        print(f"Running: {test_name}")
        
        # Start server
        server = self.run_server(use_uvloop, mode)
        time.sleep(2)  # Give server time to start
        
        try:
            # Run client benchmark
            rps = self.run_client(message_size)
            
            result = {
                'loop': loop_type,
                'mode': mode,
                'message_size': message_size,
                'requests_per_sec': rps
            }
            
            self.results.append(result)
            print(f"  Result: {rps:,.0f} requests/sec")
            
        finally:
            # Stop server
            server.terminate()
            server.wait(timeout=5)
        
        time.sleep(1)  # Brief pause between tests
        
        return result
    
    def run_all_benchmarks(self):
        """Run comprehensive benchmark suite."""
        print("=" * 70)
        print("uvloop vs asyncio Benchmark on Python 3.13")
        print("=" * 70)
        print(f"Python version: {platform.python_version()}")
        print(f"Platform: {platform.platform()}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print()
        
        modes = ["sockets", "streams", "protocol"]
        message_sizes = [1000, 10000, 100000]  # 1KB, 10KB, 100KB
        
        for mode in modes:
            print(f"\n{'='*70}")
            print(f"Testing mode: {mode}")
            print(f"{'='*70}\n")
            
            for msg_size in message_sizes:
                # Test with asyncio
                self.run_benchmark(False, mode, msg_size)
                
                # Test with uvloop
                self.run_benchmark(True, mode, msg_size)
                
                print()
    
    def print_results(self):
        """Print formatted results table."""
        print("\n" + "=" * 70)
        print("BENCHMARK RESULTS SUMMARY")
        print("=" * 70)
        print()
        
        # Group results by mode
        for mode in ["sockets", "streams", "protocol"]:
            mode_results = [r for r in self.results if r['mode'] == mode]
            
            if not mode_results:
                continue
            
            print(f"\n{mode.upper()} Mode:")
            print("-" * 70)
            print(f"{'Message Size':<15} {'asyncio (req/s)':<20} {'uvloop (req/s)':<20} {'Speedup':<15}")
            print("-" * 70)
            
            # Group by message size
            msg_sizes = sorted(set(r['message_size'] for r in mode_results))
            
            for msg_size in msg_sizes:
                asyncio_result = next((r for r in mode_results 
                                     if r['message_size'] == msg_size and r['loop'] == 'asyncio'), None)
                uvloop_result = next((r for r in mode_results 
                                    if r['message_size'] == msg_size and r['loop'] == 'uvloop'), None)
                
                if asyncio_result and uvloop_result:
                    speedup = uvloop_result['requests_per_sec'] / asyncio_result['requests_per_sec']
                    
                    print(f"{msg_size:<15} {asyncio_result['requests_per_sec']:>18,.0f}  "
                          f"{uvloop_result['requests_per_sec']:>18,.0f}  {speedup:>13.2f}x")
        
        print("\n" + "=" * 70)
        
        # Calculate overall averages
        asyncio_avg = sum(r['requests_per_sec'] for r in self.results if r['loop'] == 'asyncio') / \
                      len([r for r in self.results if r['loop'] == 'asyncio'])
        uvloop_avg = sum(r['requests_per_sec'] for r in self.results if r['loop'] == 'uvloop') / \
                     len([r for r in self.results if r['loop'] == 'uvloop'])
        
        overall_speedup = uvloop_avg / asyncio_avg
        
        print(f"\nOverall average speedup: {overall_speedup:.2f}x")
        print(f"asyncio average: {asyncio_avg:,.0f} req/s")
        print(f"uvloop average: {uvloop_avg:,.0f} req/s")
        print()
    
    def save_results(self, filename: str):
        """Save results to file."""
        with open(filename, 'w') as f:
            f.write("=" * 70 + "\n")
            f.write("uvloop vs asyncio Benchmark Results on Python 3.13\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"System Information:\n")
            f.write(f"  Python version: {platform.python_version()}\n")
            f.write(f"  Platform: {platform.platform()}\n")
            f.write(f"  Processor: {platform.processor()}\n")
            f.write(f"  Timestamp: {datetime.now().isoformat()}\n\n")
            
            # Redirect output to file
            import io
            from contextlib import redirect_stdout
            
            output = io.StringIO()
            with redirect_stdout(output):
                self.print_results()
            
            f.write(output.getvalue())
            
            # Write raw data
            f.write("\n" + "=" * 70 + "\n")
            f.write("RAW DATA\n")
            f.write("=" * 70 + "\n\n")
            
            for result in self.results:
                f.write(f"{result}\n")


def main():
    """Main benchmark execution."""
    runner = BenchmarkRunner()
    
    try:
        runner.run_all_benchmarks()
        runner.print_results()
        
        # Save results
        filename = f"benchmark_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        runner.save_results(filename)
        print(f"Results saved to: {filename}")
        
        # Also save to standard filename
        runner.save_results("benchmark_results.txt")
        print(f"Results also saved to: benchmark_results.txt")
        
    except KeyboardInterrupt:
        print("\nBenchmark interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError during benchmark: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
