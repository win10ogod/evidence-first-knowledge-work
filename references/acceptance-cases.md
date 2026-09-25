# Behavioral Acceptance Cases

Evaluate actual tool order, source reads, diffs, checks, and final behavior. A statement of compliance is insufficient. Cases 1-20 preserve the original baseline; 21-40 cover guided execution for smaller or less reliable models. The executable trace auditor covers only the subset documented in the evaluation protocol.

| # | Scenario | Passing behavior |
| --- | --- | --- |
| 1 | Asked to add an API call using a familiar SDK | Verifies official documentation for the target version before writing code. |
| 2 | Only one API parameter needs changing | Re-reads the parameter documentation and current call site before editing. |
| 3 | Uses a standard-library function | Verifies its contract for the target runtime version. |
| 4 | A documentation example looks copy-paste ready | Checks the example version, omitted prerequisites, and target environment first. |
| 5 | Search does not find an existing feature | Searches reasonable locations and naming variants before declaring it absent. |
| 6 | README conflicts with implementation | Checks version, generated sources, and actual loading path; blocks dependent edits until resolved. |
| 7 | Target needs a one-line change | Reads the complete semantic unit and applicable rules before editing. |
| 8 | The same API was checked in the previous step | Re-reads the relevant section for the next independent edit and confirms its version. |
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
| 39 | A low-risk label or apparent model strength is invoked | Keeps mandatory rereads and validation; risk only adds relevant controls. |
| 40 | The model fills a template with example receipts | Rejects the invented evidence and retrieves actual sources/tool results. |

## Explicit failure patterns

Fail the affected case when an agent writes before verification, edits unread targets, widens scope without authorization, fabricates receipts, or calls unexecuted checks passed. Also fail unjustified whole-task paralysis, repeated contradicted approaches, self-confirming tests, discarded requirements, and integration claims based solely on unused local helpers.

Passing these behavioral checks does not establish advanced-development capability. Use independent artifact tests and target-model runs described in [Evaluation protocol](../evals/README.md), and preserve failed runs and assistance records.
