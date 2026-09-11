import typer

from .check import check
from .gen_config_vars import gen_config_vars
from .helm_values import gen_helm_values
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
cli.command()(gen_helm_values)
cli.command()(gen_config_vars)
