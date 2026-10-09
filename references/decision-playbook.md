# Decision Playbook

Use the matching section when the next action is unclear. Each mutation, experiments included, still follows its level from SKILL.md.

## Contents

- D1. What kind of unknown is this?
- D2. Designing an informative experiment
- D3. A check failed
- D4. The target changed or another writer intervened
- D5. Stop, continue or escalate

## D1. What kind of unknown is this?

| Unknown | Next action | Stays blocked until resolved |
| --- | --- | --- |
| API name, parameter, type, default, version or side effect | Read version-matched docs, then installed source or type stubs (`verification-recipes.md`) | Any operation relying on that contract |
| Which code path or layer owns the behavior | Start at the real entry point and follow dispatch; read neighboring contracts and tests | Product edits in a guessed layer |
| Whether a new design is feasible | Run a bounded experiment (D2) using verified interfaces | Claims that the design works; dependent product changes |
| Sources disagree | Check versions, wrappers, generated code and runtime loading; record the conflict | Claims or edits that depend on the conflict |
| A product decision or permission | Look in existing requirements; ask one focused question if still open | The scope-changing or external operation only |
| Network access fails | Say so; use local, version-matched evidence | Steps that still need the unavailable evidence |

No published recipe for a solution is a reason to experiment, not to stop. An unknown API contract is never a "feasibility experiment" that justifies guessing arguments.

## D2. Designing an informative experiment

Write this down before running anything:

1. **Question:** one uncertainty, tied to a requirement.
2. **Hypothesis:** a claim that an observation could contradict.
3. **Known:** verified interfaces, input semantics, baseline behavior.
4. **Change:** the single variable under test, and the baseline it is compared to.
5. **Reading the result:** what supports the hypothesis, what contradicts it, and what leaves it unresolved. Use no invented success threshold.
6. **Bounds:** workspace, data, time, memory, cost, permissions, cleanup and stop conditions.
7. **Next:** how each outcome changes the plan.

Use the smallest experiment that is still representative, kept isolated from product state. A tiny success does not cover scale, concurrency, other platforms or failure modes; carry those limits forward.

## D3. A check failed

First preserve the command, working directory, versions, full error, which tests were selected, and the current diff. Then classify:

| Observation | Inspect next |
| --- | --- |
| Import, setup, permission or dependency error | The actual interpreter, the loaded package version and location, the documented setup. Do not upgrade everything. |
| Signature, type or schema mismatch | The exact interface called (and any wrapper), the version-matched contract, the arguments supplied. |
| Wrong value or behavior | The first point where the data diverges from the requirement, the fixture, and the independent expected value. |
| Unit tests pass but the public entry fails | Dispatch, registration, configuration, adapters, serialization, lifecycle. |
| Timeout, memory growth, hang | A bounded baseline, resource ownership and lifetime, input size. Stop unsafe runs. |
| Zero tests or only skipped tests | Discovery pattern, selection filters, skip reasons, whether assertions are reachable. |
| Patch did not apply, or the target changed | Re-read the current content and diff, and separate others' changes (D4). |

Record each explanation as **supported**, **contradicted** or **unresolved**, with its evidence and the next probe that would tell explanations apart. Do not retry a contradicted explanation without new evidence that changes it.

**Diagnosis reset:** after two evidence-backed repair attempts fail on the same symptom, make no further product edit until you have re-checked the requirement, the versions, the real execution path and the earliest divergence. This threshold is a project default, not a law. The reset may lead to a new experiment, a better-supported approach, or escalation with precise information. It is not a reason to abandon the task.

## D4. The target changed or another writer intervened

Invalidate the evidence for that target. Read the new content and its diff, identify the other changes, and rebuild your step against the new state. Use the tool's revision or precondition check when one exists; a read just before a write does not rule out a race. Never force-push, overwrite a newer version, widen a failed replacement, or restore an old copy to get past a conflict. If ownership cannot be separated, block the overlapping write and keep both versions.

## D5. Stop, continue or escalate

Continue evidence gathering and bounded local experiments while their own requirements are met. Pause only the actions that depend on the missing evidence or permission. When escalating, give the requirement, the observed facts, the probes already tried, the open question, and the exact artifact or decision you need. Do not ask the user to solve the whole design, and do not report success by quietly removing the uncertain part.

If the budget runs out, write a checkpoint and report partial completion instead of spending the rest on repeated failing attempts.
