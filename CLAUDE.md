# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Markterm is a command-line tool for rendering Markdown files with rich formatting in the terminal. It uses Python's `rich` library to provide syntax highlighting and formatted output.

**Version**: 0.1.0
**Python**: 3.12+
**License**: MIT

## Architecture

### Package Structure

```
markterm/
├── markterm/           # Main package directory
│   ├── __init__.py    # Package initialization with version
│   ├── __main__.py    # Entry point for `python -m markterm`
│   └── cli.py         # Core CLI implementation
├── tests/             # Test suite
│   ├── conftest.py    # Pytest fixtures
│   ├── test_cli.py    # CLI tests
│   └── test_main.py   # Module execution tests
├── .github/
│   └── workflows/
│       └── ci.yml     # CI/CD pipeline
├── pyproject.toml     # Package configuration and dependencies
├── Show-Markdown.ps1  # PowerShell wrapper for Windows
└── example.md         # Example markdown file
```

### Core Components

- **markterm/cli.py**: Main CLI implementation
  - `parse_args()`: Command-line argument parsing
  - `validate_args()`: Argument validation (wrap width, etc.)
  - `read_markdown_file()`: File reading with encoding fallback and size limits
  - `render_markdown()`: Markdown rendering with Rich library
  - `main()`: Entry point that orchestrates the workflow
  - Uses `rich.console.Console` for terminal output
  - Uses `rich.markdown.Markdown` for markdown parsing and rendering
  - Supports custom wrap widths and syntax highlighting themes
  - Handles UTF-8 and UTF-8-sig encodings
  - File size limit: 100MB

- **Show-Markdown.ps1**: PowerShell wrapper for Windows
  - Uses `$PSScriptRoot` to locate the repository dynamically
  - Supports both repository and installed package modes
  - Activates virtual environment automatically
  - Passes through --wrap and --theme options

## Setup

### Initial Setup
```bash
# Clone and navigate to repository
git clone <repository-url>
cd markterm

# Create and activate virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

# Install package in editable mode
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"
```

## Development Commands

### Running the Tool

**Installed package:**
```bash
markterm <filename>
markterm <filename> --wrap 100
markterm <filename> --theme dracula
```

**As Python module:**
```bash
python -m markterm <filename>
python -m markterm <filename> --wrap 100 --theme monokai
```

**Windows PowerShell:**
```powershell
Show-Markdown <filename>
Show-Markdown <filename> -Wrap 100 -Theme dracula
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=markterm

# Run with detailed coverage report
pytest --cov=markterm --cov-report=term-missing

# Run specific test file
pytest tests/test_cli.py

# Run specific test class
pytest tests/test_cli.py::TestMain

# Run specific test
pytest tests/test_cli.py::TestMain::test_main_success
```

**Test Structure:**
- `tests/conftest.py`: Shared fixtures (fixture_dir, simple_md, empty_md)
- `tests/test_cli.py`: Comprehensive CLI tests (28 tests)
  - TestParseArgs: Argument parsing tests
  - TestValidateArgs: Validation tests
  - TestReadMarkdownFile: File reading tests
  - TestRenderMarkdown: Rendering tests
  - TestMain: Main function tests
  - TestIntegration: End-to-end tests
- `tests/test_main.py`: Module execution test
- `tests/fixtures/`: Test markdown files

**Coverage Target**: >84% (current: 84%)

### Code Quality

**Linting:**
```bash
# Run ruff linting
ruff check markterm/ tests/

# Auto-fix issues
ruff check --fix markterm/ tests/
```

**Formatting:**
```bash
# Check formatting
ruff format --check markterm/ tests/

# Format code
ruff format markterm/ tests/
```

**Type Checking:**
```bash
# Run mypy
mypy markterm/
```

**Pre-commit Hooks:**
```bash
# Install hooks
pre-commit install

# Run all hooks manually
pre-commit run --all-files
```

### Building the Package

```bash
# Install build dependencies
pip install build

# Build distribution packages
python -m build

# Output:
# - dist/markterm-0.1.0-py3-none-any.whl
# - dist/markterm-0.1.0.tar.gz
```

### Installing Built Package

```bash
# Install from wheel
pip install dist/markterm-0.1.0-py3-none-any.whl

# Or from source distribution
pip install dist/markterm-0.1.0.tar.gz
```

## Dependencies

### Runtime Dependencies
- **rich** (>=14.0.0): Terminal rendering and markdown formatting
- **markdown-it-py** (>=4.0.0): Markdown parsing (transitive dependency of rich)
- **Pygments** (>=2.18.0): Syntax highlighting for code blocks

### Development Dependencies
- **pytest** (>=8.0.0): Testing framework
- **pytest-cov** (>=6.0.0): Coverage reporting
- **mypy** (>=1.8.0): Type checking
- **ruff** (>=0.8.0): Linting and formatting
- **pre-commit** (>=4.0.0): Git hooks management

## Configuration

All configuration is in `pyproject.toml`:

**[tool.ruff]**
- Line length: 100
- Target version: Python 3.12
- Selected rules: E, W, F, I, N, UP, B, C4, SIM, TCH, RUF

**[tool.mypy]**
- Strict mode enabled
- Python version: 3.12

**[tool.pytest.ini_options]**
- Test paths: tests/
- Strict markers and config
- Show locals on failure

**[tool.coverage]**
- Source: markterm/
- Branch coverage enabled
- Precision: 2 decimal places
- Show missing lines

## CI/CD Pipeline

GitHub Actions workflow (`.github/workflows/ci.yml`):

**Jobs:**
1. **lint**: Ruff linting and formatting checks (Ubuntu, Python 3.12)
2. **type-check**: Mypy type checking (Ubuntu, Python 3.12)
3. **test**: Pytest with coverage (Matrix: Ubuntu/Windows/macOS × Python 3.12/3.13/3.14)
4. **build**: Package building (Ubuntu, requires all previous jobs to pass)

**Triggers:**
- Push to master/main branches
- Pull requests to master/main branches

## Code Style Guidelines

### Type Hints
- **Required** for all function parameters and return values
- Use `from __future__ import annotations` for forward references
- Use `int | None` instead of `Optional[int]` (Python 3.10+ union syntax)

### Docstrings
- **Google-style docstrings** for all public functions
- Include: brief description, Args, Returns, Raises (if applicable)

### Error Handling
- Use specific exception types (FileNotFoundError, IsADirectoryError, etc.)
- Print errors to stderr with descriptive messages
- Return EXIT_ERROR (2) for error conditions

### Constants
- Define at module level (EXIT_SUCCESS, EXIT_ERROR, MAX_FILE_SIZE_MB)
- Use UPPER_SNAKE_CASE for constants

### Functions
- Keep functions focused on single responsibilities
- Extract validation logic into separate functions
- Use explicit error handling over broad try/except

## Common Tasks

### Adding a New Feature
1. Create a feature branch
2. Implement the feature in `markterm/cli.py`
3. Add tests in `tests/test_cli.py`
4. Run tests: `pytest --cov=markterm`
5. Run linting: `ruff check markterm/ tests/`
6. Run type checking: `mypy markterm/`
7. Update documentation if needed
8. Commit and push

### Fixing a Bug
1. Write a failing test that reproduces the bug
2. Fix the bug in the code
3. Verify the test now passes
4. Run full test suite to ensure no regressions
5. Update documentation if behavior changed

### Releasing a New Version
1. Update version in `markterm/__init__.py`
2. Update version in `pyproject.toml`
3. Update CHANGELOG in README.md
4. Run full test suite
5. Build package: `python -m build`
6. Tag the release: `git tag v0.x.x`
7. Push tag: `git push --tags`

## Troubleshooting

### Tests Failing
- Ensure virtual environment is activated
- Install dev dependencies: `pip install -e ".[dev]"`
- Check Python version: `python --version` (should be 3.12+)

### Import Errors
- Reinstall package: `pip install -e .`
- Check that you're in the correct directory

### PowerShell Script Not Working
- Verify script is in repository root
- Check that virtual environment exists at `.venv/`
- Ensure package is installed: `pip install -e .`

### Type Checking Failures
- Run `mypy markterm/` to see specific errors
- Ensure all function parameters and returns have type hints
- Check for missing imports in type annotations

## Notes for Claude

- This is a production-ready package following Python best practices
- All code must pass ruff, mypy, and pytest before committing
- Maintain or improve the 84% test coverage
- Use explicit type hints and Google-style docstrings
- Follow the existing code structure and patterns
- Update tests when modifying functionality
- The old `show_rendered_markdown.py` script is deprecated (keep temporarily for compatibility)
