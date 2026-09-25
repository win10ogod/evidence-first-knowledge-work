# Coding, API, and Engineering Operations Protocol

This file is the engineering branch of `SKILL.md`. It applies equally to code examples, patches, startup commands, tests, and configuration. Standard-library usage, familiar APIs, small changes, and urgent fixes are not exemptions.

## C1. Read the project before declaring a gap

Before editing, inspect:

| Area | Evidence required |
| --- | --- |
| Project rules | Applicable AGENTS.md, CLAUDE.md, subdirectory instructions, and task-specific skills. Never rewrite governing rules merely to permit a change. |
| Specifications and operating docs | README, design or requirement docs, development and testing instructions, configuration docs, and migration guidance. Confirm applicability. |
| Environment and versions | Project manifests, lockfiles, runtime, relevant package versions, and service versions. Distinguish declared, locked, and actually loaded versions. |
| Existing work | Current branch, relevant uncommitted changes, untracked targets, and user-owned edits. Without Git, use tool reads and recoverable snapshots to establish state. |
| Existing capability | Search related implementations, aliases, flags, wrappers, registries, generated sources, and alternative paths. Trace necessary upstream and downstream calls. |
| Tests | Test entry points, relevant cases, fixtures, environment requirements, and observable pre-existing failures. |

Do not conclude that a repository lacks a feature merely because one keyword search returned no result. Search reasonable candidate locations and naming variants. Check ignored directories, submodules, generated files, or external packages when they may own the behavior. This does not require blindly reading every file in the repository.

Read at least the complete semantic unit, file-level configuration, and necessary context around any edit target. If a change crosses sections or a whole-file rewrite is planned, read the entire file first. If tool output is truncated, continue reading. Never invent the missing portion.

Before creating a new file, confirm that the target does not already exist, inspect directory conventions, and search for similar implementations. If existing functionality can satisfy the request, use it correctly instead of creating a duplicate subsystem.

When project documentation is absent, record what was checked and continue with relevant source, schemas, type declarations, and tests. If the contract still cannot be determined, stop the affected implementation.

## C2. Verify every API, regardless of familiarity

For every API, SDK method, standard-library function, CLI flag, or configuration field that this step adds, changes, or relies on semantically, verify the version-matched official documentation. At minimum, check every item that can affect correctness:

- Exact name, module/package/endpoint, existence in the target version, and deprecation status.
- Signature, parameter names, types, required/default values, units, legal ranges, exclusions, and companion requirements.
- Return type, response schema, exceptions, error codes, and failure semantics.
- Synchronous/asynchronous behavior, streaming/non-streaming behavior, pagination, retries, timeouts, and resource lifetime.
- Permissions, authentication, state changes, idempotency, and relevant cost or safety constraints.

An item may be marked not applicable only when there is a concrete reason. Failure to find documentation is not a reason to mark it N/A. Do not transplant behavior from another language SDK, a similar method, a newer version, or an abbreviated example into the target environment without verification.

If official documentation does not answer the question, inspect version-matched official source, type declarations, or packaged documentation. CLI help may be used to confirm the installed version's interface, but first verify that invoking help itself does not trigger actual work. Do not assume every `--help` path is side-effect free.

When documentation conflicts with observed behavior, first distinguish version mismatch, private forks, wrappers, and genuine defects. Build a controlled minimal reproduction when necessary. A successful experiment with one input does not establish the complete contract and does not automatically override official constraints.

Never insert a plausible-looking parameter value because the real one is unclear. Do not discover parameter names by repeatedly provoking errors.

## C3. Pre-edit contract

Before the first modification, produce this compact record. Refresh the changed fields before every independent step and attach the documentation and current-state evidence for that step.

```text
RECONNAISSANCE
- Existing implementation: location and verified behavior
- Existing flags/config: relevant switches and settings
- Call path: required upstream/downstream path
- Relevant tests: real test entry points and current status
- Proven gap: specific difference between current state and valid request

BOUNDARY
- Failing layer: location of the defect; for new functionality, the new responsibility
- Owning layer: module/layer that should own the change
- Forbidden layers to modify: boundaries that must remain untouched

PATCH CONTRACT
- Files allowed to change: explicit files or bounded generated output
- Maximum file count: concrete limit for this step
- Invariants: existing behavior, interfaces, data, and user work that must not change
- Documentation evidence: version-matched source and section re-read for this step
- Current-state evidence: latest content/diff read for this step
- Validation commands: verified command, working directory, and required environment
- Expected observations: observable outcomes tied to the request
- Side effects and recovery: impact boundary, stop condition, and precise recovery method
```

Required fields may not be blank, deferred with "check later," unknown, or filled with vague slogans. If a field truly does not apply, state the concrete reason.

Set file-count limits and acceptance methods from the actual task. Do not expand the change merely to complete the template, and do not invent bitwise, hash, or value-for-value parity requirements that the user did not request.

The contract is an execution boundary, not new user authorization. Scope details may be updated after gathering more evidence, but new features, breaking changes, additional cost, or access to unauthorized resources require appropriate authorization.

## C4. Minimal edits and command control

One logical change may include the necessary code, tests, and matching documentation, but every target must be read before editing. One patch contract may not authorize unrelated refactors.

- Prefer narrowly targeted patches. Verify the expected old content before replacement. If a match fails or the file changed, re-read the target instead of widening the replacement blindly.
- Do not overwrite unknown content, remove user changes, reformat unrelated code, globally update dependencies, or upgrade frameworks without authorization.
- If ownership is wrong, return to diagnosis. Do not compensate for an architecture/backend/loader/optimizer/kernel problem by changing another layer.
- Install only in an authorized project-isolated environment. For Python, use a virtual environment and do not mutate system Python. Respect the project's existing tools and lockfile.
- Before executing a command, verify the full command, working directory, inputs, outputs, credential scope, cost, timeout, and possible side effects. Do not chain multiple unknown mutations into one command.
- Tests, builds, formatters, code generators, package managers, and imports can execute code or mutate files. Verify their actual behavior and output locations first.
- For large datasets, models, or GPU workloads, estimate resource requirements from file size, shape, dtype, and verified tool behavior. Start with bounded or sampled checks. Stop if a safe resource envelope cannot be established.
- Without explicit authorization, do not commit, push, publish, deploy, delete resources, reset a workspace, or call a service with real external side effects.

After each modification, immediately read the resulting content and diff. Confirm that only the intended location changed and that no unplanned files, formatting damage, or accidental deletions appeared.

## C5. Validation and repair loop

Derive validation commands from project documentation, existing scripts, test configuration, and version-matched tool documentation. Do not assume that a familiar command is correct for every project.

Run the validation appropriate to the step's risk and existing acceptance contract: syntax or parsing checks, formatting, type checks, focused tests, regression tests, and required integration tests. For defects, establish an observable failure or controlled minimal reproduction before confirming the repair. If reproduction is impossible, limit the conclusion accordingly.

Record the baseline before testing. Separate pre-existing failures, newly introduced failures, missing-environment failures, skipped checks, and checks not run. A local partial pass is not a full pass. Offline mocks are not real-service validation.

When one bounded change necessarily spans code and tests, complete that bounded unit before validation. You do not need to run tests after every line, but each file must still be read before editing.

On failure, read the full relevant error and current state before changing anything. Confirm a testable hypothesis. Do not repeat the same run without new evidence or a different diagnostic purpose. Every repair attempt returns through G1-G3.

Only move into a dependent next step after the current step passes. Before delivery, rerun validation affected by later changes and review the final diff against the original request.

A precise revert may remove only changes clearly attributable to the current work. Do not use whole-file restoration, global reset, or delete/re-add flows that overwrite other work. If change ownership cannot be separated safely, stop the revert.
