# Markterm OpenCode Instructions

## Commands
- **Install for dev**: `pip install -e ".[dev]" && pre-commit install`
- **Lint & format**: `ruff check markterm/ tests/ --fix && ruff format markterm/ tests/`
- **Type check**: `mypy markterm/`
- **Test single file**: `pytest tests/test_cli.py`
- **Full verify**: Run lint, type check, then `pytest --cov=markterm --cov-report=term-missing`
- **Coverage target**: 84%

## Architecture
- **Main entry**: `markterm/cli.py:main()`
- **Core logic**: Functions in `markterm/cli.py` - parse_args, validate_args, read_markdown_file, render_markdown
- **PowerShell wrapper**: `Show-Markdown.ps1` for Windows, auto-locates venv and runs Python command
- **File limits**: 100MB max, UTF-8 & UTF-8-sig encodings
- **Exit codes**: SUCCESS=0, ERROR=2

## Code Style
- **Type hints**: Full annotation, `from __future__ import annotations`
- **Docstrings**: Google-style for public functions
- **Error handling**: Specific exceptions only, no broad try/except
- **Imports**: Ruff handles sorting

## Testing
- **Fixtures**: `tests/conftest.py` (fixture_dir, simple_md, empty_md)
- **Structure**: 3 classes in test_cli.py - TestParseArgs, TestValidateArgs, etc.
- **Integration tests**: End-to-end in TestIntegration
- **Update on change**: Always add/modify tests when editing code

## CI Order
- Lint and type check run first (parallelizable); tests depend on them passing; build depends on all

## Deprecated
- `show_rendered_markdown.py`: Keep for compatibility, but use `markterm.cli` module entry