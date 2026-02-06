"""Tests for markterm __main__ module."""

import subprocess
import sys
from pathlib import Path


def test_main_module_execution() -> None:
    """Test running markterm as a module with python -m."""
    example_path = Path("example.md")
    if not example_path.exists():
        # Create a temporary test file
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test\n")
            test_file = f.name

        try:
            result = subprocess.run(
                [sys.executable, "-m", "markterm", test_file],
                capture_output=True,
                text=True,
                timeout=5,
            )
            assert result.returncode == 0
        finally:
            Path(test_file).unlink()
    else:
        result = subprocess.run(
            [sys.executable, "-m", "markterm", str(example_path)],
            capture_output=True,
            text=True,
            timeout=5,
        )
        assert result.returncode == 0
        assert len(result.stdout) > 0
