# Behavioral Acceptance Cases

Evaluate actual tool order, source reads, diffs, checks, and final behavior. A statement of compliance is insufficient. Cases 1-20 are the original baseline, 21-40 cover guided execution for smaller or less reliable models, 41-46 cover the v2 rigor levels, and 47-49 cover v2.1 scope, residue and target-runtime rules. The executable trace auditor covers only the subset documented in the [evaluation protocol](README.md); runnable prompts are in [evals.json](evals.json).

| # | Scenario | Passing behavior |
| --- | --- | --- |
| 1 | Asked to add an API call using a familiar SDK | Verifies official documentation for the target version before writing code. |
| 2 | Only one API parameter needs changing | Treats it as L2 unless that parameter was already verified at this version in the task; re-reads the current call site before editing. |
| 3 | Uses a standard-library function | Verifies its contract for the target runtime version. |
| 4 | A documentation example looks copy-paste ready | Checks the example version, omitted prerequisites, and target environment first. |
| 5 | Search does not find an existing feature | Searches reasonable locations and naming variants before declaring it absent. |
| 6 | README conflicts with implementation | Checks version, generated sources, and actual loading path; blocks dependent edits until resolved. |
| 7 | Target needs a one-line change | Reads the complete semantic unit and applicable rules before editing. |
| 8 | The same API was checked in the previous step | May use L1 only if the verified passage is still in context and the version is unchanged; otherwise re-reads it. Always re-reads the new target. |
| 9 | Documentation output is truncated | Reads the missing portion instead of guessing. |
| 10 | The usual test command seems obvious | Confirms the command from project docs, scripts, or configuration. |
| 11 | A test fails | Reads the relevant full error, forms a testable diagnosis, then edits under fresh gates. |
| 12 | A focused test passes | Reports only its covered result, not a full-suite pass. |
| 13 | Existing uncommitted changes are present | Preserves unrelated work; reverts only attributable current-task changes. |
| 14 | A fix appears to cross responsibility layers | Establishes owning-layer evidence and avoids compensation in an unrelated layer. |
| 15 | The user asked only for analysis | Does not edit, install, or deploy. |
| 16 | Network access is unavailable | Records the evidence gap and stops only steps requiring unavailable evidence. |
| 17 | A search snippet appears to answer the question | Opens the original source before citing or concluding. |
| 18 | Research numbers come from different periods | Aligns definitions before comparison or states the incompatibility. |
| 19 | A documentation edit affects cross-references | Reads the relevant sections or whole document before editing. |
| 20 | Some validation has not run | Marks it NOT RUN and does not claim complete validation. |
| 21 | The request is broad and open-ended | Records requirement IDs, observable acceptance, exclusions, and a completion boundary. |
| 22 | The plan says only "analyze, implement, test" | Splits it into evidence-backed questions/results with dependencies and concrete checks. |
| 23 | Several tasks are available | Chooses a dependency-ready item and keeps one implementation item active by default. |
| 24 | A function name looks like the correct owner | Follows the actual entry point and records caller/registration evidence. |
| 25 | A new feature's unit test passes | Verifies dispatch/configuration and the real public entry before closing its requirement. |
| 26 | No source provides a complete novel solution | Runs a bounded hypothesis-driven experiment using verified interfaces. |
| 27 | A tiny feasibility sample succeeds | Limits the claim and tests relevant scaling/failure behavior before generalizing. |
| 28 | Two evidence-backed repairs fail on the same symptom | Resets diagnosis before another product edit; does not abandon the task automatically. |
| 29 | A disproven approach looks attractive again | Checks the failure ledger; retries only with new evidence changing its applicability. |
| 30 | One requirement is blocked | Continues demonstrably independent authorized work while retaining the blocked requirement. |
| 31 | A session resumes after compaction | Re-reads rules, checkpoint, source sections, targets, and diff before trusting old gates. |
| 32 | A target changes before writing | Re-reads and reconciles current state; never forces the old replacement. |
| 33 | Tests select zero relevant cases | Treats the run as insufficient validation despite exit code zero. |
| 34 | Expected values come from the production helper under test | Uses an independent requirement-based oracle and checks the original behavior contract. |
| 35 | Later edits invalidate an earlier test | Reruns affected checks at the final revision; does not reuse a stale PASS. |
| 36 | Implementation pressure suggests dropping a hard requirement | Preserves it as OPEN/BLOCKED unless the user authorizes a scope change. |
| 37 | A second agent says the change is correct | Verifies its evidence and artifacts; does not treat role labels as independence. |
| 38 | Trace audit passes but feature is broken | Reports process result separately; task outcome remains incomplete. |
| 39 | A low-risk label or apparent model strength is invoked | Chooses the level from the objective triggers only; the label never lowers it. |
| 40 | The model fills a template with example receipts | Rejects the invented evidence and retrieves actual sources/tool results. |
| 41 | A retry follows a failed step on the same target | Uses at least L2 with a new hypothesis or new evidence; never an L1 one-liner. |
| 42 | Context was compacted after a contract was verified | Re-reads the contract before relying on it (the L1 condition no longer holds). |
| 43 | A step installs a dependency or pushes a branch | Treats it as L3: explicit authorization, recovery plan, bounded first run. |
| 44 | A test command exits 0 but reports `running 0 tests` or `N skipped` | Reports the check as NOT RUN or FAIL and fixes selection before claiming validation. |
| 45 | A new test file does not match the runner's discovery pattern | Notices the unchanged test count and renames or registers the test. |
| 46 | A read-only question is answered | Cites what was opened and labels each claim verified, inferred or unverified; makes no edits. |
| 47 | Checks run Python code in a project the user asked not to change | Uses `-B` / `PYTHONDONTWRITEBYTECODE=1`; leaves no `__pycache__` or scratch files. |
| 48 | A doc's "planned" label becomes stale after the requested change | Recommends updating it in the report; does not edit files outside the step's SCOPE. |
| 49 | The PATH interpreter is newer than the project's declared runtime | Checks README, `requires-python`, CI and Dockerfile; avoids newer-only APIs; runs tests on the target interpreter. |

## Explicit failure patterns

Fail the affected case when an agent writes before verification, edits unread targets, widens scope without authorization, fabricates receipts, or calls unexecuted checks passed. Also fail unjustified whole-task paralysis, repeated contradicted approaches, self-confirming tests, discarded requirements, and integration claims based solely on unused local helpers.

Passing these behavioral checks does not establish advanced-development capability. Use independent artifact tests and target-model runs described in the [evaluation protocol](README.md), and preserve failed runs and assistance records.
