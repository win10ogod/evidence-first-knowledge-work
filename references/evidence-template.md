# Evidence and Step Record

This template records inspectable working facts only. It does not require private chain-of-thought. It may be used in task notes, issues, pull-request descriptions, or the conversation.

## Task-level record

```text
TASK
- Request:
- Deliverable:
- Target/version/time scope:
- Allowed side effects:
- Applicable project rules:
```

## Before each step

```text
STEP <N>
G1 SOURCE / SPEC
- Source:
- Version/date:
- Exact section read:
- Supports:
- Unknown/conflict:

G2 CURRENT STATE
- Target read:
- Relevant implementation/data/tests read:
- Current diff/state:
- Proven gap:

G3 STEP CONTRACT
- Single purpose:
- Allowed files/resources:
- Maximum scope:
- Invariants:
- Operation/command:
- Validation:
- Stop conditions:
- Recovery:
```

If a required field is unknown, mark the step `BLOCKED` and obtain the missing evidence first. Do not execute the operation and fill the record afterward.

## After each step

```text
G4 OBSERVED CHANGE
- Actual operation:
- Actual files/resources changed:
- Diff/output inspected:
- Unexpected effects:

G5 VALIDATION
- Check:
- Result: PASS | FAIL | NOT RUN
- Evidence/output:
- Remaining limitation:
```

## Final delivery

```text
G6 DELIVERY
- Completed:
- Validation actually run:
- NOT RUN:
- Remaining blockers/limitations:
- Final changed files/resources:
- Sources used:
```

`PASS` may be recorded only for a check that was actually executed and observed. Expected behavior, self-written status text, or a statement that something "should work" is not a PASS.
