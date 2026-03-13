import subprocess

from hopsworks_docs.scripts.shared.docs_root import _DOCS_ROOT
from hopsworks_docs.scripts.shared.ensure_javadoc import ensure_javadoc
from hopsworks_docs.scripts.shared.ensure_local import ensure_local


def check():
    """Check the documentation."""
    ensure_local(_DOCS_ROOT / "docs" / "great_expectations.inv")
    ensure_local(_DOCS_ROOT / "docs" / "polars_patch.inv")
    ensure_javadoc()

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
