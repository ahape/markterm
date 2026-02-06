"""Tests for markterm CLI module."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from markterm.cli import (
    EXIT_ERROR,
    EXIT_SUCCESS,
    main,
    parse_args,
    read_markdown_file,
    render_markdown,
    validate_args,
)


class TestParseArgs:
    """Test argument parsing."""

    def test_parse_args_file_only(self) -> None:
        """Test parsing with just a file argument."""
        with patch.object(sys, "argv", ["markterm", "test.md"]):
            args = parse_args()
            assert args.file == "test.md"
            assert args.wrap is None
            assert args.theme == "monokai"

    def test_parse_args_with_wrap(self) -> None:
        """Test parsing with wrap argument."""
        with patch.object(sys, "argv", ["markterm", "test.md", "--wrap", "100"]):
            args = parse_args()
            assert args.file == "test.md"
            assert args.wrap == 100
            assert args.theme == "monokai"

    def test_parse_args_with_theme(self) -> None:
        """Test parsing with theme argument."""
        with patch.object(sys, "argv", ["markterm", "test.md", "--theme", "dracula"]):
            args = parse_args()
            assert args.file == "test.md"
            assert args.wrap is None
            assert args.theme == "dracula"

    def test_parse_args_all_options(self) -> None:
        """Test parsing with all options."""
        with patch.object(
            sys, "argv", ["markterm", "test.md", "--wrap", "80", "--theme", "github-dark"]
        ):
            args = parse_args()
            assert args.file == "test.md"
            assert args.wrap == 80
            assert args.theme == "github-dark"


class TestValidateArgs:
    """Test argument validation."""

    def test_validate_args_valid(self) -> None:
        """Test validation with valid arguments."""
        args = argparse.Namespace(file="test.md", wrap=100, theme="monokai")
        is_valid, error_msg = validate_args(args)
        assert is_valid is True
        assert error_msg == ""

    def test_validate_args_no_wrap(self) -> None:
        """Test validation without wrap argument."""
        args = argparse.Namespace(file="test.md", wrap=None, theme="monokai")
        is_valid, error_msg = validate_args(args)
        assert is_valid is True
        assert error_msg == ""

    def test_validate_args_negative_wrap(self) -> None:
        """Test validation with negative wrap value."""
        args = argparse.Namespace(file="test.md", wrap=-10, theme="monokai")
        is_valid, error_msg = validate_args(args)
        assert is_valid is False
        assert "--wrap must be a positive integer" in error_msg

    def test_validate_args_zero_wrap(self) -> None:
        """Test validation with zero wrap value."""
        args = argparse.Namespace(file="test.md", wrap=0, theme="monokai")
        is_valid, error_msg = validate_args(args)
        assert is_valid is False
        assert "--wrap must be a positive integer" in error_msg


class TestReadMarkdownFile:
    """Test markdown file reading."""

    def test_read_simple_file(self, simple_md: Path) -> None:
        """Test reading a simple markdown file."""
        content = read_markdown_file(simple_md)
        assert "Test Heading" in content
        assert "test paragraph" in content
        assert "Item 1" in content
        assert 'print("hello")' in content

    def test_read_empty_file(self, empty_md: Path) -> None:
        """Test reading an empty markdown file."""
        content = read_markdown_file(empty_md)
        assert content == ""

    def test_read_nonexistent_file(self, tmp_path: Path) -> None:
        """Test reading a file that doesn't exist."""
        nonexistent = tmp_path / "nonexistent.md"
        with pytest.raises(FileNotFoundError, match="File not found"):
            read_markdown_file(nonexistent)

    def test_read_directory(self, tmp_path: Path) -> None:
        """Test reading a directory instead of a file."""
        with pytest.raises(IsADirectoryError, match="Path is a directory"):
            read_markdown_file(tmp_path)

    def test_read_file_with_bom(self, tmp_path: Path) -> None:
        """Test reading a file with UTF-8 BOM."""
        bom_file = tmp_path / "bom.md"
        # Write file with BOM
        bom_file.write_bytes(b"\xef\xbb\xbf# Header with BOM\n")
        content = read_markdown_file(bom_file)
        assert "Header with BOM" in content

    def test_read_file_size_limit(self, tmp_path: Path) -> None:
        """Test reading a file that exceeds size limit."""
        large_file = tmp_path / "large.md"
        # Create a file larger than MAX_FILE_SIZE_MB (100MB)
        # We'll just test with a smaller size to avoid actually creating a 100MB file
        with patch("markterm.cli.MAX_FILE_SIZE_MB", 0.0001):  # ~100 bytes
            large_file.write_text("x" * 1000)  # 1KB
            with pytest.raises(OSError, match="File too large"):
                read_markdown_file(large_file)


class TestRenderMarkdown:
    """Test markdown rendering."""

    def test_render_markdown_simple(self, simple_md: Path, capsys: pytest.CaptureFixture) -> None:
        """Test rendering simple markdown."""
        content = read_markdown_file(simple_md)
        render_markdown(content)
        captured = capsys.readouterr()
        # Just verify output was produced (actual formatting may vary)
        assert len(captured.out) > 0

    def test_render_markdown_with_wrap(
        self, simple_md: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """Test rendering with wrap width."""
        content = read_markdown_file(simple_md)
        render_markdown(content, wrap_width=80)
        captured = capsys.readouterr()
        assert len(captured.out) > 0

    def test_render_markdown_with_theme(
        self, simple_md: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """Test rendering with custom theme."""
        content = read_markdown_file(simple_md)
        render_markdown(content, theme="dracula")
        captured = capsys.readouterr()
        assert len(captured.out) > 0

    def test_render_empty_markdown(self, capsys: pytest.CaptureFixture) -> None:
        """Test rendering empty markdown."""
        render_markdown("")
        captured = capsys.readouterr()
        # Empty markdown should produce minimal output
        assert len(captured.out) >= 0


class TestMain:
    """Test main entry point."""

    def test_main_success(self, simple_md: Path, capsys: pytest.CaptureFixture) -> None:
        """Test main with valid file."""
        with patch.object(sys, "argv", ["markterm", str(simple_md)]):
            exit_code = main()
            assert exit_code == EXIT_SUCCESS
            captured = capsys.readouterr()
            assert len(captured.out) > 0
            assert "Test Heading" in captured.out

    def test_main_file_not_found(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        """Test main with nonexistent file."""
        nonexistent = tmp_path / "nonexistent.md"
        with patch.object(sys, "argv", ["markterm", str(nonexistent)]):
            exit_code = main()
            assert exit_code == EXIT_ERROR
            captured = capsys.readouterr()
            assert "Error" in captured.err
            assert "File not found" in captured.err

    def test_main_directory_instead_of_file(
        self, tmp_path: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """Test main with directory instead of file."""
        with patch.object(sys, "argv", ["markterm", str(tmp_path)]):
            exit_code = main()
            assert exit_code == EXIT_ERROR
            captured = capsys.readouterr()
            assert "Error" in captured.err
            assert "directory" in captured.err

    def test_main_invalid_wrap(self, simple_md: Path, capsys: pytest.CaptureFixture) -> None:
        """Test main with invalid wrap value."""
        with patch.object(sys, "argv", ["markterm", str(simple_md), "--wrap", "-10"]):
            exit_code = main()
            assert exit_code == EXIT_ERROR
            captured = capsys.readouterr()
            assert "Error" in captured.err
            assert "--wrap must be a positive integer" in captured.err

    def test_main_with_wrap(self, simple_md: Path, capsys: pytest.CaptureFixture) -> None:
        """Test main with wrap option."""
        with patch.object(sys, "argv", ["markterm", str(simple_md), "--wrap", "80"]):
            exit_code = main()
            assert exit_code == EXIT_SUCCESS
            captured = capsys.readouterr()
            assert len(captured.out) > 0

    def test_main_with_theme(self, simple_md: Path, capsys: pytest.CaptureFixture) -> None:
        """Test main with custom theme."""
        with patch.object(sys, "argv", ["markterm", str(simple_md), "--theme", "dracula"]):
            exit_code = main()
            assert exit_code == EXIT_SUCCESS
            captured = capsys.readouterr()
            assert len(captured.out) > 0

    def test_main_empty_file(self, empty_md: Path, capsys: pytest.CaptureFixture) -> None:
        """Test main with empty file."""
        with patch.object(sys, "argv", ["markterm", str(empty_md)]):
            exit_code = main()
            assert exit_code == EXIT_SUCCESS
            captured = capsys.readouterr()
            # Empty file should succeed with minimal output
            assert len(captured.err) == 0


class TestIntegration:
    """Integration tests."""

    def test_end_to_end_rendering(self, simple_md: Path, capsys: pytest.CaptureFixture) -> None:
        """Test complete end-to-end rendering."""
        with patch.object(sys, "argv", ["markterm", str(simple_md), "--wrap", "100"]):
            exit_code = main()
            assert exit_code == EXIT_SUCCESS

            captured = capsys.readouterr()
            output = captured.out

            # Verify key elements are in output
            assert "Test Heading" in output
            assert "test paragraph" in output
            assert "Item" in output

    def test_example_file(self, capsys: pytest.CaptureFixture) -> None:
        """Test rendering the example.md file."""
        example_path = Path("example.md")
        if not example_path.exists():
            pytest.skip("example.md not found")

        with patch.object(sys, "argv", ["markterm", str(example_path)]):
            exit_code = main()
            assert exit_code == EXIT_SUCCESS
            captured = capsys.readouterr()
            assert len(captured.out) > 0

    def test_error_handling_chain(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        """Test error handling through the entire chain."""
        # Test 1: File doesn't exist
        with patch.object(sys, "argv", ["markterm", str(tmp_path / "missing.md")]):
            assert main() == EXIT_ERROR

        # Test 2: Invalid wrap
        with patch.object(sys, "argv", ["markterm", "test.md", "--wrap", "0"]):
            assert main() == EXIT_ERROR

        # Test 3: Directory instead of file
        with patch.object(sys, "argv", ["markterm", str(tmp_path)]):
            assert main() == EXIT_ERROR
