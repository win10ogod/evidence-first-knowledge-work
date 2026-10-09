# Worked Examples

These examples are fictional. Their paths, revisions and results are not tool receipts and say nothing about the user's project. Use them as patterns only; never paste their content into a real record.

## Contents

- E0. Choosing the level for each step
- E1. A new export format that must be reachable
- E2. No documentation describes the new algorithm
- E3. Repeated patches do not fix a schema error
- E4. The target changes between read and write
- E5. Tests agree with the implementation, but both are wrong
- E6. Resuming without repeating a disproven approach

## E0. Choosing the level for each step

| Step | Level | Why |
| --- | --- | --- |
| Answer "what does `--dry-run` do in our deploy script?" | L0 | Read-only. Cite the script lines you read. |
| Rename a local variable inside a function already read in full | L1 | Local edit; no new external contract. |
| Replace `requests.get(url)` with `requests.get(url, timeout=10)` | L2 | Introduces reliance on a parameter not yet verified for the installed version. |
| Same `timeout` change in a second module, later in the same task, docs still in context | L1 | The contract was verified at this version in this task. Still re-read the second target before editing. |
| The previous attempt failed, try again | L2 | Retries are always at least L2: new evidence or hypothesis required. |
| `pip install -U requests` | L3 | Changes dependencies; needs authorization and a recovery path. |
| "It's just a one-liner" | Decided by the triggers | Size and confidence never lower the level. |

## E1. A new export format that must be reachable

**Request:** add a `lines` format to the existing `export` command; JSON output must not change. The project's format guide says each record is one line, and empty input produces no output.

**Reconnaissance:** the manifest gives the runtime. `cli.py` selects writers through `REGISTRY` in `registry.py`, and `writers.py` owns serialization. `tests/test_cli.py` invokes the command through its real dispatch path.

**Requirements:** R1, the public command accepts `--format lines`. R2, the output follows the guide, including empty input. R3, JSON behavior is unchanged.

**Owning layers:** serialization goes in `writers.py`, beside the JSON writer. Selection goes in `registry.py`, because that is what `cli.py` reads. A function called `export_all` elsewhere would not establish either responsibility.

**Steps:** S1 (L2) adds the writer and its direct tests. S2 (L2) registers it and adds a CLI test. S3 runs both formats through the CLI.

```text
S2 [L2] R1,R3 — register "lines" writer in REGISTRY
DOC   docs/formats.md §Registration (HEAD, read now)
STATE registry.py full file, tests/test_cli.py (read now)
GAP   cli.py looks up REGISTRY[args.format]; no "lines" key
SCOPE registry.py, tests/test_cli.py | KEEP "json" entry and output
CHECK python -m unittest tests.test_cli -v → test_lines_format listed, all pass
STOP  writer signature differs from registry contract | target changed
```

**Insufficient:** "The writer's unit tests pass, so export is done." The command could still reject `--format lines`.

**Sufficient:** show the registry edge, then run the CLI test and confirm it was selected. If the writer passes but dispatch fails, R1 stays OPEN; investigate the integration point instead of rewriting the serializer.

## E2. No documentation describes the new algorithm

**Request:** reduce the memory used by processing while keeping the output semantics. **Known:** the input/output contract, the supported iteration API, and a baseline memory measurement. **Unknown:** whether chunked processing keeps data across chunks.

**Experiment:** one hypothesis (retained memory stays bounded as the number of chunks grows), verified interfaces, a bounded dataset, a known measurement method, a baseline, and stop conditions for resources. Compare several increasing workloads; one tiny sample cannot reveal growth.

**Observation:** retained data grows with each chunk. Under the tested conditions this contradicts the hypothesis. Record the result, inspect the lifetime of the accumulator, and revise the design.

**Invalid shortcuts:** inventing a memory figure, generalizing from one sample, or guessing an undocumented parameter because the work is "experimental". **Valid progress:** the experiment rejected one design and narrowed the next question.

## E3. Repeated patches do not fix a schema error

A consumer rejects a record. H1 blames producer serialization; a trace at the matching version contradicts it. H2 blames a missing field; a probe shows the field is present. Both go in the failure ledger.

Two evidence-backed attempts have failed, so reset the diagnosis. Re-reading the consumer's loading path shows it loads an older schema through a wrapper. Investigate that version boundary before any further producer patch.

**Invalid:** guessing a third field name, upgrading every dependency, suppressing the consumer's exception, or loosening the tests.

## E4. The target changes between read and write

You read the target at revision A. Another writer updates it to B, and your revision-checked write is rejected. Read B and the diff from A to B, identify the other writer's changes, rebuild the patch against B, and validate the merged result. Do not force the old replacement or treat the rejection as a transient error to retry. Where the host has no write precondition, state the remaining race risk.

## E5. Tests agree with the implementation, but both are wrong

The requirement says duplicate IDs must be rejected. The implementation silently drops duplicates, and its test builds the expected output with the same deduplication helper, so the test passes. Go back to the requirement: duplicate input must raise the documented error. Write a test against that behavior through the entry point, watch it fail, then fix the implementation. The old green test is not evidence; it encoded the same misunderstanding.

## E6. Resuming without repeating a disproven approach

The checkpoint says R1 VERIFIED, R2 OPEN, H1 contradicted by a retained-memory probe, and next action "inspect accumulator lifetime". On resumption, re-read SKILL.md, the checkpoint, the docs, the targets and the diff. Confirm R1's check still applies. Then continue from the recorded next action. Do not rerun H1 just because a shortened summary dropped it. If a receipt is no longer available, reproduce the smallest observation needed.
