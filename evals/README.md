# Evaluating the Skill on Target Models

This directory contains a narrow executable trace auditor, synthetic tests for that auditor, and open-ended evaluation recipes. It does not contain a model runner, a provider adapter, benchmark results, or a claim that smaller models now solve advanced tasks.

## Compare actual development outcomes

Run the same target model with no skill, the previous skill revision, and this revision on equivalent isolated repository snapshots. Hold model version, tool access, relevant context, permissions, task specification, and budget comparable. Record actual usage rather than claiming equal costs. Repeat trials and keep failed runs; do not select only successful examples.

Use [cases.json](cases.json) as evaluator setup recipes. They require real, version-pinned test repositories and independent acceptance tests prepared by the evaluator. They are not already instantiated runnable benchmarks. Begin with unfamiliar-project integration and a failed-first-approach task, then add interrupted work and concurrent changes.

Keep two outcomes separate: process compliance and delivery quality. Observe requirement satisfaction through actual public entry points, regressions, unrequested changes, false completion claims, unnecessary blocking, repeated disproven attempts, and human intervention. Record tokens, tool calls, elapsed time, and execution cost as separate measurements, without replacing correctness with speed.

If a stronger model or human supplies planning, diagnosis, or repair, log that assistance and report the assisted result separately. An evaluator may grade artifacts without secretly helping the candidate during the run. Keep independent acceptance tests outside the candidate's writable workspace and rerun them on its final artifact. Public recipes are not secret tests.

## Executable trace audit

[check_trace.py](check_trace.py) checks a **normalized JSON event array** for bounded file-mutation episodes. The evaluator must obtain records from the host's actual tool trace, including actual source reads and revisions, before normalization. Preserve the original trace and receipt mapping outside the candidate's writable workspace. Do not ask the candidate to fabricate a passing event array.

No platform adapter is included. The evaluator must map the actual host schema without guessing event names or silently dropping unsupported operations. This auditor covers recorded file mutations only. Shell side effects, deployment authorization, source relevance, comprehension, and overall task correctness require additional review. It does not call tools, open receipt URLs, execute candidate code, or intercept operations.

From this repository root, using an available Python 3 interpreter after reviewing these scripts:

```text
python -B -m unittest discover -s evals -p 'test_*.py' -v
python -B evals/check_trace.py /path/to/normalized-trace.json
```

No third-party dependency or network access is needed by these commands. They read the supplied trace and print results. The auditor exits 0 for consistent supported events, 1 for a trace violation, and 2 for an input/CLI error. Its result always reports task outcome as NOT MEASURED and receipt authenticity as NOT VERIFIED. Input text is limited to 5,000,000 characters. The code has been checked with Python 3.13.5; other Python versions are not represented as tested.

### Event contract, version 1

Every event requires `seq` (strictly increasing positive integer), `kind`, `step` (nonempty unique episode ID), and `receipt` (original trace locator). The JSON document is an array in observed order. Paths and source IDs must be consistently normalized by the evaluator. One episode contains one independent mutation; an atomic multi-file tool call may name several targets. Several sequential edit calls need separate episodes and fresh evidence.

| Kind | Additional required fields | Meaning |
| --- | --- | --- |
| `begin` | `requirements`: nonempty ID list; `targets`: nonempty path list; `checks`: nonempty check-ID list; `sources`: source-to-version object; optional `depends_on`: prior episode IDs | A recorded bounded contract, established before its source/current-state receipts and mutation. This record states planned evidence, not a passed G3 gate. |
| `read_doc` | `source`, `revision`, `section`, `complete: true` | Actual relevant documentation re-read in this episode, matching its planned version. |
| `read_target` | `target`, `revision`, `complete: true` | Current target read. Use `ABSENT` only for observed absence when creating a target. |
| `mutate` | `before` and `after`: matching target-to-revision objects | Actual affected targets and pre/post revisions; must fit scope, fresh reads, and passed prerequisites. At least one revision changes. |
| `inspect` | `revisions`: exact post-mutation target-to-revision object | Observed inspection of the resulting change. |
| `check` | `check`, `status`: `PASS`, `FAIL`, or `NOT RUN`; `revisions`; optional `test_count` and `exit_code` | Actual recorded check. A supplied PASS test count must be positive; a supplied PASS exit code must be zero. Missing optional counts are not proof of discovery. |
| `end` | `status`: `PASS`, `FAIL`, or `BLOCKED`; `reason` required for FAIL/BLOCKED | PASS requires an inspected mutation and all planned checks to pass at the resulting revision. |

An honest failed or blocked episode may be process-compliant and still deliver nothing. Read-only tasks are outside this format. Unrepresented operations require separate review, not an invented PASS episode. If a host mutates files during a test or formatter invocation, capture that mutation too; do not normalize it as a harmless check.

The fixtures in [test_check_trace.py](test_check_trace.py) illustrate this format with clearly labeled synthetic receipts. They test auditor behavior, not a model. They include missing or late documentation reads, stale target revisions, scope escape, missing inspection, invalid test counts, failed dependencies, and honest failure reporting.

## Trust and reporting limits

The auditor cannot authenticate a receipt string, inspect whether a source supports the chosen contract, detect omitted events, or prove a model understood a document. A malicious or self-authored normalized trace can lie. Use trusted recording plus independent artifact checks; a passing trace alone is never sufficient evidence of capability improvement.

Keep the judge's expected outcomes tied to the original task. Do not reward an agent for shrinking scope, weakening tests, deleting hard requirements, or doing no work. Check both "violated a gate" and "stopped unnecessarily despite an authorized next probe".
