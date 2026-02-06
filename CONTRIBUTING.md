# Contributing to Markterm

Thank you for your interest in contributing to Markterm! This document provides guidelines and instructions for contributing to the project.

## Getting Started

### Prerequisites

- Python 3.12 or higher
- Git

### Setting Up Your Development Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/markterm.git
   cd markterm
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # macOS/Linux
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install the package in editable mode with development dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Set up pre-commit hooks (recommended):**
   ```bash
   pre-commit install
   ```

## Development Workflow

1. **Create a new branch for your changes:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Write clear, readable code
   - Follow the existing code style
   - Add or update tests as needed
   - Update documentation if necessary

3. **Run tests:**
   ```bash
   pytest
   pytest --cov=markterm  # with coverage
   ```

4. **Check code quality:**
   ```bash
   # Linting
   ruff check markterm/ tests/

   # Formatting
   ruff format markterm/ tests/

   # Type checking
   mypy markterm/
   ```

5. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Brief description of your changes"
   ```

6. **Push your branch and create a pull request:**
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style

### Formatting and Linting

- We use **Ruff** for linting and formatting
- Maximum line length: 100 characters
- Target Python version: 3.12+
- Run `ruff format` before committing

### Type Hints

- **All functions must have type hints** for parameters and return values
- We use **mypy** in strict mode
- Run `mypy markterm/` to check types

### Documentation

- Use **Google-style docstrings** for all public functions and classes
- Include:
  - Brief description
  - Args section with parameter descriptions
  - Returns section with return value description
  - Raises section for exceptions (if applicable)

Example:
```python
def read_markdown_file(path: Path) -> str:
    """Read markdown content with encoding fallback.

    Args:
        path: Path to the markdown file to read.

    Returns:
        The content of the markdown file as a string.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        IsADirectoryError: If the path is a directory.
        PermissionError: If the file cannot be read.
    """
```

## Running Tests

### Basic Test Run
```bash
pytest
```

### With Coverage Report
```bash
pytest --cov=markterm --cov-report=term-missing
```

### Run Specific Tests
```bash
pytest tests/test_cli.py::TestParseArgs
```

### Coverage Goal
- Maintain at least **90% code coverage**
- Add tests for any new functionality
- Update tests when modifying existing code

## Pre-commit Hooks

Pre-commit hooks automatically run checks before each commit:

- Trailing whitespace removal
- End-of-file fixing
- YAML/TOML validation
- Ruff linting and formatting
- Mypy type checking

To run hooks manually:
```bash
pre-commit run --all-files
```

## Pull Request Checklist

Before submitting a pull request, ensure:

- [ ] All tests pass (`pytest`)
- [ ] Code coverage is maintained or improved
- [ ] Code is properly formatted (`ruff format`)
- [ ] No linting errors (`ruff check`)
- [ ] Type checking passes (`mypy markterm/`)
- [ ] Type hints are added to new functions
- [ ] Documentation is updated (if applicable)
- [ ] CHANGELOG entry added (if applicable)
- [ ] Pre-commit hooks pass

## Reporting Issues

When reporting issues, please include:

- **Description:** Clear description of the issue
- **Steps to reproduce:** Detailed steps to reproduce the problem
- **Expected behavior:** What you expected to happen
- **Actual behavior:** What actually happened
- **Environment:** Python version, OS, markterm version
- **Error messages:** Full error messages and tracebacks (if applicable)

## Questions?

If you have questions about contributing, feel free to:
- Open an issue for discussion
- Check existing issues and pull requests

Thank you for contributing to Markterm!
