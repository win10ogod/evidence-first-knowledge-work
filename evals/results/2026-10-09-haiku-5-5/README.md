# Benchmark: Haiku 5.5, 2026-10-09

The four prompts in [evals.json](../../evals.json) were each run with three configurations, two runs per cell, giving 24 runs. Every run used `claude-haiku-5-5` (model ID confirmed from the transcripts) as a fresh subagent with the same tools.

- **v2.0**: told to read and follow this repository's SKILL.md at commit `59cf0ee`.
- **v1.1**: told to read and follow SKILL.md at commit `e0784a6`.
- **no skill**: the same task with no skill.

Each run worked in its own copy of `fixtures/exporter`, in a directory with a random name so the condition was not visible. Process expectations were graded from the actual tool-call transcripts. Eval 1 was also checked with `acceptance/exporter_acceptance.py`. Per-run detail is in [runs.json](runs.json), and the aggregate is in [benchmark.json](benchmark.json).

## Results

| Eval | v2.0 pass | v1.1 pass | No-skill pass | v2.0 tokens | v1.1 tokens | No-skill tokens |
| --- | --- | --- | --- | --- | --- | --- |
| 1 Exporter integration | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 73.8k / 78.5k | 81.5k / 85.3k | 55.2k / 57.2k |
| 2 Analysis only | 1.00 / 1.00 | 0.75 / 1.00 | 0.75 / 0.75 | 63.4k / 58.8k | 71.0k / 71.5k | 48.7k / 47.6k |
| 3 unittest exit code | 1.00 / 1.00 | 1.00 / 0.75 | 0.75 / 1.00 | 65.0k / 61.3k | 74.6k / 70.0k | 58.4k / 57.5k |
| 4 "Trivial" rename | 1.00 / 1.00 | 1.00 / 1.00 | 0.50 / 0.50 | 61.3k / 58.3k | 70.2k / 67.7k | 47.2k / 49.0k |
| **Mean** | **1.00 ± 0.00** | **0.94 ± 0.11** | **0.78 ± 0.20** | **65.0k** | **74.0k** | **52.6k** |

| | v2.0 | v1.1 | No skill |
| --- | --- | --- | --- |
| Mean wall time | 47.7 s | 57.2 s | 34.5 s |
| Mean tool calls | 16.0 | 24.6 | 10.8 |
| Runs that left `__pycache__` in the project (of 6) | 2 | 2 | 6 |
| Unrequested `docs/formats.md` edit in eval 1 (of 2) | 1 | 2 | 1 |

## Findings

- **Where a skill helps:** in eval 4 (a "trivial" rename), both no-skill runs skipped re-reading the edited file, and neither used the project's documented test runner; one ran no tests at all. All four skill runs did both. In eval 2, both no-skill runs left `__pycache__` in a project the user had asked not to change.
- **v2.0 compared with v1.1:** the same or better on every eval, at 12% fewer tokens, 17% less wall time and 35% fewer tool calls. The pass-rate difference comes down to two assertion outcomes, which is not statistically meaningful at n=2.
- **Ceiling effect:** in eval 1, every configuration passed every assertion and the acceptance script. Haiku 5.5 solves this fixture without help, so a harder fixture is needed to measure integration skill.
- **Not prevented by either version:** unrequested edits to `docs/formats.md` (marking `lines` as supported) in eval 1. This is a candidate rule for the next revision.
- **Research quality varies by run, not by condition:** the best-sourced eval 3 answer came from a no-skill run, which cited the 3.12.0b1 NEWS entry. One v1.1 run found that the skip condition changed between 3.12.1 and 3.12.3. Both claims were checked against CPython tags.

## Limitations

- Two runs per cell. Treat the differences as directional.
- The grader also wrote v2.0, and grading was not blind. Six expectations were judged by hand; their evidence strings are in `runs.json`.
- The eval 2 "no modifications" expectation counts a leftover `__pycache__` as a change, which is a strict reading.
- The skill was supplied by telling the agent to read SKILL.md, not through the host's automatic skill triggering, so description triggering was not measured here.
