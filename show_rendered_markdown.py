#!/usr/bin/env python3
"""
show_rendered_markdown.py
Render a Markdown file to ANSI and print it to the terminal.

Dependencies:
  pip install rich

Usage:
  python show_rendered_markdown.py README.md
  python show_rendered_markdown.py README.md --wrap 100
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Render a Markdown file in the terminal.")
    p.add_argument("file", help="Path to the Markdown file")
    p.add_argument(
        "--wrap",
        type=int,
        default=None,
        help="Optional fixed width to wrap content (defaults to terminal width).",
    )
    p.add_argument(
        "--theme",
        default="monokai",
        help="Syntax highlighting theme (passed to rich). Default: monokai",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    md_path = Path(args.file).expanduser()

    if not md_path.exists():
        print(f"Error: file not found: {md_path}", file=sys.stderr)
        return 2
    if md_path.is_dir():
        print(f"Error: path is a directory, not a file: {md_path}", file=sys.stderr)
        return 2

    try:
        text = md_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        # Fallback for files with a BOM or odd encoding situations.
        text = md_path.read_text(encoding="utf-8-sig")
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        return 2

    console = Console(width=args.wrap) if args.wrap else Console()
    md = Markdown(text, code_theme=args.theme)
    console.print(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
