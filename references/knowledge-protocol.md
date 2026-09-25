# Research, Analysis, and Technical Documentation Protocol

This file applies to research, fact checking, data analysis, technical Q&A, API explanations, and documentation maintenance. The core rule is the same as in `SKILL.md`: obtain locatable evidence before writing conclusions that depend on it, and re-check applicable sources and current state before every independent conclusion or edit step.

## K1. Define the question and time scope first

Before starting, confirm:

- Whether the task asks for facts, comparison, derivation, summary, recommendation, or document modification.
- The subject, version, time range, geography, dataset, and terminology.
- Which claims are time-sensitive and which can rely on stable specifications or mathematical derivation.
- The requested output format and the allowed scope of inference.

If a term, version, or premise is ambiguous and would materially affect the answer, verify it first. When reliable sources can resolve the ambiguity, investigate directly rather than asking the user to repeat information unnecessarily.

## K2. Search locates evidence; original sources support claims

Search-result snippets, AI summaries, and third-party retellings are primarily discovery aids. Important claims should be grounded as close to the original fact as possible:

1. Formal specifications, official documentation, official source code, or official announcements.
2. Original research papers, datasets, statutes, standards, or first-party statistics.
3. High-quality secondary sources only when first-party material is insufficient for context.

After opening a source, record its date, version, applicable subject, and the claim it directly supports. Do not substitute a homepage, index page, or search snippet for the relevant passage.

## K3. Separate fact, inference, and unknown

Every material conclusion should fit one of these categories:

- **Directly supported**: explicitly stated by the source or directly visible in the data.
- **Evidence-based inference**: derived from verified premises; the scope and assumptions must be stated.
- **Unverified**: evidence is insufficient, conflicting, or outside the covered population/version/time range.

Do not present an inference as if it were quoted from the source. Do not generalize one case to an entire population, version family, or time range without supporting evidence.

## K4. Confirm the data contract before analysis

Before using a dataset, verify:

- Field definitions, units, missing-value conventions, time basis, sample coverage, and update timestamp.
- Deduplication, filtering, aggregation, and transformation rules.
- Whether denominators, baselines, and comparison periods are consistent.
- Selection bias, censoring, imputation, or exclusion rules that could change interpretation.

Computed results must be reproducible. If only partial, sampled, or truncated data is available, state the limitation in the conclusion.

## K5. Re-read before editing documentation

Before changing existing technical documentation, read at least:

- The target section and enough surrounding context to understand it.
- Relevant definitions, cross-references, and version notes within the document.
- Version-matched evidence for any API, implementation, configuration, or workflow the document describes.

Do not infer the intent of an entire document from one sentence that needs correction. For cross-section changes, table-of-contents changes, or whole-file rewrites, read the full document or the complete semantic scope first.

## K6. Citations and numbers

- Place citations close to the claims they support.
- Preserve units, periods, sample definitions, and counting rules for numeric claims.
- Do not directly compare values from incompatible versions, populations, or statistical definitions.
- When valid sources conflict, present the conflict and plausible causes without forcing a premature conclusion.
- If a source does not support an exact number, do not invent a precise value that merely looks plausible.

## K7. Re-pass the gates for each independent conclusion

If a later conclusion depends on a new source, a different table, another version, or a different document section, repeat G1-G3 from `SKILL.md`. One verified paragraph does not automatically authorize the entire answer.

Re-check time-sensitive information before delivery. If a source changes during the task, record the observation time and re-evaluate affected conclusions.

## K8. Delivery limits

Deliver only claims that are verified or explicitly labeled as inference. If required evidence cannot be obtained, state the confirmed portion and the evidence gap. Do not fill the gap from model memory or turn words such as "probably" and "usually" into definite claims.
