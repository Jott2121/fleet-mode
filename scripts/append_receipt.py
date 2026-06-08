#!/usr/bin/env python3
"""Append-only honest receipts for Fleet Mode.

One row per kept/killed decision: what was tried, the verdict, WHY, and the real
number. Append-only by construction (never rewrites existing rows). Mirrors the
Kill Log engine's "kill_reason required + numbers are real" invariant, kept tiny
and dependency-free so the skill is portable (copy the dir to ~/.claude later).
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

HEADER = "| when (UTC) | task | tried | verdict | why | metric | value |"
SEP = "|---|---|---|---|---|---|---|"
VALID_VERDICTS = ("kept", "killed", "adopted", "rejected")


def _esc(s) -> str:
    """Keep a value inside one table cell: no raw pipes or newlines."""
    return (str(s).replace("\\", "\\\\").replace("|", "\\|")
            .replace("\r", " ").replace("\n", " ").strip())


def append_receipt(killlog_path, *, tried, verdict, why, metric, value,
                   task="", now=None) -> str:
    """Append one receipt row to killlog_path and return the row text.

    Raises ValueError if the verdict is unknown or any honesty-required field
    (why / metric / value) is blank. `now` is injectable for deterministic tests.
    """
    if verdict not in VALID_VERDICTS:
        raise ValueError(f"verdict must be one of {VALID_VERDICTS}, got {verdict!r}")
    if not str(why).strip():
        raise ValueError("why is required (no empty kill/keep reason)")
    if not str(metric).strip():
        raise ValueError("metric is required (the real-number label: tokens/steps/tests/ms/$)")
    if str(value).strip() == "":
        raise ValueError("value is required (the real number or measured note)")

    when = (now or datetime.now(timezone.utc)).strftime("%Y-%m-%d %H:%M")
    cells = (when, task, tried, verdict, why, metric, value)
    row = "| " + " | ".join(_esc(c) for c in cells) + " |"

    path = Path(killlog_path)
    if not path.exists() or path.stat().st_size == 0:
        path.write_text(
            "# Kill Log — Fleet Mode receipts\n\n"
            "Append-only. Every kept/killed decision with the real number.\n\n"
            f"{HEADER}\n{SEP}\n{row}\n"
        )
        return row

    text = path.read_text()
    pad = "" if text.endswith("\n") else "\n"
    if HEADER in text:
        path.write_text(text + pad + row + "\n")
    else:  # file exists but has no table yet — start one
        path.write_text(text + pad + f"\n{HEADER}\n{SEP}\n{row}\n")
    return row


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Append a Fleet Mode receipt to KILLLOG.md")
    p.add_argument("--killlog", default="KILLLOG.md")
    p.add_argument("--task", default="")
    p.add_argument("--tried", required=True)
    p.add_argument("--verdict", required=True, choices=VALID_VERDICTS)
    p.add_argument("--why", required=True)
    p.add_argument("--metric", required=True)
    p.add_argument("--value", required=True)
    a = p.parse_args(argv)
    try:
        row = append_receipt(a.killlog, tried=a.tried, verdict=a.verdict, why=a.why,
                             metric=a.metric, value=a.value, task=a.task)
    except ValueError as e:
        p.error(str(e))  # prints "usage... error: <msg>" to stderr, exits 2
    print(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
