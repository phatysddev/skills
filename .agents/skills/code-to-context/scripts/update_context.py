#!/usr/bin/env python3
"""Safely create or replace the generated Codebase Context block in CONTEXT.md."""

from __future__ import annotations

import argparse
import json
import os
import stat
import tempfile
from pathlib import Path

HEADING = "## Codebase Context"
START = "<!-- phat:code-to-context:start -->"
END = "<!-- phat:code-to-context:end -->"


class ContextUpdateError(ValueError):
    """Raised when generated input is invalid."""


def _heading_positions(text: str) -> list[int]:
    """Return offsets for actual Markdown Codebase Context heading lines."""
    positions: list[int] = []
    offset = 0
    for line in text.splitlines(keepends=True):
        if line.rstrip("\r\n") == HEADING:
            positions.append(offset)
        offset += len(line)
    return positions


def _result(action: str, context: Path, reason: str | None = None) -> dict[str, str]:
    payload = {"action": action, "context": str(context)}
    if reason:
        payload["reason"] = reason
    return payload


def _validate_generated_block(block: str) -> str:
    """Validate and normalize the generated canonical block."""
    normalized = block.replace("\r\n", "\n").replace("\r", "\n").strip("\n")

    if len(_heading_positions(normalized)) != 1:
        raise ContextUpdateError("generated block must contain exactly one '## Codebase Context' heading")
    if normalized.count(START) != 1 or normalized.count(END) != 1:
        raise ContextUpdateError("generated block must contain exactly one start marker and one end marker")

    heading_pos = normalized.find(HEADING)
    start_pos = normalized.find(START)
    end_pos = normalized.find(END)

    if not (heading_pos < start_pos < end_pos):
        raise ContextUpdateError("generated block heading and markers are out of order")

    if normalized[:heading_pos].strip():
        raise ContextUpdateError("generated block must begin with the Codebase Context heading")

    between_heading_and_start = normalized[heading_pos + len(HEADING):start_pos]
    if between_heading_and_start.strip():
        raise ContextUpdateError("only whitespace may appear between the Codebase Context heading and start marker")

    if normalized[end_pos + len(END):].strip():
        raise ContextUpdateError("generated block must end with the end marker")

    return normalized


def _atomic_write(path: Path, content: str, original_mode: int | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(content.encode("utf-8"))
        if original_mode is not None:
            os.chmod(temp_path, stat.S_IMODE(original_mode))
        os.replace(temp_path, path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def _compose_update(existing: str | None, block: str) -> tuple[str | None, str, str | None]:
    """Return (new_text, action, reason). new_text None means refuse to write."""
    if existing is None:
        return f"# Repository context\n\n{block}\n", "created", None

    start_count = existing.count(START)
    end_count = existing.count(END)
    heading_positions = _heading_positions(existing)
    heading_count = len(heading_positions)

    if start_count == 0 and end_count == 0:
        if heading_count:
            return None, "not written", "unmarked '## Codebase Context' exists and is treated as human-authored"

        separator = "" if existing == "" else ("\n" if existing.endswith("\n") else "\n\n")
        return f"{existing}{separator}{block}\n", "generated block appended", None

    if start_count != 1 or end_count != 1:
        return None, "not written", "malformed or ambiguous boundary markers"

    start_pos = existing.find(START)
    end_pos = existing.find(END)
    if start_pos >= end_pos:
        return None, "not written", "boundary markers are reversed or malformed"

    if heading_count != 1:
        return None, "not written", "expected exactly one Codebase Context heading for the marked block"

    heading_pos = heading_positions[0]
    if heading_pos > start_pos:
        return None, "not written", "Codebase Context heading is not attached to the generated block"

    between_heading_and_start = existing[heading_pos + len(HEADING):start_pos]
    if between_heading_and_start.strip():
        return None, "not written", "unexpected content appears between Codebase Context heading and start marker"

    replacement_end = end_pos + len(END)
    prefix = existing[:heading_pos]
    suffix = existing[replacement_end:]
    return f"{prefix}{block}{suffix}", "generated block replaced", None


def update_context(context_path: Path, generated_block_path: Path, dry_run: bool = False) -> dict[str, str]:
    block = _validate_generated_block(generated_block_path.read_text(encoding="utf-8"))

    existing: str | None
    original_mode: int | None = None
    if context_path.exists():
        if not context_path.is_file():
            return _result("not written", context_path, "context path exists but is not a regular file")
        existing = context_path.read_bytes().decode("utf-8")
        original_mode = context_path.stat().st_mode
    else:
        existing = None

    new_text, action, reason = _compose_update(existing, block)
    if new_text is None:
        return _result(action, context_path, reason)

    if not dry_run:
        _atomic_write(context_path, new_text, original_mode)

    payload = _result(action, context_path)
    if dry_run:
        payload["dry_run"] = "true"
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Safely create or replace the generated Codebase Context block in CONTEXT.md."
    )
    parser.add_argument(
        "--context",
        default="CONTEXT.md",
        help="Path to CONTEXT.md (default: CONTEXT.md)",
    )
    parser.add_argument(
        "--generated-block",
        required=True,
        help="Path to a generated Markdown file containing the complete canonical Codebase Context block",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and report the action without writing CONTEXT.md",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    context_path = Path(args.context)
    generated_block_path = Path(args.generated_block)

    if not generated_block_path.is_file():
        print(json.dumps(_result("not written", context_path, "generated block file does not exist"), ensure_ascii=False))
        return 2

    try:
        result = update_context(context_path, generated_block_path, dry_run=args.dry_run)
    except (ContextUpdateError, UnicodeError, OSError) as exc:
        print(json.dumps(_result("not written", context_path, str(exc)), ensure_ascii=False))
        return 2

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
