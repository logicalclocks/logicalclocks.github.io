import typer

from .check import check
from .linkchecker import linkchecker
from .markdownlint import markdownlint
from .serve import serve
from .snakeoil import snakeoil


cli = typer.Typer(no_args_is_help=True)

cli.command()(check)
cli.command()(serve)
cli.command()(markdownlint)
cli.command()(linkchecker)
cli.command()(snakeoil)
