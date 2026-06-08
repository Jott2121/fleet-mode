#!/usr/bin/env python3
"""Tests for the Fleet Mode receipt helper. Dependency-free; run directly."""
import os
import shutil
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import append_receipt as ar  # noqa: E402

FIXED = datetime(2026, 5, 30, 18, 0, tzinfo=timezone.utc)


def _rows(text):
    """Data rows: table rows that are neither the header nor the separator."""
    return [ln for ln in text.splitlines()
            if ln.startswith("| ") and ln not in (ar.HEADER, ar.SEP)]


class TestAppendReceipt(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.kl = os.path.join(self.dir, "KILLLOG.md")
        self.addCleanup(shutil.rmtree, self.dir, ignore_errors=True)

    def test_creates_file_with_header_and_row(self):
        ar.append_receipt(self.kl, tried="approach A", verdict="kept",
                          why="passed all checks", metric="tests", value="42/42",
                          task="demo", now=FIXED)
        text = Path(self.kl).read_text()
        self.assertIn(ar.HEADER, text)
        self.assertIn("2026-05-30 18:00", text)
        self.assertIn("approach A", text)
        self.assertEqual(len(_rows(text)), 1)

    def test_append_is_additive(self):
        ar.append_receipt(self.kl, tried="A", verdict="kept", why="ok",
                          metric="steps", value="3", now=FIXED)
        ar.append_receipt(self.kl, tried="B", verdict="killed", why="slower",
                          metric="ms", value="900", now=FIXED)
        text = Path(self.kl).read_text()
        self.assertEqual(text.count(ar.HEADER), 1)   # header written exactly once
        self.assertEqual(len(_rows(text)), 2)

    def test_kill_requires_reason(self):
        with self.assertRaises(ValueError):
            ar.append_receipt(self.kl, tried="C", verdict="killed", why="   ",
                              metric="x", value="1", now=FIXED)

    def test_metric_and_value_required(self):
        with self.assertRaises(ValueError):
            ar.append_receipt(self.kl, tried="C", verdict="kept", why="ok",
                              metric="", value="1", now=FIXED)
        with self.assertRaises(ValueError):
            ar.append_receipt(self.kl, tried="C", verdict="kept", why="ok",
                              metric="tokens", value="", now=FIXED)

    def test_invalid_verdict_rejected(self):
        with self.assertRaises(ValueError):
            ar.append_receipt(self.kl, tried="C", verdict="maybe", why="ok",
                              metric="x", value="1", now=FIXED)

    def test_pipe_is_escaped(self):
        ar.append_receipt(self.kl, tried="a|b", verdict="kept", why="ok",
                          metric="x", value="1", now=FIXED)
        text = Path(self.kl).read_text()
        self.assertIn("a\\|b", text)          # pipe escaped so the table isn't corrupted
        self.assertEqual(len(_rows(text)), 1)

    def test_cli_exits_cleanly_on_invalid_input(self):
        """main() should exit non-zero (argparse error), not dump a traceback."""
        import contextlib
        import io
        argv = ["--killlog", self.kl, "--tried", "x", "--verdict", "kept",
                "--why", "   ", "--metric", "m", "--value", "1"]
        with self.assertRaises(SystemExit) as cm, \
                contextlib.redirect_stderr(io.StringIO()):
            ar.main(argv)
        self.assertNotEqual(cm.exception.code, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
