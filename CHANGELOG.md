# Changelog

## 2.1.0

Driven by the 2026-10-09 Haiku 5.5 benchmark (`evals/results/2026-10-09-haiku-5-5`).

- New core rule **Leave no residue**: run Python with `-B`, keep scratch copies outside the project, and remove what you created. A read-only task leaves the project byte-identical. (In the benchmark, 10 of 18 runs left `__pycache__` behind.)
- **Stay inside the request** now says to recommend side changes (doc status labels, helpers) instead of making them, and SCOPE in the receipt is binding. (4 of 6 eval-1 runs edited `docs/formats.md` unasked.)
- "Version in use" now means the project's **target runtime** (README, `requires-python`, CI, Dockerfile), not the interpreter on PATH. Added target-interpreter recipes.
- Research: added fallbacks for when an official docs site is unreachable (raw files at a release tag, local stdlib sources) and a method for "since which version" questions (changelog entry or adjacent-tag comparison).
- Cost: SKILL.md alone is enough for L0 and L1 work; `engineering.md` and `completion-review.md` are only required for L2 and L3 steps.
- Result: on Haiku 5.5 (45 runs, mechanical grading), mean pass rate went from v2.0 0.888 to v2.1 0.987 (no skill 0.801), and residue from 6/12 to 0/12 at the same token cost as v2.0; see `evals/results/2026-10-09-haiku-5-5-v2.1`.
- Evals: acceptance scripts no longer create `__pycache__` in candidate projects.
- Evals: added eval 5 (`fixtures/uploader`, a Python 3.11 target with an `itertools.batched` trap) and scope and residue expectations for evals 1 and 4.

## 2.0.0

Restructured to follow current skill-authoring guidance: concise core, progressive disclosure, explanations of why, utility scripts, and evaluation first.

**Behavior**

- Replaced blanket per-step rules with four rigor levels (L0 read-only, L1 local edit, L2 standard, L3 guarded), chosen by objective triggers. Confidence, change size and "low risk" labels still never lower a level.
- L1 may reuse a contract verified earlier in the same task at the same version, while it is still in context. It must always re-read the target. Retries after a failure are at least L2.
- Source priority now favors installed, version-matched source and type stubs over "latest" online docs. Online checks remain required for time-sensitive facts; when offline, claims are labeled unverified instead of blocking all work.
- One step receipt format (about 7 lines; 1 line for L1) replaces the three overlapping contract templates.

**Structure**

- SKILL.md went from 2,071 to about 1,460 words and stays inside the 5,000-token re-attachment budget used after compaction. The description is now third-person "what + when", with explicit non-triggers.
- Merged `coding-protocol.md` and `guided-development.md` into `references/engineering.md`; renamed `knowledge-protocol.md` to `research.md` and `evidence-template.md` to `records.md`. Required reading for engineering tasks dropped from about 6,100 to about 3,300 words.
- Added `references/verification-recipes.md` with concrete commands, verified locally, for versions, signatures and test selection.
- Every reference is linked directly from SKILL.md, and files over 100 lines have a table of contents.
- Replaced the two near-identical platform snippets with a single `project-instructions.snippet.md`.
- Moved `acceptance-cases.md` to `evals/` (evaluator material) and added cases 41-46 for the levels.

**Tools**

- `scripts/env_snapshot.py`: read-only snapshot of git state, instruction files, manifests, runtimes and installed package versions.
- `hooks/zero_tests_guard.py`: optional Claude Code `PostToolUse` hook that flags zero-test runs, including ones that exit 0.
- `evals/check_trace.py`: event contract v2 with levels, `no_source_reason`, L3 authorization and recovery fields, cross-step stale-revision detection, and `--all-errors`.
- `evals/`: runnable `evals.json`, a fixture project with traps, an evaluator-owned acceptance script, 20 trigger queries, and real runner captures.

## 1.1.0

Added guided development for smaller models, worked examples, the decision playbook, the completion review, 40 acceptance cases and the trace auditor.
