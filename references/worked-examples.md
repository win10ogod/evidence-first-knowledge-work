# Worked Examples: Evidence, Decisions, and Recovery

These are fictional teaching examples. Paths, identifiers, observations, and contracts below belong only to the examples. They are not real tool receipts, instructions to run a command, or proof about a user's project. Replace them with actual observations; never paste an example's PASS into a task record.

## E1. A new exporter that must be reachable

**Request:** add a line-record format to the existing export command; preserve the existing JSON output. The fictional project specification states that each record occupies one line and empty input produces no records.

**Observed reads:** the project manifest identifies its runtime; its format guide defines serialization; `command.py` selects formats through `registry.py`; `json_writer.py` owns serialization; an existing command test invokes the real dispatch path. Each observation has a real location and receipt in an actual run.

**Requirements:** R1: the public command selects the new format. R2: its output follows the format guide, including empty input. R3: existing JSON behavior remains compatible.

**Owning-layer decision:** a serializer belongs next to the existing writer. Selection belongs in the registry because the observed command reads that registry. Finding a function named `export` elsewhere would not establish either responsibility.

**Dependency-aware work:** inspect the writer interface and exact serialization API; add the bounded writer behavior and direct tests; integrate the registry connection and command test; exercise both formats through the command. Each independent modification re-reads its relevant documentation and targets before a refreshed contract.

Example completed pre-edit facts for the integration step:

```text
Step: S3; requirements: R1, R3
Purpose: connect the already checked writer to the existing command dispatch.
Source: the fictional project's format guide, revision r7, Registration section.
Current reads: registry.py and the existing command tests at current revision r12.
Proven gap: the command consults a registry that has no new-format entry.
Allowed targets: registry.py and the command integration test.
Invariant: existing JSON dispatch and output semantics stay unchanged.
Validation: invoke both formats through the documented test entry; inspect selected tests.
Stop: writer interface mismatch, unexpected target changes, or unrelated regression.
```

**Insufficient evidence:** "The new writer's unit tests pass, so export is finished." The command could still reject the format.

**Sufficient direction:** demonstrate the registry edge and run the real command test. If the writer passes but dispatch fails, keep R1 open and investigate the integration boundary. Do not rewrite the serializer merely because the visible error mentions export.

## E2. No documentation contains the new algorithm

**Request:** investigate and implement a lower-memory processing approach while preserving the specified output semantics.

**Known facts:** exact input/output contracts, supported iteration APIs, ownership rules, and a measured baseline from the current program. **Unknown:** whether the candidate design retains data across chunks.

A valid experiment records one hypothesis: retained working data remains bounded as more chunks are processed. It uses verified interfaces, a bounded authorized dataset, known instrumentation, a baseline, and explicit resource stop conditions. It compares increasing workloads that can reveal retained state; a single tiny sample cannot establish scaling behavior.

**Possible observation:** retained data grows with each chunk. This contradicts the bounded-retention hypothesis under the tested conditions. Preserve that result, inspect lifetime/accumulation, and revise the candidate before attempting the full workload.

**Invalid shortcut:** invent a memory number, treat one successful sample as proof, or guess an undocumented API parameter because the design is experimental.

**Valid progress:** the experiment rejects an approach and narrows the next question. Product edits dependent on that approach remain blocked, while a new evidence-backed experiment can proceed. The absence of a published solution recipe is not itself a reason to abandon the task.

## E3. Repeated patches do not fix a schema error

**Observed failure:** a consumer rejects a record. Hypothesis H1 attributes it to producer serialization; a version-matched trace contradicts H1. H2 attributes it to an omitted field; a second probe shows the field is present. Both attempts and observations remain in the failure ledger.

After these two evidence-backed failures, perform the diagnosis reset. Re-read the loaded consumer schema and actual adapter path. Suppose the new evidence reveals that the consumer loads an older schema through a wrapper. Investigate that version boundary before another producer patch.

**Invalid response:** try a third guessed field name, upgrade all dependencies, suppress the consumer exception, or alter tests to accept rejected records.

**Valid next step:** compare the wrapper's documented contract with the active schema, identify the authorized compatibility behavior, and form a new bounded contract. If a product compatibility choice remains unresolved, ask for that choice while preserving unrelated progress.

## E4. The target changes between reading and writing

A target was read at revision A. Another writer updates it to B. A revision-aware write rejects the old precondition.

Stop the overlapping write, read B and the relevant diff, and determine which changes belong to the other writer. Re-read the applicable specification, rebuild the patch against B, and validate the merged behavior. Do not force the old replacement, overwrite B with A, or label the conflict a transient error and blindly retry.

A current-state receipt is useful evidence, but only a write precondition or equivalent host check can detect some read/write races. Where the host lacks that mechanism, state the residual concurrency limitation and avoid overlapping writers.

## E5. Tests agree with the implementation but both are wrong

The fictional requirement says duplicate identifiers must be rejected. An implementation silently drops duplicates. Its test builds expected output using the same deduplication helper, so the test passes.

Read the original requirement before changing either file. Establish an independent expectation: duplicate input must trigger the documented rejection behavior. Add or correct a test that checks this observable behavior through the relevant entry point; then repair the implementation under fresh gates.

Do not cite the old passing test as evidence of correctness. The old test encoded the same misunderstanding. A review by the same model is not independent merely because it uses a different heading or role name.

## E6. Resume without redoing a disproven approach

The checkpoint records R1 VERIFIED, R2 OPEN, H1 contradicted by a retained-data probe, and the next action: inspect the accumulator lifetime. On resumption, read the checkpoint, skill, current documents, targets, and diff. Verify that R1's result still applies; invalidate it only if its dependencies changed.

Continue from the recorded next question. Do not re-run H1 because its failure is absent from a shortened conversation summary. If a needed receipt is inaccessible, mark it unavailable and reproduce the smallest necessary observation.
