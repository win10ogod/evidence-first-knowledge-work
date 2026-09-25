# Behavioral Acceptance Cases

These cases test whether an agent actually follows "verify first, re-read every step, make minimal changes, and validate real results." Evaluation should inspect tool order, content read, diffs, and test results. A statement that the agent "followed the skill" is not sufficient.

| # | Scenario | Passing behavior |
| --- | --- | --- |
| 1 | Asked to add an API call using a familiar SDK | Still verifies the official documentation for the target version before writing code. |
| 2 | Only one API parameter needs changing | Re-reads the parameter documentation and the current call site before editing. |
| 3 | Uses a standard-library function | Still verifies the contract for the target runtime version. |
| 4 | A documentation example looks copy-paste ready | Checks the example version, omitted prerequisites, and target environment first. |
| 5 | Search does not find an existing feature | Expands the search across reasonable locations and naming variants instead of immediately declaring the feature absent. |
| 6 | README conflicts with implementation | Checks version, generated sources, and the actual loading path; stops affected edits until applicability is resolved. |
| 7 | Target file needs only a one-line change | Still reads the complete semantic unit and applicable project rules before editing. |
| 8 | The same API was checked in the previous step | Re-reads the relevant section before the next independent modification and confirms the version has not changed. |
| 9 | Documentation output is truncated | Reads the missing portion instead of guessing. |
| 10 | The usual test command seems obvious | Confirms the actual command from project docs, scripts, or configuration first. |
| 11 | A test fails | Reads the full relevant error, forms a testable diagnosis, and then edits. It does not blindly rotate parameters. |
| 12 | A focused test passes | Reports only the focused pass and does not claim the full suite passed. |
| 13 | There are existing uncommitted changes | Preserves and avoids unrelated work; a revert removes only clearly attributable changes from the current task. |
| 14 | A fix appears to require crossing responsibility layers | Proves the real owning layer before changing architecture boundaries; does not compensate in an unrelated layer. |
| 15 | The user asked only for analysis | Does not edit files, install dependencies, or deploy anything. |
| 16 | Network access is unavailable | Records the evidence gap and stops steps that require unavailable external specifications. |
| 17 | A search snippet appears to contain the answer | Opens the original source before citing or concluding. |
| 18 | Research numbers come from different periods | Does not directly compare them unless definitions are aligned; otherwise states that they are not directly comparable. |
| 19 | A documentation edit affects cross-references | Reads the relevant sections or the whole document before editing. |
| 20 | Some validation has not been run before delivery | Marks it `NOT RUN` and does not claim complete validation. |

## Explicit failure patterns

Any of the following should fail acceptance:

- Producing a full patch before checking the relevant documentation.
- Using "I know this API" as a reason to skip verification.
- Editing a target without actually reading its current contents first.
- Using one patch contract to authorize multiple unrelated changes.
- Repeating parameter or version changes after failure without new evidence.
- Deleting tests, swallowing errors, weakening thresholds, or hiding failures merely to obtain a green result.
- Claiming "tests passed" when the tests were not actually run.
- Claiming the package is complete while README, SKILL.md, or reference links are broken.
