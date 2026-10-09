# Benchmark: v2.2 vs v2.1 vs no skill, and activation (Haiku 5.5, 2026-10-09)

Two questions:

1. Does v2.2 behave better once it is loaded?
2. Does it actually get loaded in real use?

Every run used `claude-haiku-5-5`.

## 1. Behavior when loaded (36 runs)

Evals 1, 2, 4 and 5 from [evals.json](../../evals.json), with 3 runs per configuration. Eval 3 (research) was skipped because v2.2 did not change the research guidance. The configurations were v2.2 (`1544217`), v2.1 (`bbccd96`) and no skill. Each run worked in a fixture copy in a directory with a random name. Grading was mechanical, using the same fixed rules as the v2.1 round. Residue was snapshotted before any acceptance script ran, and grading was repeated twice with identical results.

| Eval | v2.2 | v2.1 | No skill |
| --- | --- | --- | --- |
| 1 Exporter integration | 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 | 0.78 / 0.89 / 0.78 |
| 2 Analysis only | 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 | 0.75 / 0.75 / 0.75 |
| 4 "Trivial" rename | 1.00 / 1.00 / 1.00 | 0.80 / 1.00 / 1.00 | 0.60 / 0.80 / 0.60 |
| 5 Python 3.11 batching (target hidden) | 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 | 0.83 / 0.67 / 1.00 |
| **Mean** | **1.000** | **0.983** | **0.766** |
| Tokens / run | 63.5k | 63.7k | 50.8k |
| Wall time / run | 48.1 s | 47.4 s | 23.7 s |
| Left `__pycache__` (of 12) | 0 | 0 | 10 |
| Unrequested `docs/formats.md` edit (of 3) | 0 | 0 | 3 |

- **v2.2 fixed the remaining miss.** For the second round in a row, v2.1 skipped re-reading the file after the eval-4 edit once. v2.2 did so in all 3 runs, at the same token cost.
- **The hidden-target trap still did not trigger.** With the Python 3.11 target only in `pyproject.toml`, the CI workflow and the Dockerfile, and the spec naming `itertools.batched`, no run in any configuration used `batched`. Haiku 5.5 knows the API is 3.12+ and checks `requires-python`. What separates the configurations is whether tests were then run on 3.11: one no-skill run tested only on 3.13.
- **The skill's added value at this point is discipline, not knowledge.** The no-skill runs fail on residue (10/12), unrequested doc edits (3/3), skipped test runs and skipped post-edit reads. They do not fail on API knowledge. Both skill versions now cost about 25% more tokens and twice the wall time.

## 2. Activation in real use

Data: [triggering.json](triggering.json). The harness is skill-creator's `run_eval` / `run_loop` (`claude -p`, Claude Code 2.1.295), run against the 20 queries in [trigger-queries.json](../../trigger-queries.json).

| Setup | Should-trigger loaded | Should-not-trigger loaded |
| --- | --- | --- |
| Current description, 3 runs per query | 1 / 30 | 0 / 30 |
| Description optimization loop, 5 rounds, 60/40 train/held-out split | Held-out recall 0% in every round; best description = original | 0% |
| Deliberately forceful description ("Required first step for ANY request…") | Haiku 2/10, Opus 2/10 | — |
| Skill in `.claude/skills/`, **no** project snippet | 1 / 20 | — |
| Skill in `.claude/skills/` **plus** `project-instructions.snippet.md` as `CLAUDE.md` | **20 / 20** | **0 / 10** |

- **Descriptions alone do not activate this skill.** For tasks the model believes it can handle directly (coding, config, debugging), neither Haiku nor Opus chose to load a general working-method skill from its description. That held for every wording tried, including forceful ones. This matches the skill-authoring guidance that Claude consults skills mainly for tasks it cannot easily handle alone.
- **The project snippet is what activates it.** With the snippet in `CLAUDE.md`, Haiku loaded the skill on every engineering query and on none of the non-engineering ones. The installation instructions now treat the snippet as required, not optional.
- The description is kept unchanged. No rewrite beat it on held-out queries, and its precision is 100%.

## Limitations

- Three runs per behavioral cell, and the grading rules were written by the skill's author.
- Trigger tests ran on single-turn `claude -p` prompts in an empty project. Multi-turn sessions or real repositories may differ.
- The snippet test checks only whether the skill was loaded, not how well it was then followed. Section 1 covers behavior once loaded.
