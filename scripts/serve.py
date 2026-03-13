import subprocess
from pathlib import Path
from typing import Annotated

import typer


_DOCS_ROOT = Path(__file__).parent.parent


def serve(
    port: Annotated[int, typer.Option(help="Port to serve on.")] = 8000,
):
    """Serve the documentation site locally."""
    subprocess.run(
        [
            "mkdocs",
            "serve",
            "-f",
            str(_DOCS_ROOT / "mkdocs.yml"),
            "--dev-addr",
            f"localhost:{port}",
        ],
        check=True,
    )
