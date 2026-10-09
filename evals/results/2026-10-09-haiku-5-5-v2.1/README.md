# Benchmark: v2.1 vs v2.0 vs no skill (Haiku 5.5, 2026-10-09)

The five prompts in [evals.json](../../evals.json) were each run with three configurations, three runs per cell, giving 45 runs. Every run used `claude-haiku-5-5` as a fresh subagent. Each worked in its own fixture copy, in a directory with a random name.

- **v2.1**: SKILL.md at commit `bbccd96`.
- **v2.0**: SKILL.md at commit `59cf0ee`.
- **no skill**: the same task with no skill.

**Grading is mechanical.** Every expectation is decided by a fixed rule over the tool-call transcript, the final files, the answer text and the evaluator-owned acceptance scripts. Eval 5's script runs the candidate under `python3.11`. No run was judged individually. Per-run evidence is in [runs.json](runs.json), and the aggregate is in [benchmark.json](benchmark.json).

## Results

| Eval | v2.1 | v2.0 | No skill |
| --- | --- | --- | --- |
| 1 Exporter integration (9 checks) | 1.00 / 1.00 / 1.00 | 0.89 / 0.89 / 0.89 | 0.89 / 0.78 / 0.89 |
| 2 Analysis only (4) | 1.00 / 1.00 / 1.00 | 0.75 / 0.75 / 0.75 | 0.75 / 0.75 / 0.75 |
| 3 unittest exit code (4) | 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 0.75 |
| 4 "Trivial" rename (5) | 1.00 / 0.80 / 1.00 | 0.80 / 0.80 / 0.80 | 0.60 / 0.40 / 0.80 |
| 5 Python 3.11 batching (6) | 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 | 0.83 / 0.83 / 1.00 |
| **Mean** | **0.987 ± 0.050** | **0.888 ± 0.102** | **0.801 ± 0.152** |
| Mean excluding assertions added after iteration 1 | 0.983 | 0.950 | 0.883 |

| | v2.1 | v2.0 | No skill |
| --- | --- | --- | --- |
| Tokens / run | 63.7k | 63.4k | 53.1k |
| Wall time / run | 47.8 s | 41.0 s | 31.8 s |
| Tool calls / run | 16.1 | 15.7 | 11.1 |
| Left `__pycache__` in the project (of 12 project runs) | **0** | 6 | 9 |
| Unrequested `docs/formats.md` edit in eval 1 (of 3) | **0** | 3 | 3 |

## Findings

- **The v2.1 rules worked as intended.** The two rules added after iteration 1 ("Leave no residue" and "recommend, don't make, side edits") removed both failure classes: residue went from 6/12 to 0/12, and unrequested doc edits from 3/3 to 0/3. Every v2.1 eval-1 run listed the stale doc label as a recommendation instead of editing it.
- **The core behaviors hold.** With the new scope and residue assertions excluded, the order stays the same (0.983 > 0.950 > 0.883), but the gap between v2.1 and v2.0 shrinks to about three points. The rest of v2.1's lead comes from assertions written for its new rules.
- **The eval 5 trap did not trigger.** No run used `itertools.batched`, and every run, including all no-skill runs, tested with `python3.11`, because the README names that interpreter directly. Eval 5 therefore measures residue and scope rather than target-runtime discipline. A subtler fixture, with the target declared only in `pyproject.toml` or CI, is needed.
- **The remaining v2.1 miss is in eval 4.** One run checked `inspect.signature` after the edit instead of re-reading the file. Two of three no-skill runs never ran `run_tests.py`.
- **Cost.** v2.1 costs the same as v2.0 overall. It is cheaper on edits, because L1 work reads only SKILL.md (eval 4: -4k, eval 5: -2k tokens), and more expensive on research, because it checks more sources (eval 3: +8k). Against no skill it uses about 20% more tokens and 50% more wall time.

## Grading bug found and fixed

The first grading pass showed `__pycache__` in eight eval-1 projects. The timestamps showed the caches had appeared after the agents finished: `exporter_acceptance.py` ran the candidate CLI and tests without `-B`. Both acceptance scripts now run children with `-B` and `PYTHONDONTWRITEBYTECODE=1`. Caches newer than each run's `answer.md` were removed, and grading was re-run twice with identical output. All residue counted above predates the agent's own answer.

The same contamination affected the eval-1 `pycache_left` flags in the iteration-1 `runs.json`. They have been corrected to the first-pass values. Iteration 1's README statistics and pass rates already used the first-pass values and are unchanged.

## Limitations

- Three runs per cell. The v2.1 vs v2.0 difference rests largely on assertions designed after iteration 1.
- The grading rules are mechanical, but the grader also wrote the skill and the rules.
- The skill was supplied by telling the agent to read SKILL.md; automatic description triggering was not measured.
