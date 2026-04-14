# Markterm OpenCode Instructions

## Commands
- **Install for dev**: `pip install -e .`

## Architecture
- **Main entry**: `markterm/cli.py:main()`
- **Core logic**: Functions in `markterm/cli.py` - parse_args, validate_args, read_markdown_file, render_markdown, render_browser_preview
- **PowerShell wrapper**: `Show-Markdown.psm1` for Windows, forwards to the installed `markterm` command
- **File limits**: 100MB max, UTF-8 & UTF-8-sig encodings
- **Exit codes**: SUCCESS=0, ERROR=2

## Code Style
- **Type hints**: Full annotation, `from __future__ import annotations`
- **Docstrings**: Google-style for public functions
- **Error handling**: Specific exceptions only, no broad try/except
- **Imports**: Alphabetical sorting

## Compatibility
- `--html`: Kept as a CLI alias for `--browser`
