# Engineering Protocol

Detailed guidance for code, configuration, CLI and test work. SKILL.md sets the rules and levels; this file explains how to carry them out.

## Contents

1. Reconnaissance: read the project before declaring a gap
2. Trace the real execution path and owning layer
3. API and tool contract checklist
4. Decompose into steps
5. Edit and command discipline
6. Validation
7. Reverts
8. Interruption and resumption

## 1. Reconnaissance

Before the first edit, collect this evidence. `scripts/env_snapshot.py` gathers most of the environment row in one read-only call.

| Area | What to establish |
| --- | --- |
| Project rules | AGENTS.md, CLAUDE.md, CONTRIBUTING, subdirectory instructions. Never rewrite governing rules to permit a change. |
| Environment | The **target** runtime (README, `requires-python`, `.python-version`, CI matrix, Dockerfile) and the installed version of each relevant dependency. Declared ranges (manifest), locked versions (lockfile), the interpreter on PATH and the production runtime can all differ. Run checks on the target. |
| Existing work | Branch, uncommitted changes, untracked files. Treat edits you did not make as the user's. |
| Existing capability | Related implementations, flags, wrappers, registries and generated sources. Search several names and locations before declaring a feature absent. |
| Tests | How the project actually runs tests (docs, scripts, CI config), where tests live, the naming pattern the runner collects, and pre-existing failures. |

Read at least the complete semantic unit around an edit (the whole function or class, plus imports and file-level config). Read the whole file before cross-section edits or rewrites. If output was truncated, read the rest; never reconstruct missing text. Before creating a file, confirm it does not exist and look at neighboring conventions.

## 2. Trace the real execution path

A similarly named function is only a candidate. To choose where a change belongs:

1. Find the user-facing entry: command, route, public method, event handler or job.
2. Follow dispatch or registration from that entry to the behavior. For each important edge, note the caller and callee locations, or the registration or config that connects them.
3. Read a nearby feature that already works, and the test that exercises it through the same path.
4. State the gap: expected behavior, observed behavior, and the first boundary where they differ. For new features, the gap is often a missing connection, not a broken function.

The owning layer is the one whose responsibility matches the missing behavior **and** that the real path reaches. Do not compensate in another layer (for example, patching a caller around a serializer bug). Stop reading once the active question is answered; reading unrelated files does not replace a missing call edge.

## 3. API and tool contract checklist

For every API, SDK method, standard-library function, CLI flag or config field that a step adds, changes or relies on, confirm from a version-matched source:

- The name, module or endpoint exists in the installed version and is not deprecated or removed.
- The signature: parameter names, types, required versus default values, units, allowed ranges and mutually exclusive options.
- Returns, raised errors, error codes and behavior on failure.
- Sync or async, streaming, pagination, retries, timeouts and resource cleanup.
- Permissions, authentication, side effects, idempotency, cost.

Mark an item not applicable only with a concrete reason; "could not find documentation" is not one. Do not transplant behavior from another language SDK, a newer version or a shortened doc example. Never insert a plausible-looking value, and never discover parameter names by provoking errors. Source priority and concrete commands are in `verification-recipes.md`.

When documentation and observed behavior disagree, first rule out a version mismatch, a wrapper, a fork or a local patch. A minimal reproduction shows only the case it ran; it does not override documented constraints.

## 4. Decompose into steps

Give each requirement an ID (R1...) and an acceptance condition an outside observer could check, such as entry point, input, expected behavior and limits. "Implement export" is not checkable; "`app export --format lines` writes one record per line, and empty input writes nothing" is.

Keep these separate: **requirements** (what the user authorized), **implementation decisions** (reversible means), **hypotheses** (unverified explanations), and **unknowns** (each with a named next probe). Do not promote a preferred implementation into a requirement, and do not invent thresholds or exact-output parity the user did not ask for.

Make each step one result plus one check. Split a step when it mixes unrelated behaviors, contains several unverified assumptions, or cannot be checked until future work is done. Labels like "understand everything" or "implement and test" are not steps.

Choose the next step in this priority order:

1. Contain unexpected side effects and get back to an understood working state, without discarding others' work.
2. Investigate the failed prerequisite of the active step.
3. Run a bounded experiment on an uncertainty that could invalidate the approach.
4. Do the earliest dependency-ready step, including its integration and check.

Keep one implementation step active. Read-only investigations can run in parallel. Parallel writers need isolated targets and an integration plan.

For new architecture, write a provisional interface first (inputs, outputs, failure behavior, ownership, resource lifetime, integration points) derived from the requirements and neighboring contracts. Revise it when evidence changes.

For underspecified decisions that change scope, cost, irreversibility or acceptance, look in existing requirements first, then ask one focused question. For reversible details within scope, follow project convention, note the assumption and keep going.

## 5. Edit and command discipline

- Make narrow patches. Confirm the expected old text before replacing it. If the match fails, re-read the file instead of widening the pattern.
- Edit only the files in the step's SCOPE. Updating a doc's "planned" label, tidying a helper, or changing a shared test utility's signature are separate changes. Recommend them in the report unless the user asked for them.
- Leave no residue: run Python with `-B` (or `PYTHONDONTWRITEBYTECODE=1`), put mutation experiments and scratch copies outside the project, and delete what you created. Before delivery, list the project's files and confirm that only intended files changed.
- Do not reformat unrelated code, rename broadly, update dependencies globally or upgrade frameworks without authorization.
- Before running a command, know its working directory, inputs, outputs, side effects, cost and timeout. Do not chain several unknown mutations into one command.
- Tests, builds, formatters, code generators, package managers, `npx`/`cargo`/`go` invocations and even imports can execute code, write files or use the network. Treat them as actions, not as read-only inspection.
- Install only into a project-isolated environment (for example a virtualenv, or `node_modules` using the existing lockfile). Respect the existing package manager.
- For large data, models or GPU work, estimate resources from sizes and shapes first, then start with a bounded sample.
- Commit, push, publish, deploy, delete, reset and external side effects are L3: they need explicit authorization.

After each modification, read the diff and confirm that only the intended locations changed: no stray files, no formatting damage, no accidental deletions.

## 6. Validation

Get the commands from project docs, scripts and CI config, not from habit. Record a baseline before changing anything, so that new failures can be told apart from pre-existing ones.

- **For bugs:** reproduce the failure first (an observable failing check or a minimal reproduction). If you cannot reproduce it, limit the claim.
- **Selection:** confirm that the tests you care about ran. Use verbose output or a collect/list mode, and check that a newly added test appears by name. Zero selected, all skipped, or "no tests to run" is not validation, even when the exit code is 0.
- **Independent oracle:** derive expected values from the requirement, a spec or a known example, never from the production helper under test. A failing test is a reason to investigate, not permission to edit its expectation.
- **Scope of a pass:** syntax checks prove syntax, and mocks cover only their own assumptions. Unit tests do not show that dispatch, config, serialization or persistence work end to end.
- **Staleness:** when later edits touch inputs to a result, mark that result stale and rerun the check before delivery.

When a step necessarily spans code and tests, finish that bounded unit before validating. You do not need to run tests after every line.

## 7. Reverts

Revert only changes clearly attributable to the current task. Do not restore whole files, reset the workspace, or delete and re-add files when that would overwrite the user's work or someone else's. If ownership cannot be separated, stop and report.

## 8. Interruption and resumption

Keep a checkpoint (see `records.md`) at meaningful points: requirement status, active step, open questions, disproven hypotheses, last checks, exact next action. After an interruption or compaction, re-read SKILL.md, the checkpoint, the relevant docs, the targets and the diff. Results whose dependencies changed are stale. Do not replay a disproven approach just because the failure is missing from a shortened summary.
