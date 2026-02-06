#!/usr/bin/env python3
"""Render a Markdown file to ANSI and print it to the terminal.

This module provides a command-line interface for rendering markdown files
with syntax highlighting and rich formatting using the Rich library.

Usage:
    markterm README.md
    markterm README.md --wrap 100
    markterm README.md --theme monokai
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown

# Exit codes
EXIT_SUCCESS = 0
EXIT_ERROR = 2

# Constants
MAX_FILE_SIZE_MB = 100


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments containing file path, optional wrap width, and theme.
    """
    parser = argparse.ArgumentParser(
        description="Render a Markdown file in the terminal with syntax highlighting.",
        epilog="Example: markterm README.md --wrap 100 --theme monokai",
    )
    parser.add_argument(
        "file",
        help="Path to the Markdown file to render",
    )
    parser.add_argument(
        "--wrap",
        type=int,
        default=None,
        metavar="WIDTH",
        help="Fixed width to wrap content (defaults to terminal width)",
    )
    parser.add_argument(
        "--theme",
        default="monokai",
        metavar="THEME",
        help="Syntax highlighting theme for code blocks (default: monokai)",
    )
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> tuple[bool, str]:
    """Validate parsed command-line arguments.

    Args:
        args: Parsed arguments from argparse.

    Returns:
        A tuple of (is_valid, error_message). If valid, error_message is empty.
    """
    if args.wrap is not None and args.wrap <= 0:
        return False, "--wrap must be a positive integer"
    return True, ""


def read_markdown_file(path: Path) -> str:
    """Read markdown content from a file with encoding fallback.

    Attempts to read the file with UTF-8 encoding, falling back to UTF-8-sig
    if a BOM is detected.

    Args:
        path: Path to the markdown file to read.

    Returns:
        The content of the markdown file as a string.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        IsADirectoryError: If the path points to a directory.
        PermissionError: If the file cannot be read due to permissions.
        OSError: For other file system errors.
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if path.is_dir():
        raise IsADirectoryError(f"Path is a directory, not a file: {path}")

    # Check file size
    file_size_mb = path.stat().st_size / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        raise OSError(f"File too large: {file_size_mb:.1f}MB (max: {MAX_FILE_SIZE_MB}MB)")

    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        # Fallback for files with a BOM or odd encoding situations
        return path.read_text(encoding="utf-8-sig")


def render_markdown(text: str, wrap_width: int | None = None, theme: str = "monokai") -> None:
    """Render markdown text to the terminal.

    Args:
        text: The markdown content to render.
        wrap_width: Optional fixed width for wrapping. Uses terminal width if None.
        theme: Syntax highlighting theme for code blocks.
    """
    console = Console(width=wrap_width) if wrap_width else Console()
    md = Markdown(text, code_theme=theme)
    console.print(md)


def main() -> int:
    """Main entry point for the markterm CLI.

    Parses arguments, reads the markdown file, and renders it to the terminal.

    Returns:
        Exit code: EXIT_SUCCESS (0) for success, EXIT_ERROR (2) for errors.
    """
    args = parse_args()

    # Validate arguments
    is_valid, error_msg = validate_args(args)
    if not is_valid:
        print(f"Error: {error_msg}", file=sys.stderr)
        return EXIT_ERROR

    # Resolve file path
    md_path = Path(args.file).expanduser().resolve()

    # Read markdown file
    try:
        text = read_markdown_file(md_path)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return EXIT_ERROR
    except IsADirectoryError as e:
        print(f"Error: {e}", file=sys.stderr)
        return EXIT_ERROR
    except PermissionError:
        print(f"Error: Permission denied: {md_path}", file=sys.stderr)
        return EXIT_ERROR
    except OSError as e:
        print(f"Error: {e}", file=sys.stderr)
        return EXIT_ERROR

    # Render markdown
    try:
        render_markdown(text, wrap_width=args.wrap, theme=args.theme)
    except Exception as e:
        print(f"Error rendering markdown: {e}", file=sys.stderr)
        return EXIT_ERROR

    return EXIT_SUCCESS


if __name__ == "__main__":
    raise SystemExit(main())
