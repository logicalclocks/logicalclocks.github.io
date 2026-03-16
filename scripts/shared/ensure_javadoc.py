import atexit

from hopsworks_docs.scripts.shared.docs_root import _DOCS_ROOT


def ensure_javadoc() -> None:
    """Ensure javadoc is present."""
    path = _DOCS_ROOT / "docs" / "javadoc"
    if not path.exists():
        gipath = path.parent / ".gitignore"
        if gipath.exists():
            gi = gipath.read_text()
        else:
            gi = "/.gitignore\n"
            atexit.register(lambda: gipath.unlink())
        if "/" + path.name not in gi:
            gipath.write_text(gi + f"\n/{path.name}\n")

        atexit.register(lambda: path.unlink())
        path.write_text("")
