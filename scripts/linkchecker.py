import subprocess
import time
import urllib.request
from urllib.error import URLError

from hopsworks_docs.scripts.shared.docs_root import _DOCS_ROOT
from hopsworks_docs.scripts.shared.ensure_javadoc import ensure_javadoc
from hopsworks_docs.scripts.shared.ensure_local import ensure_local
from rich import print
from rich.rule import Rule


def linkchecker():
    """Build and check links in the documentation site."""
    ensure_local(_DOCS_ROOT / "docs" / "great_expectations.inv")
    ensure_local(_DOCS_ROOT / "docs" / "polars_patch.inv")
    ensure_javadoc()

    server = subprocess.Popen(
        ["mkdocs", "serve", "-q", "-f", str(_DOCS_ROOT / "mkdocs.yml")],
    )
    try:
        for _ in range(120):
            try:
                urllib.request.urlopen("http://127.0.0.1:8000/")
                break
            except URLError:
                time.sleep(1)

        print(Rule("Links"))
        subprocess.run(
            [
                "linkchecker",
                "--no-warnings",
                "--no-status",
                "http://127.0.0.1:8000/",
                "--ignore-url",
                "http://127.0.0.1:8000/javadoc/resources/fonts/dejavu.css",
            ],
            check=True,
        )
        print("[green]Links OK.[/green]")
    finally:
        server.kill()
        server.wait()
