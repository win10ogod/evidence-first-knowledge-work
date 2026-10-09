# evidence-first-knowledge-work

**Version 2.1.0 | English | MIT**

An Agent Skill that stops the most common way agents damage engineering work: confident guesses. Examples are a parameter remembered from another version, an edit to a file that changed since it was read, a test run that selected zero tests, or a "done" nobody checked. It is written to work with smaller models as well as larger ones.

**Verify before writing. Re-read the target before every edit. Report only checks that actually ran.** How much ceremony a step needs depends on what the step does (L0 read-only, L1 local edit, L2 standard, L3 guarded), never on how confident the model feels.

See [CHANGELOG.md](CHANGELOG.md) for what changed from 1.x.

## Layout

| Path | Loaded | Purpose |
| --- | --- | --- |
| [SKILL.md](SKILL.md) | When the skill triggers | Core rules, rigor levels, receipt format, the loop, stop rules, routing table (~2.6k tokens) |
| [references/engineering.md](references/engineering.md) | Code/config/CLI/test work | Reconnaissance, execution paths, API checklist, decomposition, edit and validation discipline |
| [references/verification-recipes.md](references/verification-recipes.md) | When an exact command is needed | Versions, signatures, CLI flags and test selection for Python, Node, Go, Rust and git |
| [references/research.md](references/research.md) | Research, Q&A, data, docs | Primary sources, claim labels, data contracts, numbers, documentation edits |
| [references/decision-playbook.md](references/decision-playbook.md) | Unknowns, conflicts, failures | Unknown types, experiment design, failure triage, diagnosis reset, escalation |
| [references/records.md](references/records.md) | Multi-step or multi-session work | Requirement ledger, failure ledger, checkpoints, delivery format |
| [references/worked-examples.md](references/worked-examples.md) | Unfamiliar situations | Level selection and six fictional end-to-end examples |
| [references/completion-review.md](references/completion-review.md) | Before delivery | Independent oracles, real selection, real entry points, diff integrity |
| [scripts/env_snapshot.py](scripts/env_snapshot.py) | Executed, not read | Read-only snapshot: git state, instruction files, manifests, runtimes, installed package versions |
| [hooks/](hooks/) | Optional, Claude Code | `PostToolUse` hook that warns when a test run selected zero tests |
| [project-instructions.snippet.md](project-instructions.snippet.md) | Merge into AGENTS.md / CLAUDE.md | Short always-on reminder that points to the skill |
| [evals/](evals/README.md) | Evaluators only | Runnable prompts, fixture project, acceptance checks, trigger queries, trace auditor, tool tests |

Every reference file is linked directly from SKILL.md (one level deep), and every file over 100 lines has a table of contents. SKILL.md stays under the 5,000 tokens that Claude Code re-attaches after context compaction, so the whole core survives compaction.[3]

## Installation

Install a clean runtime copy (no `.git/`, no `evals/`) into your host's skill location:

```bash
mkdir -p <dest> && git archive --prefix=evidence-first-knowledge-work/ HEAD | tar -x -C <dest>
```

| Host | `<dest>` (the skill lands in `<dest>/evidence-first-knowledge-work/`) |
| --- | --- |
| Claude Code (project) | `<project>/.claude/skills` |
| Claude Code (personal) | `~/.claude/skills` |
| Codex (project) | `<project>/.agents/skills` |

Then merge [project-instructions.snippet.md](project-instructions.snippet.md) into your existing `CLAUDE.md` or `AGENTS.md`. Replace `<SKILL_DIR>` with the actual install path. Read your existing instructions first, do not overwrite them, and start a new session so the host picks up the change.[1][2][3][4]

Invoke the skill explicitly with `/evidence-first-knowledge-work` (Claude Code) or `$evidence-first-knowledge-work` (Codex), or let the description trigger it automatically. The frontmatter uses only portable fields (`name`, `description`, `license`, `metadata`), so the same SKILL.md also uploads to claude.ai and the Skills API.[3][5]

### Optional: zero-test hook (Claude Code)

Merge the `hooks` block from [hooks/settings.example.json](hooks/settings.example.json) into `.claude/settings.json`, adjusting the path if you installed the skill elsewhere. After each Bash call, the hook scans the output for zero-selection signals (for example `running 0 tests`, `[no tests to run]`, `N skipped, N total`) and adds a reminder to Claude's context. It never blocks, never rewrites output, and always exits 0.[6] The patterns come from real runner output (see [evals/README.md](evals/README.md#zero-test-captures)).

## Validation

```bash
python -B -m unittest discover -s evals -p 'test_*.py' -v   # 46 tests: auditor, hook, snapshot script
```

The tool tests show that the bundled tools behave as specified. They do not measure whether a model performs better with the skill. To measure that, run the prompts in [evals/evals.json](evals/evals.json) with and without the skill on the models you deploy, as described in [evals/README.md](evals/README.md).

Benchmarks on Haiku 5.5:

- [v2.1 vs v2.0 vs no skill](evals/results/2026-10-09-haiku-5-5-v2.1/README.md): 45 runs, mechanical grading. Mean pass rate v2.1 0.987, v2.0 0.888, no skill 0.801. Generated residue in 0/12, 6/12 and 9/12 project runs respectively. v2.1 costs the same tokens as v2.0 and about 20% more than no skill.
- [v2.0 vs v1.1 vs no skill](evals/results/2026-10-09-haiku-5-5/README.md): 24 runs. Mean pass rate 1.00, 0.94 and 0.78.

Both are small samples graded by the skill's author, so treat them as directional.

## Limits

These are instructions, not enforcement; the optional hook is the only automated control. The trace auditor checks recorded ordering, not whether receipts are authentic or relevant. Level thresholds, the two-failure diagnosis reset and the receipt format are design choices made by this project. They are not official platform requirements or empirically tuned values.

## Sources

Anthropic sources [3], [5] and [6] were re-checked on 2026-10-09. The OpenAI sources [1] and [2] were checked on 2026-09-25 for 1.1.0 and could not be re-fetched for this release (DNS failure), so confirm the Codex paths against current docs. Platform sources support the format, loading, frontmatter and hook mechanics. The workflow itself is this project's design.

[1] OpenAI, Build skills: https://developers.openai.com/codex/skills

[2] OpenAI, Custom instructions with AGENTS.md: https://developers.openai.com/codex/guides/agents-md

[3] Anthropic, Extend Claude with skills (frontmatter fields, portability, 1,536-character listing cap, 5,000-token re-attachment after compaction): https://code.claude.com/docs/en/skills

[4] Anthropic, How Claude remembers your project: https://code.claude.com/docs/en/memory

[5] Anthropic, Skill authoring best practices (conciseness, third-person descriptions, one-level references, tables of contents over 100 lines, utility scripts, evaluation-first development): https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

[6] Anthropic, Hooks reference (`PostToolUse` input, `hookSpecificOutput.additionalContext`, exit codes): https://code.claude.com/docs/en/hooks
