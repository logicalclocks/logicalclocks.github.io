import shutil
import subprocess
from pathlib import Path

from rich import print
from rich.rule import Rule


_DOCS_ROOT = Path(__file__).parent.parent
_NVM_SH = Path.home() / ".nvm" / "nvm.sh"


def _ensure_markdownlint() -> None:
    if shutil.which("markdownlint-cli2"):
        return

    if shutil.which("npm"):
        print("[yellow]Installing markdownlint-cli2...[/yellow]")
        subprocess.run(["npm", "install", "-g", "markdownlint-cli2"], check=True)
        return

    if not _NVM_SH.exists():
        print("[yellow]nvm not found — installing...[/yellow]")
        subprocess.run(
            [
                "bash",
                "-c",
                "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/HEAD/install.sh | bash",
            ],
            check=True,
        )

    print("[yellow]Installing Node.js and markdownlint-cli2 via nvm...[/yellow]")
    subprocess.run(
        [
            "bash",
            "-c",
            f'. "{_NVM_SH}" && nvm install --lts && npm install -g markdownlint-cli2',
        ],
        check=True,
    )


def _run_markdownlint(glob: str, cwd: Path) -> None:
    if shutil.which("markdownlint-cli2"):
        subprocess.run(["markdownlint-cli2", glob], cwd=cwd, check=True)
    else:
        # Installed via nvm — not on PATH in current process, source and run
        subprocess.run(
            ["bash", "-c", f'. "{_NVM_SH}" && markdownlint-cli2 "{glob}"'],
            cwd=cwd,
            check=True,
        )


def lint() -> None:
    """Lint markdown source files."""
    print(Rule("Markdown"))
    _ensure_markdownlint()
    _run_markdownlint("docs/**/*.md", _DOCS_ROOT)
    print("[green]Passed.[/green]")
