"""Assemble LLM messages from diffs and configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from nopush.providers.base import Message
from nopush.prompts.templates import (
    DEPTH_PROMPTS,
    FILE_DIFF_TEMPLATE,
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE,
)

if TYPE_CHECKING:
    from nopush.git.models import FileDiff

# ---------------------------------------------------------------------------
# Rough token estimation (4 chars ≈ 1 token)
# ---------------------------------------------------------------------------

_CHARS_PER_TOKEN = 4
_DEFAULT_MAX_TOKENS = 120_000  # Conservative limit for most models


class PromptBuilder:
    """Builds the message list for an LLM code review request.

    Attributes
    ----------
    max_input_tokens:
        Approximate maximum input tokens. Diffs exceeding this are chunked.
    review_depth:
        One of ``minimal``, ``standard``, or ``thorough``.
    """

    def __init__(
        self,
        review_depth: str = "standard",
        max_input_tokens: int = _DEFAULT_MAX_TOKENS,
    ) -> None:
        self.review_depth = review_depth
        self.max_input_tokens = max_input_tokens

    def build(self, file_diffs: list["FileDiff"]) -> list[list[Message]]:
        """Build one or more message lists from a set of file diffs.

        Returns a list of message lists. Each inner list is a self-contained
        prompt that fits within the token budget. In the common case there is
        only one inner list.
        """
        if not file_diffs:
            return []

        system_message = self._build_system_message()
        diff_blocks = [self._format_file_diff(fd) for fd in file_diffs]

        # Chunk diff blocks to fit within the token budget
        chunks = self._chunk_blocks(diff_blocks, system_message)
        return chunks

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_system_message(self) -> Message:
        """Construct the system message with depth modifier."""
        depth_instruction = DEPTH_PROMPTS.get(self.review_depth, DEPTH_PROMPTS["standard"])
        content = f"{SYSTEM_PROMPT}\n\n## Review Depth\n\n{depth_instruction}"
        return Message(role="system", content=content)

    @staticmethod
    def _format_file_diff(file_diff: "FileDiff") -> str:
        """Format a single FileDiff into a prompt-ready string."""
        # Reconstruct the raw diff lines from hunks
        diff_lines: list[str] = []
        for hunk in file_diff.hunks:
            diff_lines.append(
                f"@@ -{hunk.old_start},{hunk.old_count} "
                f"+{hunk.new_start},{hunk.new_count} @@ {hunk.header}"
            )
            for line in hunk.lines:
                if line.change_type.value == "added":
                    diff_lines.append(f"+{line.content}")
                elif line.change_type.value == "removed":
                    diff_lines.append(f"-{line.content}")
                else:
                    diff_lines.append(f" {line.content}")

        return FILE_DIFF_TEMPLATE.format(
            file_path=file_diff.path,
            language=file_diff.language or "unknown",
            status=file_diff.status.value,
            diff_content="\n".join(diff_lines),
        )

    def _chunk_blocks(
        self, diff_blocks: list[str], system_message: Message
    ) -> list[list[Message]]:
        """Split diff blocks into chunks that fit the token budget."""
        system_tokens = self._estimate_tokens(system_message.content)
        budget = self.max_input_tokens - system_tokens

        chunks: list[list[Message]] = []
        current_blocks: list[str] = []
        current_tokens = 0

        for block in diff_blocks:
            block_tokens = self._estimate_tokens(block)

            if current_tokens + block_tokens > budget and current_blocks:
                # Flush current chunk
                user_content = USER_PROMPT_TEMPLATE.format(
                    file_diffs="\n".join(current_blocks)
                )
                chunks.append([system_message, Message(role="user", content=user_content)])
                current_blocks = []
                current_tokens = 0

            current_blocks.append(block)
            current_tokens += block_tokens

        # Flush remaining
        if current_blocks:
            user_content = USER_PROMPT_TEMPLATE.format(
                file_diffs="\n".join(current_blocks)
            )
            chunks.append([system_message, Message(role="user", content=user_content)])

        return chunks

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        """Rough token estimate: 1 token ≈ 4 characters."""
        return len(text) // _CHARS_PER_TOKEN
