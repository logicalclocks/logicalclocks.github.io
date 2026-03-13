from rich import print
from rich.rule import Rule

from .linkchecker import linkcheck
from .markdownlint import lint


def snakeoil():
    """Run all quality checks: lint, linkcheck."""
    print(Rule("Snakeoil"))
    lint()
    linkcheck()
    print(Rule("All checks passed", style="green"))
