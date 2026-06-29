"""Top-level Typer application and command registration."""

from __future__ import annotations

import typer

from nopush import __version__
from nopush.cli.commands.init_cmd import init_callback
from nopush.cli.commands.review_cmd import review_callback

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = typer.Typer(
    name="nopush",
    help="NoPush — AI-powered local code review assistant.",
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode="rich",
)


# ---------------------------------------------------------------------------
# Version callback
# ---------------------------------------------------------------------------


def _version_callback(value: bool) -> None:
    """Print the current version and exit."""
    if value:
        typer.echo(f"nopush {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show the installed version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
) -> None:
    """NoPush — AI-powered local code review assistant."""


# ---------------------------------------------------------------------------
# Register commands
# ---------------------------------------------------------------------------

app.command(name="init", help="Configure your API key and preferred model.")(init_callback)
app.command(name="review", help="Review staged Git changes using AI.")(review_callback)
