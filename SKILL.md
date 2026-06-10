---
name: fleet-mode
description: Use when implementing any non-trivial or irreversible change in this project. Fan out subagents ONLY for read-heavy parallel work, keep writes single-threaded, gate work through deterministic checks then an independent reviewer before shipping, human-gate MAJOR/irreversible acts, and log an honest receipt. Pilot of the default multi-agent operating mode.
---

# Fleet Mode (inline ship-gate)

Evaluate without prejudice; adopt only on measured proof. Receipts over hype.

## When this applies
Any non-trivial or irreversible change. Trivial/mechanical edits (typo, rename,
one-liner, doc tweak) skip the fleet and get a fast single-pass check.

## Dependencies
Steps 2 and 4 reference `superpowers:*` skills. If superpowers skills are
unavailable, substitute: fan-out decisions manually, run tests before any model
review, get a colleague to review independently.

## The gate (run in order)

1. **Classify stakes.** trivial: light check, ship. non-trivial: full gate below.
   irreversible/MAJOR: full gate plus human approval before acting.

2. **Decide fan-out (bias-to-NO on agents).** Use a single strong agent by default.
   Fan out parallel subagents (via `superpowers:dispatching-parallel-agents`) ONLY
   for read-heavy, parallelizable work that exceeds one context window: research,
   codebase/PR review, multi-file audits. NEVER fan out to edit code in parallel.
   Subagents explore in clean contexts and return condensed summaries of roughly
   1-2k tokens each.

3. **Write single-threaded.** One agent makes the edit. No parallel writers
   (map-reduce-and-manage: extra agents add intelligence, not parallel actions).

4. **QC gate, deterministic first.** Run objective checks that need no model:
   tests, types, lint, build, and re-derive any numbers. Only if they pass, run an
   **independent** review that tries to REFUTE the work: a separate clean-context
   reviewer (`superpowers:requesting-code-review` / `superpowers:verification-before-completion`).
   For high-stakes/irreversible/published output, escalate to a different-model judge.
   No agent grades its own work. Fail closed.

5. **Human-gate MAJOR items only.** A change is MAJOR if ANY of: hard to reverse;
   changes a core default/rule or the operating mode itself; affects many projects;
   materially shifts cost, quality, or safety; force-push/deploy/real-money-trade/
   mass-delete/send/post; or adds a new external dependency/spend. MAJOR: propose
   and wait for the human. Minor reversible: proceed and log a receipt.

6. **Log a receipt.** For each kept/killed decision append a row with the real number
   (`--verdict` is one of: kept, killed, adopted, rejected):

   ```bash
   python3 ~/.claude/skills/fleet-mode/scripts/append_receipt.py \
     --task "<task>" --tried "<what>" --verdict kept \
     --why "<why>" --metric <label> --value <n>
   ```

   *(Installed globally at `~/.claude/skills/fleet-mode/`; the receipt defaults to `KILLLOG.md` in the current repo. Pass `--killlog <path>` to target a specific ledger.)*

## Red flags (STOP: you're cutting the corner)
| Thought | Reality |
|---|---|
| "I'll fan out agents to write this faster" | Writes stay single-threaded. Fan-out is for reading, not editing. |
| "More agents = better" | Mean multi-agent gain across tasks is -3.5% (Source: internal Fleet Mode task set, 2026-06; see docs/EVIDENCE.md). Scale to the task; default single. |
| "The reviewer can be the author" | No self-grading. The reviewer must be independent. |
| "It's basically reversible" | If unsure whether it's MAJOR, treat it as MAJOR and ask. |
| "No number handy for the receipt" | Then you haven't measured it. Get the number or it didn't earn 'kept'. |
