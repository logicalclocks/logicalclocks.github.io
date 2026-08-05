"""Read-only MCP server for the Hopsworks documentation."""

__all__ = ["main"]


def main() -> None:
    """Entry point; imports the server lazily so the index stays importable."""
    from .server import main as _main

    _main()
