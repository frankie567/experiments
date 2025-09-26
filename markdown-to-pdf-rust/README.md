# Markdown to PDF Rust

A CLI tool to convert Markdown files to beautifully formatted PDF documents with LaTeX-like typography.

## Overview

This experiment creates a fast, portable CLI tool built in Rust that can take Markdown files and generate high-quality PDF documents. The tool focuses on:

- **Direct PDF Generation**: No intermediate HTML step - parses Markdown and generates PDF directly
- **Great Typography**: LaTeX-inspired typography with proper font selection, spacing, and layout
- **Proper Pagination**: Intelligent page breaks and page numbering
- **Internal Linking**: Support for cross-references and table of contents
- **Portable**: Single binary that works across platforms
- **Fast**: Built in Rust for optimal performance

## Requirements Addressed

✅ **Built in Rust**: Uses Rust for portability and performance  
✅ **Direct PDF Generation**: Uses `printpdf` to generate PDFs directly from parsed Markdown  
✅ **Existing Crates**: Leverages `pulldown-cmark` for Markdown parsing and `printpdf` for PDF creation  
✅ **Single PDF Output**: Generates a single, well-formatted PDF document  
✅ **LaTeX-like Typography**: Implements proper typography, pagination, and linking  

## Dependencies

- `pulldown-cmark` - High-performance Markdown parser
- `printpdf` - Pure Rust PDF generation library
- `clap` - Command-line argument parsing
- `anyhow` - Simplified error handling

## Usage

```bash
# Build the tool
cargo build --release

# Convert a Markdown file to PDF
cargo run -- input.md -o output.pdf

# Or using the built binary
./target/release/markdown-to-pdf-rust input.md -o output.pdf
```

## Features

### Typography
- LaTeX-inspired font selection and sizing
- Proper line spacing and paragraph margins
- Hierarchical heading styles
- Code block formatting with monospace fonts

### Document Structure
- Automatic page numbering
- Table of contents generation
- Header and footer support
- Intelligent page breaks

### Markdown Support
- Standard Markdown syntax
- Code blocks with syntax highlighting
- Tables
- Links (both external and internal)
- Images (when supported)
- Lists (ordered and unordered)

## Implementation Details

The tool follows a multi-stage processing pipeline:

1. **Parse**: Uses `pulldown-cmark` to parse Markdown into an AST
2. **Layout**: Calculates typography and page layout parameters
3. **Render**: Uses `printpdf` to generate the final PDF document

This approach ensures optimal performance while maintaining clean separation of concerns.

## Sample Files

The repository includes sample Markdown files to test various features:
- `samples/simple.md` - Basic formatting test
- `samples/complex.md` - Advanced features test
- `samples/technical.md` - Technical document with code blocks

## Building and Running

```bash
# Install dependencies and build
cargo build

# Run with sample file
cargo run -- samples/simple.md -o simple.pdf

# Build release version
cargo build --release
```