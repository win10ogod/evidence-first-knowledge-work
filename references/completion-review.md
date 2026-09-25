# Completion and Independent Verification Review

Run this review before G6 and when focused tests appear successful but the user-visible outcome is uncertain. It is also the checklist for a supervising agent. A second agent, or a second pass by the same model, does not automatically supply independent evidence.

## V1. Establish the expected result independently

For every requested outcome, name the source of the expected behavior: original requirement, applicable specification, known input/output example, documented invariant, or independent reference implementation. Record expected results before adapting the implementation to a failing test.

Do not compute a test's expected value by calling the same production helper being tested. Do not change an expected value just because the current implementation returns something else. If the requirement genuinely changes, record the authorized change and re-check affected tests.

Where no single correct output exists, use the requested constraints and demonstrable properties: valid interfaces, preserved data, bounded resources, failure handling, and working integration. Do not invent byte-identical parity, arbitrary benchmark thresholds, or subjective scoring requirements.

## V2. Check that the check really happened

Read the test command and its result. Confirm relevant tests were selected, assertions reached, and results apply to the revision and environment being delivered. Distinguish PASS, FAIL, NOT RUN, and BLOCKED; a skipped test is not a passed test.

A syntax check proves syntax. A mock checks behavior under the mock's assumptions. A unit test covers the unit it exercised. None alone proves that dispatch, configuration, adapters, serialization, persistence, or cleanup works end to end.

When later changes affect inputs, code, dependencies, fixtures, or configuration used by a result, mark the result stale and rerun the affected check. Keep unrelated verified results when their independence is established.

## V3. Verify the real path and boundaries

For each requirement, connect:

```text
requirement -> implementation location -> real entry point -> test/oracle -> observed result
```

Look for implemented-but-unregistered features, unused helpers, stale callers, mismatched schemas, and tests that bypass the integration boundary. Run the actual public path in an authorized test environment when required to demonstrate the requested behavior. Never call a real paid, destructive, or production endpoint merely because a mock is insufficient.

Check the applicable negative or boundary cases derived from the contract. Examples include empty input, invalid input, failure cleanup, duplicate events, or resource bounds, but only use cases relevant to the task. Do not copy every example into every project.

Preserve existing behavior explicitly required by the task or project. Compare compatible baselines under the same relevant conditions. Do not erase unrelated user changes to make a comparison simpler.

## V4. Check the integrity of the work

Inspect the final diff and list actual changed files. Confirm no unrequested dependencies, framework upgrades, unrelated refactors, removed tests, disabled assertions, swallowed errors, leaked secrets, or unexplained generated files appeared.

A legitimate test correction requires evidence that the old test contradicted the applicable requirement, plus independent verification of the new expectation. Moving a failure out of the test suite is not a correction.

Check documentation, configuration examples, and cross-references against actual behavior. Examples in this skill are fictional; do not cite them as proof about a user's code.

## V5. Decide completion without dropping scope

Keep two judgments separate:

- **Process compliance:** required reads, authorization, bounded edits, and honest reporting were observed.
- **Task outcome:** the original requested behavior and constraints were actually satisfied.

A perfectly documented failure is still an incomplete task. Working code with a skipped mandatory safety gate is still a process violation. Report both honestly.

Mark a requirement VERIFIED only when its acceptance evidence is current and sufficient. Mark remaining requirements OPEN or BLOCKED with their dependency and next action. Claim overall completion only when all required outcomes are verified, or when the user has explicitly changed the scope. Report exclusions that were already part of the agreed task separately from unfinished work.

Do not claim that this skill makes a particular model capable of advanced development without evaluation on that model and task distribution. Structural checks and synthetic trace tests do not measure that capability.
