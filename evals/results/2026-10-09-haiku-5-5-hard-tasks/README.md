# Hard tasks: can Haiku 5.5 be made to fail? (2026-10-09)

Goal: find multi-step debugging and cross-file integration tasks that Haiku 5.5 fails on its own, then see whether skill v2.2 changes the outcome. Three rounds, each harder than the last, with 3 runs per configuration (v2.2 or no skill) per eval: 54 runs in all, all on `claude-haiku-5-5`. Per-run data is in [runs.json](runs.json).

Setup was the same as the earlier benchmarks. Each run got a fixture copy in a randomly named directory, no git, and no package installs. Grading was mechanical. Residue was snapshotted first, then the evaluator-owned acceptance script ran against the final copy with `-B` and `PYTHONDONTWRITEBYTECODE=1`. Each acceptance script reruns the pristine tests against the candidate code. Fixtures, traps and acceptance scripts are described in [evals/README.md](../../README.md#hard-task-fixtures-evals-6-13).

## Results

| Round | Eval | What is hidden | v2.2 pass | No skill pass |
| --- | --- | --- | --- | --- |
| 1 | 6 billing | Float parse **and** per-line half-up rounding | 3/3 | 3/3 |
| 1 | 7 fetcher | Option through the config chain, s->ms, two client sites | 3/3 | 2/3 |
| 1 | 8 pricing | Order-dependent failure from a mutated `lru_cache` table | 3/3 | 3/3 |
| 2 | 9 scheduler | DST gaps and folds in any zone (Lord Howe, Santiago) | 3/3 | 3/3 |
| 2 | 10 sessions | Boundary bug visible; offsets and string sort hidden | **0/3** | **0/3** |
| 2 | 11 notifier | Vendored docstring says seconds, code says ms | 3/3 | 3/3 |
| 3 | 10b sessions, scoped prompt | Same fixture, prompt asks for spec conformance | 3/3 | 3/3 |
| 3 | 12 versions | Long range spec, answers from npm `semver` 7.6.0 (77 cases + 783-pair grid) | 3/3 | 3/3 |
| 3 | 13 inventory | Model, storage format bump, CLI exit code, CSV, list, two money paths | 3/3 | 3/3 |
| | **Total** | | **24/27** | **23/27** |

| Per run (mean) | v2.2 | No skill |
| --- | --- | --- |
| Left `__pycache__` in the project | 0 / 27 | 19 / 27 |
| Unrequested `docs/config.md` edit (eval 7) | 0 / 3 | 3 / 3 |
| Tokens, rounds 1 / 2 / 3 | 74k / 74k / 95k | 56k / 59k / 76k |
| Wall time, rounds 1 / 2 / 3 | 75 s / 144 s* / 134 s | 38 s / 61 s / 105 s |

\* Includes one run whose timing was reconstructed after a container restart (728 s, may include queueing). Without it the round-2 v2.2 mean is 71 s.

## Findings

1. **Haiku 5.5 did not fail on any task whose spec was in the repository and whose request covered it.** These tasks included DST folds in 30-minute and midnight-shift zones, a complete npm range grammar checked against 783 oracle answers, a seven-site cross-file change with a format migration, a stale vendored docstring, and a mutated cache. Without the skill, Haiku read the spec, found the hidden defects and passed 23 of 27 runs. Two runs (one with v2.2, one without) found npm's bundled `semver` on the machine on their own and fuzzed against it.
2. **The one reproducible failure is about scope, not ability.** On eval 10 ("this test is failing, fix it"), all 6 runs fixed only the visible boundary bug. Every run *found* the offset and sort bugs. All 6 reported them and left them unfixed because the request named one test. The one difference: all 3 v2.2 runs confirmed the hidden bugs by running a probe, while 2 of the 3 no-skill runs only inferred them from reading the code. With the same fixture and a prompt asking for conformance to `docs/sessions.md` (10b), 6 of 6 passed. The skill does not change the outcome. Its rule 4 ("stay inside the request; recommend side edits") supports the narrow reading, and the v2.2 answers describe the extra bugs as outside the request.
3. **The only capability miss was a detail.** One no-skill eval-7 run returned the wrong exit status and message for an invalid timeout. All three no-skill eval-7 runs also edited `docs/config.md`, which nobody asked for.
4. **What the skill changes on hard tasks is process, not pass rate.** Residue: 0 runs with v2.2 against 19 without. No unrequested doc edits. Claims are checked by running code rather than read off it (eval 10 above). The cost is 25-32% more tokens and 1.2-2x the wall time.

## What this means for the eval suite

- Evals 6-13 are kept as regression checks. They are realistic and the acceptance scripts catch the trap solutions, but on Haiku 5.5 they do not separate configurations by pass rate. They separate them by residue and scope discipline, as the earlier benchmarks did.
- Eval 10 is kept with its original prompt as a **scope-judgment** probe. It fails every time on Haiku, so it can measure a future change to how the skill treats "fix this test" when the same spec is violated elsewhere. Eval 14 (the scoped prompt) is its control.
- Tasks that would actually fail Haiku probably need what these fixtures avoided on purpose: a requirement that is **not written down** (inferred from callers, data or history), context too large to read in full, or behaviour that only shows when a real external system runs. Those are harder to grade mechanically and are left for a later round.

## Limitations

- Three runs per cell. Rounds were designed one after another by the skill's author, who also wrote the acceptance scripts.
- Single-turn tasks in small projects. The runs could not ask questions, so scope ambiguity was resolved by the model alone.
- No v2.1 or v1.1 arms. This round compares only v2.2 with no skill.
