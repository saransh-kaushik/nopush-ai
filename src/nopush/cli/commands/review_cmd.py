"""``nopush review`` — run an AI-powered code review."""

from __future__ import annotations

import typer
from rich.console import Console

console = Console()


def review_callback() -> None:
    """Analyze staged Git changes and display AI-powered review suggestions.

    This is the main command of NoPush. It reads staged diffs, sends them
    to the configured LLM provider, and renders structured feedback in the
    terminal.
    """
    console.print(
        "\n[bold cyan]nopush review[/bold cyan] — AI code review\n"
        "[dim]This will be implemented in Steps 3–7.[/dim]\n"
    )
    raise typer.Exit()
