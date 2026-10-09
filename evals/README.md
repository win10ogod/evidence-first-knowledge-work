# Evaluating the Skill

This directory is for evaluators, not for the agent using the skill. Packaging tools exclude a root-level `evals/` directory, so none of this enters the agent's context. It contains runnable eval prompts, an instantiated fixture project with evaluator-owned acceptance checks, real test-runner captures, a trace auditor, and the tests for all bundled tools. Benchmark results are in [results/](results/): [v2.0 vs v1.1 vs no skill](results/2026-10-09-haiku-5-5/README.md) and [v2.1 vs v2.0 vs no skill](results/2026-10-09-haiku-5-5-v2.1/README.md), both on Haiku 5.5. Acceptance scripts run candidate code with `-B` and `PYTHONDONTWRITEBYTECODE=1` so that grading never creates the residue it measures.

## Contents

| Path | Purpose |
| --- | --- |
| [evals.json](evals.json) | Five runnable prompts with expectations (skill-creator schema) |
| [fixtures/exporter/](fixtures/exporter/) | A small Python CLI project with deliberate traps: an unused look-alike helper (`legacy.py`), and a runner that collects only `*_test.py` |
| [acceptance/exporter_acceptance.py](acceptance/exporter_acceptance.py) | Evaluator-owned checks for eval 1. Fails on the untouched fixture and on a "test not collected" solution; passes on a correct one |
| [fixtures/uploader/](fixtures/uploader/) | A Python 3.11 project (declared only in `pyproject.toml`, the CI workflow and the Dockerfile) whose spec describes the batching as `itertools.batched` semantics, an API that exists only on 3.12+ |
| [acceptance/uploader_acceptance.py](acceptance/uploader_acceptance.py) | Evaluator-owned checks for eval 5, run on `python3.11`. A `batched`-based solution passes on 3.13 and fails here; a correct one passes on both |
| [trigger-queries.json](trigger-queries.json) | 10 should-trigger and 10 near-miss queries for description optimization |
| [fixtures/runner_outputs.json](fixtures/runner_outputs.json) | 16 real outputs from unittest, pytest, Jest, Vitest, Go and Cargo (zero-test and normal runs) |
| [acceptance-cases.md](acceptance-cases.md) | 49 behavioral cases for reviewing transcripts |
| [cases.json](cases.json) | Eight further setup recipes that need evaluator-built repositories |
| [check_trace.py](check_trace.py) | Auditor for normalized step traces (format below) |
| `test_*.py` | Tests for the auditor, the hook and the snapshot script |

Run all tool tests from the repository root (standard library only, no network):

```bash
python -B -m unittest discover -s evals -p 'test_*.py' -v
```

## Comparing skill versions

1. Copy the fixture into an isolated workspace for each run. Keep `acceptance/` outside the candidate's writable area.
2. Run the same model on each `evals.json` prompt with (a) no skill, (b) the previous skill version, and (c) this version. Keep tools, permissions, context and budget comparable, and repeat each configuration several times.
3. Grade the expectations from the transcript, and run `python -I acceptance/exporter_acceptance.py <final copy>` for eval 1. The acceptance script executes candidate code, so run it in the sandbox.
4. Record pass rate, tokens, tool calls and wall time separately. Keep failed runs. Log any human or stronger-model assistance and report assisted results separately.
5. Test on every model you deploy with. Guidance that works for a large model may be insufficient for a small one, and the reverse can over-explain.

The skill-creator workflow (with-skill and baseline subagents, a grader, `aggregate_benchmark`, and the review viewer) can consume `evals.json` directly. Use `trigger-queries.json` with its description-optimization loop.

Judge two outcomes separately: **task outcome** (acceptance passes, no regressions, no unrequested changes) and **process** (reads before edits, honest PASS/FAIL/NOT RUN, no repeated disproven attempts, no unnecessary blocking). Penalize shrinking scope, weakening tests and doing nothing just as much as gate violations.

## Trace auditor

[check_trace.py](check_trace.py) checks a **normalized JSON event array** derived from the host's real tool trace. The evaluator builds this array and keeps the mapping back to the original receipts. Never ask the candidate to produce a passing trace.

```bash
python -B evals/check_trace.py trace.json               # stop at the first violation
python -B evals/check_trace.py --all-errors trace.json  # report every invalid step
```

Exit codes: 0 consistent, 1 violation, 2 input error. Input is limited to 5,000,000 characters. Each result reports task outcome as NOT MEASURED and receipt authenticity as NOT VERIFIED.

### Event contract (version 2)

Every event needs `seq` (a strictly increasing positive integer), `kind`, `step` (episode ID) and `receipt` (a locator in the original trace). Revision identifiers must never repeat for different points in time; use a write counter or a hash plus sequence number.

| Kind | Fields | Rules |
| --- | --- | --- |
| `begin` | `requirements`; `targets`; `checks`; `sources` (source → version); optional `level` (`L0`-`L3`, default `L2`), `depends_on`, `no_source_reason`, `authorization`, `recovery` | `sources` may be `{}` only with `no_source_reason`. L0 may have empty `targets` and `checks`. L1 may not touch a target of an earlier FAILed step. L3 needs `authorization` and `recovery` |
| `read_doc` | `source`, `revision`, `section`, `complete: true` | Must match the planned version; before the mutation |
| `read_target` | `target`, `revision`, `complete: true` | `ABSENT` for observed absence; a revision already replaced by a recorded mutation is stale |
| `mutate` | `before`, `after` (target → revision) | Not allowed in L0. L2/L3 must re-read every source in this step. L1 may rely on a source read at the same version in an earlier step. Targets must be in scope and freshly read |
| `inspect` | `revisions` | Must equal the post-mutation revisions |
| `check` | `check`, `status` (`PASS`/`FAIL`/`NOT RUN`), `revisions`; optional `test_count`, `exit_code` | A PASS with `test_count` 0 or a non-zero `exit_code` is rejected |
| `end` | `status` (`PASS`/`FAIL`/`BLOCKED`); `reason` unless PASS | L0 PASS needs at least one read; other PASS needs an inspected mutation and every planned check passing |

An honest FAIL or BLOCKED episode is process-compliant even though it delivers nothing. Shell side effects, source relevance, comprehension and overall correctness are outside the auditor's scope. A self-authored trace can lie, so use trusted recording together with independent artifact checks.

## Zero-test captures

`fixtures/runner_outputs.json` was captured on 2026-10-09 with Python 3.13.16 unittest, pytest 9.1.1, Jest 29.7.0, Vitest 2.1.9, Go 1.24.7 and Cargo 1.97.0. Four of the zero-test runs exit with code 0: a Jest `-t` filter, a Go `-run` filter, Go with no test files, and Cargo. This is why `hooks/zero_tests_guard.py` reads the output instead of trusting exit codes. Re-capture with newer runner versions before relying on the patterns elsewhere.
