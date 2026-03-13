import subprocess
from pathlib import Path


_DOCS_ROOT = Path(__file__).parent.parent


def check():
    """Check the documentation."""
    subprocess.run(
        [
            "mkdocs",
            "build",
            "-s",
            "-f",
            str(_DOCS_ROOT / "mkdocs.yml"),
        ],
        check=True,
    )
