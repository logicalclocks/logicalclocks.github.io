import re
import subprocess

from hopsworks_docs.scripts.shared.docs_root import _DOCS_ROOT
from rich import print
from rich.rule import Rule


_DOCS = _DOCS_ROOT / "docs"
_PY_LANGS = ["python", "py", "Python", "python3", "py3"]
_FENCE_PAT = re.compile(
    r"([ \t]*)(```(?:"
    + "|".join(_PY_LANGS)
    + r"| "
    + r"| ".join(_PY_LANGS)
    + r")(?:[^\n]*)\n)(.*?)([ \t]*```)",
    re.DOTALL,
)


def _strip_trailing_blank(m: re.Match) -> str:
    body = m.group(3).rstrip("\n") + "\n"
    return m.group(1) + m.group(2) + body + m.group(4)


def snakeoil():
    """Run snakeoil to check Python code blocks in Markdown files."""
    print(Rule("Snakeoil"))
    subprocess.run(
        [
            "snakeoil",
            "--line-length",
            "88",
            "--rules",
            "E,F,B,C4,ISC,PIE,PYI,Q,RSE,RET,SIM,TC,I,W,D2,D3,D4,INP,UP,FA",
            str(_DOCS),
        ],
        check=True,
    )

    for path in _DOCS.rglob("*.md"):
        original = path.read_text()
        fixed = _FENCE_PAT.sub(_strip_trailing_blank, original)
        if fixed != original:
            path.write_text(fixed)

    subprocess.run(["git", "diff", "--exit-code"], check=True)
    print(Rule("All checks passed", style="green"))
