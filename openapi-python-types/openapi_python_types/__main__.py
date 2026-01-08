"""Command-line interface for openapi-python-types."""

import argparse
import sys
from pathlib import Path

from .generator import generate_types


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate Python type definitions from OpenAPI specifications"
    )
    parser.add_argument(
        "spec",
        type=str,
        help="Path to OpenAPI specification file (JSON or YAML)",
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["json", "yaml", "auto"],
        default="auto",
        help="Format of the specification file (default: auto-detect)",
    )
    
    args = parser.parse_args()
    
    # Read the specification file
    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"Error: File not found: {args.spec}", file=sys.stderr)
        sys.exit(1)
    
    spec_content = spec_path.read_text()
    
    # Generate types
    try:
        types_code = generate_types(spec_content, args.format)
        print(types_code)
    except Exception as e:
        print(f"Error generating types: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
