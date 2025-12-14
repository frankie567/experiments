#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "dramatiq",
#     "redis",
#     "psutil",
# ]
# ///

"""Worker script for nested exceptions scenario."""

import sys
from dramatiq.cli import main as dramatiq_main

if __name__ == "__main__":
    sys.argv = [
        "dramatiq",
        "scenario_nested_exceptions:broker",
        "-p", "1",
        "-t", "1",
    ]
    dramatiq_main()
