# Evidence

## The -3.5% multi-agent figure

SKILL.md states: "Mean multi-agent gain across tasks is -3.5%."

**Source: internal Fleet Mode task set, 2026-06.** The figure comes from the Fleet
Mode QC runs on the [bow](https://github.com/Jott2121/bow) build: a set of real build
tasks (code changes, reviews, research) executed both as a single strong agent and as
a multi-agent fan-out, scored on task success and rework required. Averaged across the
set, adding agents produced a net -3.5% change versus the single-agent baseline. Gains
concentrated in read-heavy parallelizable work; losses concentrated in parallel writes
and self-graded review.

This is an internal measurement, not a published benchmark. n is small and the task
mix reflects one project's workload. Treat the sign and the shape of the result
(fan-out pays only for reading; parallel writes lose) as the takeaway, not the exact
magnitude. A fuller writeup with the task list and per-task numbers is planned; until
then, re-derive the number on your own task set before relying on it.
