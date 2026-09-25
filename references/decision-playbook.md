# Evidence and Recovery Decision Playbook

Use the matching situation below when the next action is unclear. Every mutation, including an experimental mutation, still passes G1-G3. These are working rules, not a claim that every problem has a known solution.

## D1. Which kind of unknown is this?

| Situation | Next action | What remains blocked |
| --- | --- | --- |
| API name, parameter, type, version, default, or side effect is unknown | Read exact-version official documentation, then official source/types or packaged documentation if needed. | Operations relying on the unknown contract. |
| The code path or owning layer is unknown | Start at the real entry point, follow dispatch/calls, inspect neighboring contracts and tests. | Product edits at a guessed layer. |
| A new design's feasibility is unknown | Define a falsifiable hypothesis and a bounded experiment using verified interfaces. | Claims that the design already works, and dependent production changes. |
| Sources disagree | Check versions, wrappers, generated sources, runtime loading, and applicable requirements; record the conflict. | Definite claims or edits depending on the unresolved conflict. |
| A material product decision or permission is missing | Check existing authorized requirements, then ask a focused question if necessary. | The affected scope-changing or externally consequential operation. |
| Network access fails | Report the failure; read available version-matched local evidence. Observe any governing online-verification requirement. | Any step whose required evidence remains unavailable. |

A missing solution recipe does not by itself block investigation. A missing API contract cannot be reclassified as a feasibility experiment to justify guessing arguments.

## D2. How to design an informative experiment

Write a short experiment contract before executing it:

1. **Question:** one uncertainty linked to a requirement.
2. **Hypothesis:** a claim that can be contradicted by an observation.
3. **Evidence already known:** verified interfaces, input semantics, and baseline behavior.
4. **Controlled change:** the variable being tested and the baseline being compared.
5. **Observation rule:** what outcome supports, contradicts, or leaves the hypothesis unresolved. Do not invent a success threshold absent from requirements or an explicit experiment rationale.
6. **Bounds:** workspace, data, memory/time/cost envelope, permissions, cleanup, and stop conditions.
7. **Next action:** how each possible result changes the plan.

Use the smallest representative experiment that answers the question. Keep prototypes isolated from product state when possible. Changing several independent variables together makes causal interpretation uncertain; use separate probes unless coupling is justified and recorded.

A small experiment can reject an approach without proving a replacement. Do not generalize a tiny successful sample to untested scale, concurrency, platforms, or failure modes. Carry the limitation forward.

## D3. A check failed: choose the next read, not the next random patch

First preserve the command, working directory, relevant versions, original error, actual test selection, and current diff. Classify from evidence:

| Observation | Inspect next |
| --- | --- |
| Import, setup, permission, or dependency failure | Actual interpreter, loaded package location/version, documented setup, and missing resource. Do not immediately upgrade everything. |
| Signature, type, or schema mismatch | Exact called interface, wrapper, official version-matched contract, and supplied arguments. |
| Wrong value or behavior | First divergence from the requirement, input fixture, transformation, and independent expected result. |
| Focused tests pass but public entry fails | Dispatch, configuration, registration, adapters, serialization, and lifecycle boundaries. |
| Timeout, memory growth, or stalled work | A bounded baseline, resource ownership/lifetime, input size, and verified instrumentation. Stop unsafe runs. |
| Zero relevant tests or skipped-only execution | Selection filters, discovery rules, fixture collection, skip reasons, and assertion reachability. |
| Patch mismatch or target changed | Re-read current content and diff; separate other work before rebuilding the patch. |

Record each attempted explanation as **supported**, **contradicted**, or **unresolved**, with evidence and the next discriminating probe. Do not replay a contradicted explanation unless new evidence changes its applicability.

After two distinct evidence-backed repair attempts fail on the same symptom, perform a mandatory diagnosis reset before another product edit: re-check requirements, versions, the execution path, and the earliest divergence. This is a procedural default chosen by this project, not a scientific limit or a reason to abandon the task. A reset may select a different experiment, a better-supported approach, or an escalation with precise missing information. Identical retries already require a new diagnostic reason even before this threshold.

## D4. State changed or another writer intervened

Invalidate evidence for every dependent target. Read the new target and related diff, identify the other changes, and revise the step contract. Use a tool's revision/precondition check when available. A read just before a write cannot guarantee that no concurrent change occurs afterward.

Do not force-push, overwrite a newer blob, widen a failed replacement, or restore an entire old file to bypass a conflict. If ownership cannot be separated, block the overlapping mutation and preserve both versions. Disjoint work can continue after its independence is checked.

## D5. Stop, continue, or escalate

A high-risk label adds authorization, recovery, and environment checks; a low-risk label never removes documentation reads or validation.

Continue authorized evidence gathering and bounded local experiments while their own gates pass. Pause only actions that depend on missing evidence or permissions. Escalate with the precise requirement, observed facts, attempted probes, remaining question, and the artifact needed to proceed. Do not demand that the user solve the whole architecture, and do not report success because the uncertain work was removed.

If the task budget is exhausted, preserve a resumable checkpoint and report partial completion. Do not spend the remaining budget on repeated failing attempts or a false completion claim.
