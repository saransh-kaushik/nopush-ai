"""``nopush init`` — interactive first-time setup."""

from __future__ import annotations

import typer
from rich.console import Console

console = Console()


def init_callback() -> None:
    """Walk the user through first-time NoPush configuration.

    This command collects the AI provider, API key, and preferred model,
    then persists them to ``~/.nopush/credentials.yaml``.
    """
    console.print(
        "\n[bold cyan]nopush init[/bold cyan] — first-time setup\n"
        "[dim]This will be implemented in Step 2 (BYOK Support).[/dim]\n"
    )
    raise typer.Exit()
