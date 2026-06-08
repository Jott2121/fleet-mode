#!/usr/bin/env python3
"""Guard: the fleet-mode SKILL.md must be discoverable and cover the core gates.

A skill with malformed frontmatter silently fails to load; a skill missing a
'Use when' description won't trigger. This makes those failures loud.
"""
import os
import unittest
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.join(os.path.dirname(HERE), "SKILL.md")  # scripts/../SKILL.md


class TestFleetModeSkill(unittest.TestCase):
    def test_skill_file_exists(self):
        self.assertTrue(os.path.exists(SKILL), f"missing {SKILL}")

    def test_valid_frontmatter(self):
        text = Path(SKILL).read_text()
        self.assertTrue(text.startswith("---\n"),
                        "SKILL.md must open with YAML frontmatter")
        parts = text.split("---\n")
        self.assertGreaterEqual(len(parts), 3,
                                "frontmatter must have opening AND closing ---")
        fm = parts[1]
        self.assertIn("name: fleet-mode", fm)
        self.assertRegex(fm, r"description:\s*Use when",
                         "description must start with 'Use when' so the skill triggers")

    def test_covers_core_gates(self):
        text = Path(SKILL).read_text().lower()
        for token in ("single-threaded", "deterministic", "independent",
                      "receipt", "major"):
            self.assertIn(token, text, f"SKILL.md must cover '{token}'")


if __name__ == "__main__":
    unittest.main(verbosity=2)
