import typer

from .check import check
from .linkchecker import linkcheck
from .markdownlint import lint
from .serve import serve
from .snakeoil import snakeoil


cli = typer.Typer(no_args_is_help=True)

cli.command()(check)
cli.command()(serve)
cli.command()(lint)
cli.command()(linkcheck)
cli.command()(snakeoil)
