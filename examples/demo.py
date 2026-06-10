"""
Fleet Mode receipt demo — shows append_receipt.py logging real decisions to KILLLOG.md.

Run: python3 examples/demo.py
"""

import sys
import os
import time
import tempfile
import subprocess

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from append_receipt import append_receipt

SEP = "-" * 62

tmp = tempfile.mktemp(suffix=".md")

decisions = [
    dict(
        task="fan-out 10 parallel writer agents",
        tried="parallel subagents each editing different files",
        verdict="killed",
        why="writes stayed single-threaded per Fleet Mode doctrine; parallel writers caused silent merge conflicts",
        metric="merge-conflicts",
        value=3,
    ),
    dict(
        task="independent review of auth middleware rewrite",
        tried="same agent reviewed its own output",
        verdict="rejected",
        why="self-grading; reviewer must be a separate clean-context agent with no memory of the write",
        metric="self-review-bias",
        value=1,
    ),
    dict(
        task="model routing: cheapest sufficient model per call",
        tried="route chat to haiku, deep-work to fable, builds to fable@xhigh",
        verdict="adopted",
        why="premium burns weekly limit 4x faster; routing cuts cost without quality loss on routine calls",
        metric="cost-reduction-pct",
        value=62,
    ),
]

print(SEP)
print("Fleet Mode — logging honest receipts for every kept/killed decision")
print(SEP)

for d in decisions:
    row = append_receipt(tmp, **d)
    print(f"\n  verdict : {d['verdict'].upper()}")
    print(f"  task    : {d['task']}")
    print(f"  why     : {d['why'][:60]}...")
    print(f"  metric  : {d['metric']} = {d['value']}")
    time.sleep(1.5)

print()
print(SEP)
print("KILLLOG.md (last 4 lines):")
print(SEP)
with open(tmp) as f:
    lines = f.readlines()
for line in lines[-4:]:
    print(line.rstrip())

os.unlink(tmp)
print()
print("Receipts over hype.")
