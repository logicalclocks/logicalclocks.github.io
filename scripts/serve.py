import subprocess
from typing import Annotated

import typer
from hopsworks_docs.scripts.shared.docs_root import _DOCS_ROOT
from hopsworks_docs.scripts.shared.ensure_local import ensure_local


def serve(
    port: Annotated[int, typer.Option(help="Port to serve on.")] = 8000,
):
    """Serve the documentation site locally."""
    ensure_local(_DOCS_ROOT / "docs" / "great_expectations.inv")
    ensure_local(_DOCS_ROOT / "docs" / "polars_patch.inv")

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
