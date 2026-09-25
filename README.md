# evidence-first-knowledge-work

A behavioral skill for evidence-first knowledge work. Language: English. Version: 1.0.0.

Core rule: verify before writing; re-read version-matched documentation and current target state before every edit step; stop the affected step when required evidence is missing; claim only results that were actually validated.

## Contents

| File | Purpose |
| --- | --- |
| [SKILL.md](SKILL.md) | Core principles, G0-G6 gates, per-step re-verification, blocking rules, and delivery discipline. |
| [references/coding-protocol.md](references/coding-protocol.md) | Repository reconnaissance, API verification, patch contracts, command control, side effects, testing, and precise rollback. |
| [references/knowledge-protocol.md](references/knowledge-protocol.md) | Research, primary-source reading, analysis, citation, and documentation maintenance. |
| [references/evidence-template.md](references/evidence-template.md) | Compact evidence and before/after step records. |
| [references/acceptance-cases.md](references/acceptance-cases.md) | 20 behavioral acceptance cases for checking actual operation order and evidence. |
| [AGENTS.snippet.md](AGENTS.snippet.md) | Persistent Codex project rule to merge into an existing AGENTS.md. |
| [CLAUDE.snippet.md](CLAUDE.snippet.md) | Persistent Claude Code project rule to merge into an existing CLAUDE.md. |
| [LICENSE](LICENSE) | MIT license. |

## Installation and loading

This repository contains instruction files only. It does not automatically install hooks, intercept tool calls, or modify user settings.

### Codex projects

Place the repository under:

```text
<project>/.agents/skills/evidence-first-knowledge-work/
```

Codex documentation describes repo-local skills under `.agents/skills/` and supports both explicit invocation and description-based matching.[1]

Read the existing `AGENTS.md` and applicable project rules first. Then merge `AGENTS.snippet.md` into the root `AGENTS.md` without overwriting existing instructions. Codex builds its instruction chain at session start, so begin a new session after updating it and confirm the effective instruction sources, overrides, and size limits.[2]

Explicit invocation:

```text
$evidence-first-knowledge-work
Follow this skill for the task. Verify first and read the current target state before editing.
```

### Claude Code projects

Place the repository under:

```text
<project>/.claude/skills/evidence-first-knowledge-work/
```

Read the existing `CLAUDE.md`, then merge `CLAUDE.snippet.md` into it while preserving existing rules.[3][4]

Explicit invocation:

```text
/evidence-first-knowledge-work
```

Persistent instructions and full skill loading serve different purposes. After installation, verify which source is actually in effect. You normally do not need both platform snippets in the same project.[2][4][5]

### Paths and existing project rules

The snippets use project-root-relative paths. If you install the skill elsewhere, update the snippet to the confirmed real path and verify that the file is readable. Do not move the skill while leaving a dead reference behind.

This repository preserves repository reconnaissance, ownership boundaries, and patch-contract discipline while adding cross-task and per-step evidence gates. If a project already has equivalent rules, merge and deduplicate them under the applicable instruction hierarchy. Do not delete, disable, or weaken existing requirements without valid authorization.

## Enforcement boundary

The skill and persistent snippets can state mandatory behavior such as "must", "must not", and "stop if blocked". This repository does not install an external enforcement layer, so it cannot guarantee system-level prevention of every violating tool call.

Claude documentation distinguishes contextual guidance in CLAUDE.md from external enforcement mechanisms such as hooks and managed settings. Loading text instructions alone does not prove perfect compliance.[4]

This repository intentionally stays at the portable instruction layer. It does not invent cross-platform YAML enforcement fields, hook APIs, or permission controls that are not part of the documented skill format.[6]

## Validation and limitations

Format checks should verify UTF-8, YAML front matter, directory/name consistency, required files, and relative links. Packaged archives should additionally be checked for readability and content completeness.[6]

Behavioral checks are defined in `references/acceptance-cases.md`. They focus on whether source reading happens before dependent writing or editing, whether scope matches the contract, and whether validation claims correspond to real tool results. A syntactically valid skill, a self-written `PASS`, or a statement that the agent "understands" the rule does not prove compliance.

This repository has not been behaviorally benchmarked across the user's Codex, Claude Code, or other agent environments. It does not claim measured trigger rates, compliance rates, or guaranteed behavior under conflicting instructions.

## Format and platform references

Checked: 2026-09-25. These sources support file layout and loading behavior. The G0-G6 workflow and operational constraints in this repository are project-specific rules, not platform policy.

[1] OpenAI, "Using skills to accelerate OSS maintenance". Repo-local Codex `.agents/skills/`, `AGENTS.md`, and progressive loading.

```text
https://developers.openai.com/blog/skills-agents-sdk
```

[2] OpenAI, model guidance: "Using AGENTS.md". Codex AGENTS.md loading and instruction scope.

```text
https://developers.openai.com/api/docs/guides/latest-model
```

[3] Anthropic, "Explore the .claude directory". Claude Code `.claude/skills/` and `CLAUDE.md` locations.

```text
https://code.claude.com/docs/en/claude-directory
```

[4] Anthropic, "Extend Claude Code". Roles of `CLAUDE.md`, Skills, Hooks, and permission mechanisms.

```text
https://code.claude.com/docs/en/features-overview
```

[5] Anthropic, "Extend Claude Code". Difference between persistent instructions and on-demand skill loading.

```text
https://code.claude.com/docs/en/features-overview
```

[6] Agent Skills, Specification. Name, description, directory, front matter, and relative references.

```text
https://agentskills.io/specification
```
