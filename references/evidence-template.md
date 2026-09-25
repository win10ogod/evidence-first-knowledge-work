# Evidence and Resumable Task Record

Record inspectable working facts, not private chain-of-thought. Use one existing task note, issue, authorized scratch file, or conversation record. Identifiers below are labels to replace with actual evidence; they are not proof by themselves. Do not create repository tracking files without authorization.

## Task-level record: establish once, refresh when facts change

```text
TASK
- Original request and source:
- Deliverable and completion boundary:
- Target, branch/revision, runtime, dependency versions, time scope:
- Applicable instructions and their locations:
- Allowed side effects; forbidden resources; recovery constraints:
- Explicit exclusions:

REQUIREMENTS
- R1: source; observable acceptance; implementation/entry point;
      validation and independent expected-result source;
      status OPEN | ACTIVE | IMPLEMENTED | VERIFIED | BLOCKED.
- Keep every original requirement, including compatibility and resource limits.

PLAN
- S1: requirement IDs; single result/question; dependencies;
      allowed targets; expected observation; next action.
- Active implementation item:
- Open questions with next evidence-gathering actions:
- Material decisions and their supporting evidence:
```

Requirements cannot disappear when inconvenient. Implementation choices and hypotheses remain separate from user requirements. VERIFIED requires current, sufficient acceptance evidence; IMPLEMENTED is not completion.

## Before every independent step

```text
STEP S<n>
- Requirement IDs; purpose; dependency results:

G1 SOURCE / SPEC
- Source ID, original location, exact version, complete section re-read:
- Actual tool receipt or accessible source snapshot:
- Contract facts this evidence supports:
- Unknown/conflict; next probe; what remains blocked:

G2 CURRENT STATE
- Exact target and current revision, or observed absence for a new file:
- Current read receipt and complete semantic context:
- Relevant existing diff, call edges, configuration and tests read:
- Expected behavior versus observed behavior; proven gap; owning layer evidence:

G3 STEP CONTRACT
- Single intended change or experiment:
- Allowed files/resources and concrete maximum scope:
- Invariants; unrelated work to preserve:
- Verified operation/command, inputs, directory, costs and side effects:
- Checks; independent expected-result source; applicable boundary case:
- Stop conditions and precise recovery:
```

If required evidence is missing, mark the affected step BLOCKED before operating. A new experiment may investigate an unknown outcome only after its own interfaces, permissions, and bounds are verified. Do not retroactively manufacture a pre-edit record.

## After every step

```text
G4 OBSERVED CHANGE
- Actual operation and tool receipt:
- Actual changed targets and resulting revisions:
- Content/diff inspected; unexpected effects:

G5 VALIDATION
- Check ID; requirement IDs; exact command and selected cases:
- Independent expected result and its source:
- Observed result and output receipt:
- Status PASS | FAIL | NOT RUN; skipped cases and reasons:
- Revision/environment covered; remaining limitations:

FAILURE LEDGER (when applicable)
- Hypothesis ID and the failure it explains:
- Probe and observation:
- Supported | contradicted | unresolved:
- Repair attempts already made; next discriminating action:

CHECKPOINT
- Requirements still open/blocked:
- Last verified state and results now stale:
- Decisions, rejected approaches, and evidence locations:
- Active item and exact next read/probe:
- Resources or temporary changes still needing authorized cleanup:
```

A source receipt proves neither relevance nor comprehension. Check the actual passage. A tool result proves only what that tool observed. Never copy sample receipts or convert an expected result into PASS.

## Final delivery

```text
G6 DELIVERY
- Original requirement -> delivered behavior -> current acceptance evidence:
- Process compliance and any violations:
- Task outcome: complete | partial | blocked:
- Validation actually run, with scope and revision:
- FAIL / NOT RUN / stale results and unresolved requirements:
- Final changed files/resources; preserved work; remaining cleanup:
- Sources and reproducible next action for unfinished work:
```

A partial result can be valuable without being called complete. Trace-audit success, a green unit test, or completion of every planned step cannot replace verification of the original requested outcome.
