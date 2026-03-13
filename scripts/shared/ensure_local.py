import atexit
from pathlib import Path

from hopsworks_docs.scripts.shared.docs_root import _DOCS_ROOT


def ensure_local(path: Path) -> None:
    """Ensure the given file exists locally, copying from the repo if not."""
    local_path = path.relative_to(_DOCS_ROOT)
    if not local_path.exists():
        for p in reversed(local_path.parents):
            if not p.exists():
                atexit.register(p.rmdir)
                p.mkdir()

        gipath = local_path.parent / ".gitignore"
        gi = gipath.read_text() if gipath.exists() else "/.gitignore\n"
        if "/" + local_path.name not in gi:
            gipath.write_text(gi + f"\n/{local_path.name}\n")

        atexit.register(lambda: local_path.unlink())
        local_path.write_bytes(path.read_bytes())
