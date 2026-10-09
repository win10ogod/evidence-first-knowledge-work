# Records: Ledger, Failures and Checkpoints

Use these formats when work spans several steps or sessions. Keep them in the conversation, an existing task note or issue, or authorized scratch space. Do not add tracking files to a repository unless the user wants them. Records hold observed facts and decisions, not private reasoning.

Labels such as `S3` or `H1` are names, not proof. Every field must point to a real read or tool result from this task.

## Requirement ledger

Write it once at the start and update it after every step.

```text
TASK  <original request, quoted or linked> | deliverable | exclusions | authorization limits
ENV   <branch/HEAD>, <runtime + key dependency versions>, instruction files read

R1  <observable acceptance: entry point, input, expected behavior>
    check: <command or procedure> | oracle: <where the expected value comes from>
    status: OPEN | ACTIVE | IMPLEMENTED | VERIFIED | BLOCKED(<what would unblock>)
R2  ...

NEXT  S<n>: <one result> (depends on S<m>)
OPEN  <question> → <next probe>
```

Requirements never disappear because they are inconvenient. Only the user can change scope. IMPLEMENTED is not VERIFIED: VERIFIED needs a current check through the real entry point.

## Step receipts

Use the L1 and L2 receipt formats from SKILL.md. For L3 steps, add two lines:

```text
AUTH     <who authorized what, where>
RECOVER  <exact undo procedure and its limits>
```

## Failure ledger

```text
H1  <hypothesis about failure F1>
    probe: <what was run or read> → <observation>
    verdict: supported | contradicted | unresolved
    attempts: <repair attempts made under this hypothesis>
    next: <discriminating probe>
```

Check this ledger before every retry. A contradicted hypothesis may be revisited only with new evidence that changes its applicability.

## Checkpoint

Write a checkpoint before stopping, at natural milestones, and whenever context is getting long.

```text
CHECKPOINT <time or revision>
- Requirements: R1 VERIFIED (check X @rev), R2 OPEN, R3 BLOCKED(<reason>)
- Stale results: <checks whose inputs changed since they ran>
- Rejected approaches: H1 contradicted by <evidence location>
- Changed files: <list>; temporary resources needing cleanup: <list>
- Next action: <exact read or probe>
```

On resumption, read the checkpoint, then re-read SKILL.md, the relevant docs, the targets and the diff. Results whose dependencies changed are stale.

## Final delivery

```text
OUTCOME  complete | partial | blocked
  R1 → <delivered behavior> → <current evidence>
  R2 → OPEN: <what remains, next action>
PROCESS  checks run (scope, revision) | NOT RUN / stale | any rule deviations
CHANGED  <files/resources>; preserved: <unrelated work left untouched>
SOURCES  <the sources the result depends on>
```
