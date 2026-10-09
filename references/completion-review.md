# Completion Review

Run this before final delivery, whenever tests pass but the user-visible result is uncertain, and when supervising another agent's work. A second pass by the same model, or a second agent with a different role name, is not independent evidence.

```text
- [ ] V1 Every requirement has an expected result from an independent source
- [ ] V2 Every claimed check really ran, selected the relevant tests, and covers the final revision
- [ ] V3 Each requirement works through its real entry point, including the relevant edge cases
- [ ] V4 The final diff contains only intended changes
- [ ] V5 Outcome and process are reported separately and honestly
```

## V1. Independent expected results

For each requirement, name where the expected behavior comes from: the request, a specification, a known input/output example, a documented invariant, or an independent reference. Do not compute expected values with the production helper under test. Do not change an expected value because the implementation returns something else; change it only when the requirement changed and the change is recorded. When no single correct output exists, check the stated constraints and demonstrable properties instead of inventing exact parity or arbitrary thresholds.

## V2. The check really happened

Read the command and its output. Confirm the relevant tests were selected by name, that their assertions were reached, and that the run used the revision and environment you are delivering. A skipped test is not a passed test. A zero-test run is not validation. If later edits touched a result's inputs, rerun the check.

## V3. The real path works

Connect each requirement end to end:

```text
requirement → implementation location → real entry point → check/oracle → observed result
```

Look for implemented-but-unregistered features, unused helpers, stale callers, mismatched schemas, and tests that bypass the integration point. Exercise the edge cases the contract implies (empty or invalid input, failure cleanup, duplicates, resource limits) where they are relevant. Never call a real paid, destructive or production endpoint just because a mock seems insufficient; report the gap instead.

## V4. Integrity of the diff

List the files that actually changed. Confirm there are no unrequested dependencies, unrelated refactors, removed or weakened tests, swallowed errors, leaked secrets or unexplained generated files. Correcting a test requires evidence that the old test contradicted the requirement. Check that documentation and examples match the final behavior.

## V5. Report outcome and process separately

- **Outcome:** VERIFIED requirements with their current evidence; OPEN or BLOCKED ones with their reason and next action. Claim overall completion only if every requirement is VERIFIED, or the user changed the scope.
- **Process:** which checks ran, at which revision, plus anything NOT RUN, stale or skipped, and any deviation from the rules.

Following the procedure does not prove capability, and the examples in this skill are fictional. Do not cite them as evidence about the user's code.
