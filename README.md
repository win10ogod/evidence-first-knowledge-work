# evidence-first-knowledge-work

**Version 1.1.0 | English | MIT**

A strict evidence-first skill with guided execution for smaller or less reliable models working on open-ended development tasks. It makes requirements, discovery, decomposition, experiments, recovery, integration, and completion checks explicit. It is intended to reduce unsupported engineering decisions; it does not claim to turn every model into an expert.

**Verify before writing. Re-read version-matched documentation and current targets before every independent edit. Validate the actual result. Never claim a check ran when it did not.** Familiar APIs, small changes, low-risk labels, and model confidence do not waive these requirements.

## What changed in 1.1.0

The original G0-G6 gates and strict per-step reads remain. The guided profile adds a concrete route from an open-ended request to requirement-linked work items, execution-path evidence, bounded experiments, failure diagnosis, resumable checkpoints, and independent completion review.

Six fictional worked examples demonstrate good and insufficient evidence. Forty behavioral cases define process expectations. Eight evaluator setup recipes address actual development outcomes. A small executable trace auditor checks recorded ordering and preconditions, with synthetic unit tests that deliberately include violations. These tools do not run a model or enforce tool permissions.

## Files and loading

| File | Purpose |
| --- | --- |
| [SKILL.md](SKILL.md) | Mandatory core, G0-G6 gates, strict rereads, and the guided execution routing table. |
| [references/guided-development.md](references/guided-development.md) | Request decomposition, real call paths, owning-layer evidence, one active implementation item, integration, and resumable state. |
| [references/decision-playbook.md](references/decision-playbook.md) | Unknown-contract versus unknown-outcome decisions, experiments, diagnosis resets, conflicts, and scoped blocking. |
| [references/worked-examples.md](references/worked-examples.md) | Six fictional examples covering integration, novel designs, repeated failure, concurrency, test oracles, and resumption. |
| [references/completion-review.md](references/completion-review.md) | Independent expectations, real test execution, final-revision integration, scope preservation, and honest completion. |
| [references/coding-protocol.md](references/coding-protocol.md) | Existing repository reconnaissance, API verification, patch contracts, side effects, testing, and precise rollback. |
| [references/knowledge-protocol.md](references/knowledge-protocol.md) | Research, data analysis, source verification, and documentation maintenance. |
| [references/evidence-template.md](references/evidence-template.md) | Requirement ledger, per-step receipts, failure history, checkpoints, and delivery mapping. |
| [references/acceptance-cases.md](references/acceptance-cases.md) | Forty behavioral acceptance cases, including weaker-model failure modes. |
| [AGENTS.snippet.md](AGENTS.snippet.md) / [CLAUDE.snippet.md](CLAUDE.snippet.md) | Persistent loading snippets to merge into existing project instructions. |
| [evals/README.md](evals/README.md) | Target-model comparisons, the trace format, and evaluation limitations. |
| [evals/cases.json](evals/cases.json) | Eight setup recipes requiring evaluator-prepared repositories and independent tests. |
| [evals/check_trace.py](evals/check_trace.py) / [evals/test_check_trace.py](evals/test_check_trace.py) | Read-only trace auditing and synthetic tests of the auditor. |
| [LICENSE](LICENSE) | MIT license. |

Read the core in full. Engineering tasks also load the coding protocol and guided development. Load the relevant decision/example section at its trigger, and load the completion review before delivery. No default "fast mode" lets a model skip evidence. The file split keeps unrelated material out of the active context without removing required operations.

## Installation

### Codex

Place this whole directory at:

```text
<project>/.agents/skills/evidence-first-knowledge-work/
```

Read the existing project rules, then merge `AGENTS.snippet.md` into the root `AGENTS.md`. Preserve existing instructions and check the effective discovery scope and overrides. Codex loads repository skills from `.agents/skills/`; it builds its instruction chain at startup, so start a fresh session after changing persistent instructions.[1][2]

```text
$evidence-first-knowledge-work
Use guided execution. Preserve every requested outcome and re-read evidence before each independent edit.
```

### Claude Code

Place the whole directory at:

```text
<project>/.claude/skills/evidence-first-knowledge-work/
```

Read the existing `CLAUDE.md` before merging `CLAUDE.snippet.md`. Confirm the actual instruction and skill sources in the installed environment. Project skill placement and explicit invocation follow Claude Code's documented skill mechanism.[3][4]

```text
/evidence-first-knowledge-work
```

The snippets use project-root-relative paths. Update them to a confirmed real path when installing elsewhere. Do not overwrite existing AGENTS.md or CLAUDE.md, duplicate conflicting rules, or assume the skill loaded merely because its files exist. Keep the appropriate platform snippet; the skill does not require duplicate loading through both platforms.

## Validation

The optional auditor uses Python's standard library and does not install dependencies, execute a candidate, or contact a service. Read its documented scope first:

```text
python -B -m unittest discover -s evals -p 'test_*.py' -v
python -B evals/check_trace.py /path/to/normalized-trace.json
```

The unit tests validate the auditor on synthetic events. They do not measure a weak model's ability. Real evaluations must compare comparable target-model runs, inspect the actual tool trace, and independently test the final artifact. Record stronger-model or human assistance separately.[6]

Structural review should also check UTF-8, YAML front matter, name/directory consistency, required files, relative links, and package integrity.[7]

## Limits and enforcement boundary

The workflow is an instruction-level control. No hooks, tool interceptor, provider adapter, or permission changes are installed. The trace auditor cannot authenticate receipts, detect omitted events, verify source relevance, or judge task success. A fabricated trace can lie. Host-level enforcement requires separate authorized integration with documented host mechanisms.[4]

The intended use includes less capable models that need explicit steps and examples. Guidance should be tested on the models actually used; effectiveness cannot be inferred from a stronger model's behavior.[5] This release has no measured target-model completion rate, compliance rate, or advanced-development benchmark result. Good procedure can expose limits and support reliable progress without proving universal capability.

## Sources

Checked 2026-09-25. Platform sources support format and loading instructions. The specific workflow, diagnosis-reset rule, examples, and trace schema are project-authored choices, not official platform requirements or empirically proven thresholds.

[1] OpenAI, Build skills: https://developers.openai.com/codex/skills

[2] OpenAI, Custom instructions with AGENTS.md: https://developers.openai.com/codex/guides/agents-md

[3] Anthropic, Extend Claude with skills: https://code.claude.com/docs/en/skills

[4] Anthropic, How Claude remembers your project: https://code.claude.com/docs/en/memory

[5] Anthropic, Skill authoring best practices, especially model-specific guidance, explicit workflows, examples, and verifiable intermediate outputs: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

[6] OpenAI, Testing Agent Skills Systematically with Evals: https://developers.openai.com/blog/eval-skills

[7] Agent Skills, Specification: https://agentskills.io/specification

[8] Python 3.13 standard-library references used for the auditor: https://docs.python.org/3.13/library/json.html ; https://docs.python.org/3.13/library/argparse.html ; https://docs.python.org/3.13/library/pathlib.html ; https://docs.python.org/3.13/library/unittest.html
