#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "dramatiq",
#     "redis",
#     "psutil",
# ]
# ///

"""
Worker script to process fixed middleware test tasks.
This runs a dramatiq worker to execute the fixed_oom_task.
"""

import sys
from dramatiq.cli import main as dramatiq_main

if __name__ == "__main__":
    # Run dramatiq worker
    sys.argv = [
        "dramatiq",
        "test_fixed_middleware:broker",
        "-p", "1",  # 1 process
        "-t", "1",  # 1 thread per process
    ]
    dramatiq_main()
