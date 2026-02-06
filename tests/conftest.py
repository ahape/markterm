"""Shared pytest fixtures for markterm tests."""

from pathlib import Path

import pytest


@pytest.fixture
def fixture_dir() -> Path:
    """Return path to test fixtures directory.

    Returns:
        Path to the fixtures directory.
    """
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def simple_md(fixture_dir: Path) -> Path:
    """Return path to simple markdown test file.

    Args:
        fixture_dir: Path to fixtures directory from fixture.

    Returns:
        Path to simple.md test file.
    """
    return fixture_dir / "simple.md"


@pytest.fixture
def empty_md(fixture_dir: Path) -> Path:
    """Return path to empty markdown test file.

    Args:
        fixture_dir: Path to fixtures directory from fixture.

    Returns:
        Path to empty.md test file.
    """
    return fixture_dir / "empty.md"
