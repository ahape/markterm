"""Allow running markterm as: python -m markterm"""

from markterm.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
