# Markterm

[![CI](https://github.com/alanhape/markterm/actions/workflows/ci.yml/badge.svg)](https://github.com/alanhape/markterm/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Render markdown beautifully in your terminal with syntax highlighting and rich formatting.

## Features

- 🎨 **Rich Formatting**: Beautiful markdown rendering with colors and styles
- 💻 **Syntax Highlighting**: Code blocks with customizable themes
- 📏 **Flexible Width**: Control text wrapping with custom widths
- 🚀 **Fast**: Lightweight and quick to render
- 🎯 **Simple**: Single command, no configuration needed
- 🔧 **Cross-Platform**: Works on Windows, macOS, and Linux

## Installation

### From PyPI (Coming Soon)

```bash
pip install markterm
```

### From Source

```bash
# Clone the repository
git clone https://github.com/alanhape/markterm.git
cd markterm

# Create and activate virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

# Install the package
pip install -e .
```

### Development Installation

To install with development dependencies:

```bash
pip install -e ".[dev]"
```

## Usage

### Basic Usage

Render a markdown file:

```bash
markterm README.md
```

### With Options

Control text wrapping:

```bash
markterm README.md --wrap 80
```

Choose a syntax highlighting theme:

```bash
markterm README.md --theme dracula
```

Combine options:

```bash
markterm README.md --wrap 100 --theme github-dark
```

### As a Python Module

You can also run markterm as a Python module:

```bash
python -m markterm README.md
```

### Available Themes

Markterm supports any theme available in [Pygments](https://pygments.org/styles/), including:

- `monokai` (default)
- `dracula`
- `github-dark`
- `solarized-dark`
- `solarized-light`
- `nord`
- `gruvbox-dark`
- `one-dark`
- And many more!

## PowerShell Integration (Windows)

For Windows users, a PowerShell wrapper is included for convenient usage:

### Setup PowerShell

1. Copy `Show-Markdown.ps1` to a directory in your `$env:PATH` or your PowerShell profile directory
2. Optionally, add the script directory to your PATH

### Usage

```powershell
# Basic usage
Show-Markdown README.md

# With wrap width
Show-Markdown README.md -Wrap 80

# With custom theme
Show-Markdown README.md -Theme dracula

# All options
Show-Markdown README.md -Wrap 100 -Theme github-dark

# Works with pipeline
Get-Item README.md | Show-Markdown
```

The PowerShell script automatically:
- Locates the markterm installation (repository or installed package)
- Activates the virtual environment (if using from repository)
- Runs the command with proper arguments

## Development

### Setting Up Development Environment

```bash
# Clone and navigate to repository
git clone https://github.com/alanhape/markterm.git
cd markterm

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install with development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks (recommended)
pre-commit install
```

### Running Tests

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
```

### Code Quality

```bash
# Lint with ruff
ruff check markterm/ tests/

# Format with ruff
ruff format markterm/ tests/

# Type check with mypy
mypy markterm/

# Run all pre-commit hooks
pre-commit run --all-files
```

### Building the Package

```bash
# Install build dependencies
pip install build

# Build distribution packages
python -m build

# This creates:
# - dist/markterm-0.1.0-py3-none-any.whl
# - dist/markterm-0.1.0.tar.gz
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting (`pytest`, `ruff check`, `mypy`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

Markterm is built with:

- [Rich](https://github.com/Textualize/rich) - Beautiful terminal formatting
- [markdown-it-py](https://github.com/executablebooks/markdown-it-py) - Markdown parsing
- [Pygments](https://pygments.org/) - Syntax highlighting

## Support

- 📝 [Report Issues](https://github.com/alanhape/markterm/issues)
- 💬 [Discussions](https://github.com/alanhape/markterm/discussions)
- 📖 [Documentation](https://github.com/alanhape/markterm)

## Changelog

### v0.1.0 (2026-02-06)

- Initial release
- Basic markdown rendering
- Syntax highlighting support
- Customizable text wrapping
- Theme selection
- Cross-platform support
- PowerShell wrapper for Windows
- Comprehensive test suite
- CI/CD pipeline
- Pre-commit hooks
