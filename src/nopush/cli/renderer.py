"""Rich-based terminal rendering for review results."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

if TYPE_CHECKING:
    from nopush.review.models import ReviewResult

# ---------------------------------------------------------------------------
# Severity styling
# ---------------------------------------------------------------------------

_SEVERITY_STYLES: dict[str, tuple[str, str]] = {
    "critical": ("bold red", "🔴"),
    "warning": ("bold yellow", "🟡"),
    "suggestion": ("bold blue", "🔵"),
    "nitpick": ("dim", "⚪"),
}


class ReviewRenderer:
    """Formats and renders :class:`ReviewResult` objects to the terminal."""

    def __init__(self, console: Console | None = None) -> None:
        self.console = console or Console()

    def render(self, result: "ReviewResult") -> None:
        """Render a full review result to the console.

        Implementation will be completed in Step 7.
        """
        raise NotImplementedError("ReviewRenderer.render() — coming in Step 7")

    # ------------------------------------------------------------------
    # Helpers (to be fleshed out)
    # ------------------------------------------------------------------

    def _render_summary(self, result: "ReviewResult") -> Panel:
        """Render a summary panel with issue counts by severity."""
        raise NotImplementedError

    def _render_comment(self, comment: object) -> Panel:
        """Render a single review comment."""
        raise NotImplementedError
