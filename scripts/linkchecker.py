import subprocess
from pathlib import Path

from rich import print
from rich.rule import Rule


_DOCS_ROOT = Path(__file__).parent.parent


def linkcheck():
    """Build and check links in the documentation site."""
    subprocess.run(
        ["mkdocs", "build", "-f", str(_DOCS_ROOT / "mkdocs.yml")],
        check=True,
    )
    print(Rule("Links"))
    subprocess.run(
        ["linkchecker", "--no-warnings", (_DOCS_ROOT / "site").as_uri()],
        check=True,
    )
    print("[green]Links OK.[/green]")
