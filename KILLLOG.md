# Kill Log: Fleet Mode receipts

Append-only. Every kept/killed decision with the real number. Sample rows below show
the format written by `scripts/append_receipt.py`.

| when (UTC) | task | tried | verdict | why | metric | value |
|---|---|---|---|---|---|---|
| 2026-06-02 14:11 | add retry to uploader | exponential backoff with jitter | kept | cut timeout errors to zero in a 200-run soak | errors | 0 |
| 2026-06-05 09:47 | speed up PR review | 4-way parallel reviewer fan-out | killed | duplicated findings and missed the one real bug a single reviewer caught | unique_findings | 3 vs 5 |
| 2026-06-08 20:30 | nightly backup job | rsync to offsite branch plus 14d local retention | adopted | restore drill recovered full state in under a minute | restore_seconds | 52 |
