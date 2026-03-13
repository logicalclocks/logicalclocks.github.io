import atexit

from hopsworks_docs.scripts.shared.docs_root import _DOCS_ROOT


def ensure_javadoc() -> None:
    """Ensure javadoc is present."""
    path = _DOCS_ROOT / "docs" / "javadoc"
    if not path.exists():
        atexit.register(lambda: path.unlink())
        path.write_text("")
