# Guided Development for Smaller or Less Reliable Models

Use this protocol for every engineering task, including open-ended work. The procedure is the default; confidence, task size, and model branding cannot disable it. It adds concrete actions to G0-G6 and grants no additional permissions.

## Contents

1. Turn the request into observable requirements.
2. Establish the actual execution path.
3. Build a dependency-aware plan.
4. Prepare one evidence-backed work packet.
5. Implement, inspect, and validate.
6. Integrate and preserve progress.

## 1. Turn the request into observable requirements

Read the user request and applicable project instructions. Give each requested outcome a stable identifier such as R1. Record the original source, an observable acceptance condition, exclusions, and any unresolved product decision. Use the task ledger in the evidence template.

An acceptance condition states what an external observer can check: entry point, input, expected behavior, and relevant limits. "Implement export" is insufficient. "The existing export entry point accepts the new format and produces a readable output" identifies an observable result. Specific data semantics must come from the task or an applicable specification, not from this example.

Keep these separate:

- **Requirement:** an authorized result or constraint.
- **Implementation decision:** a reversible means of achieving a requirement.
- **Hypothesis:** an unverified explanation or feasibility claim.
- **Unknown:** a question with a named next evidence-gathering action.

Do not turn a preferred implementation into an extra requirement. Preserve explicit performance, compatibility, privacy, or resource constraints, but do not invent thresholds or exact-output parity. Set the completion boundary before implementing. A prototype is an intermediate result unless the request explicitly asks only for a prototype.

For an underspecified product decision that changes scope, irreversible behavior, cost, or acceptance, retrieve existing requirements first; ask one focused question only if authorized sources cannot resolve it. For reversible implementation details within scope, choose a documented project convention, record the assumption, and continue. Do not seek approval for every local engineering decision.

## 2. Establish the actual execution path

Perform these reads before choosing an owning layer:

1. Read project rules, manifests, lockfiles, documented commands, and relevant existing changes. Identify the actual runtime and loaded dependency version.
2. Locate the user-facing entry point: command, route, public method, event handler, or job entry. Read its dispatch or registration code.
3. Trace the relevant input through configuration, validation, transformation, and output. For every important edge, record the caller and callee locations or the registration/configuration that connects them. A similarly named function is only a candidate.
4. Read a nearby working feature and the tests that actually exercise that path. Check test selection before running anything.
5. Form a minimal gap statement: expected behavior, observed behavior, and the first boundary at which they differ. New functionality may have an absent connection rather than a failing function.

An owning layer is supported when its responsibility matches the missing behavior and the real execution path reaches it. When two layers could own the change, inspect their existing contracts and use the decision playbook. Do not use file names, proximity, or the shortest patch as proof of ownership.

Stop expanding repository reads once the active question is answered by sufficient evidence. Still re-read the relevant documentation and current targets before every independent modification. Repeatedly reading unrelated files does not compensate for a missing call edge.

## 3. Build a dependency-aware plan

For each requirement, identify discovery, experiment, implementation, integration, and validation work that is actually necessary. Each work item names its requirement IDs, prerequisites, one concrete result, and a check of that result. Do not use "understand everything", "implement everything", or "test everything" as executable work items.

Split an item again when it contains unrelated behaviors, has several unresolved assumptions that need different experiments, or cannot be validated without unexplained future work. Several files may belong to one bounded logical change; file count alone does not define a useful step.

Keep one implementation item active by default. Independent read-only investigations may run in parallel. Parallel writers require isolated targets, explicit ownership, and an integration plan; model confidence is insufficient justification.

Select the next item in this order:

1. Contain unexpected side effects and restore an understood working state without discarding other people's work.
2. Investigate a failed prerequisite of the active item.
3. Resolve an uncertainty that could invalidate the proposed approach using a bounded experiment.
4. Complete the earliest dependency-ready requirement item, including its integration and validation.

When a chosen item is blocked, record exactly what it depends on and continue with independent authorized work. Revisit the task ledger after every completed item; do not let a successful local task silently become the whole deliverable.

For a new architecture, write a provisional interface contract before implementation: inputs, outputs, failure behavior, ownership, state/resource lifetime, and integration points. Derive it from requirements and neighboring contracts. Revise it when evidence changes, then re-check affected dependencies. Do not freeze an unsupported initial guess or rewrite unrelated architecture merely to simplify a local problem.

## 4. Prepare one evidence-backed work packet

Before each independent modification or repair, actually re-read:

- The relevant, version-matched specification section and applicable project rules.
- The exact current targets, required context, and relevant existing diff.
- The requirement and the latest failed or successful check that motivates this step.

Then complete the step contract. Bind every relied-on API to a source location and version. Bind every target to the read that established its current state. For a new target, record observed absence plus the parent directory's conventions. An evidence label without an inspectable source or tool receipt is incomplete.

The packet must answer: What changes? Why here? What must remain unchanged? What observable result would prove the step useful? What would stop it? A weak answer such as "fix the bug in the main file" requires more investigation.

For the first implementation in an unfamiliar project, read worked example E1. For a feasibility experiment, read E2. For retries or stale state, use E3 or E4. Examples are reasoning patterns, never evidence about the current repository.

## 5. Implement, inspect, and validate

Execute only the bounded operation. Inspect actual content and the diff immediately. Read-only inspection cannot be used to disguise formatter, import, install, build, or test side effects.

Verify the expected behavior through the entry point named in the contract. Also exercise the nearest applicable failure or boundary case and the existing behavior at risk. Select tests from actual requirements and project conventions. Do not add irrelevant test volume to manufacture progress.

Check that tests were discovered and executed; inspect assertions and fixture setup. A zero exit code with zero relevant tests does not validate the change. A mock validates only its covered boundary. Use the completion review before deciding what a passing test supports.

When a check fails, preserve the error and follow the decision playbook. A failing test is evidence for investigation, not permission to change its expected result. Do not continue to dependent work with an unvalidated prerequisite.

## 6. Integrate and preserve progress

Close a requirement only when its requested behavior works through the actual integration path and the associated checks apply to the final revision. Keep "implemented", "locally checked", "integrated", and "verified" distinct.

At each meaningful checkpoint, update one task record with requirements, active item, open questions, decisions and evidence, disproven hypotheses, changed targets, last checks, and the next concrete action. Use an existing task record or authorized scratch space; do not add tracking files to a repository without authorization.

After interruption or context compaction, re-read the skill, task record, applicable documents, current targets, and diff. Verify stale receipts again. A remembered plan or a summary from another agent cannot restore a gate to PASS.

Before delivery, run the completion review against every original requirement. Useful partial progress must be labeled partial, with blockers and preserved artifacts. Do not claim the model's capability improved merely because it followed this procedure once.
