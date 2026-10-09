# Research, Analysis and Documentation Protocol

For fact checking, technical Q&A, API explanations, data analysis and documentation edits. These are usually L0 (read-only) steps. Editing a document is an L1 or L2 step under SKILL.md.

## Contents

1. Frame the question
2. Find and open primary sources
3. Classify every material claim
4. Check the data contract before analysis
5. Numbers and citations
6. Editing documentation
7. Delivery

## 1. Frame the question

Settle these before searching: what kind of answer is wanted (fact, comparison, derivation, summary, recommendation, or a document change), plus the subject, version, time range, region, dataset and terminology. Mark which claims are time-sensitive. If an ambiguity would change the answer and sources can resolve it, investigate instead of asking the user.

## 2. Find and open primary sources

Search results, AI summaries and blog posts help you find sources. Base claims on the closest primary source:

1. Specifications, official documentation, official source code, official announcements.
2. Original papers, datasets, statutes, standards, first-party statistics.
3. High-quality secondary sources, used only for context the primary sources lack.

For "since which version" questions, look for the changelog or release-notes entry. Without one, compare the source at the last tag lacking the behavior and the first tag that has it. When an official site is unreachable, the version-tagged copy in the project's repository is still a primary source; see `verification-recipes.md` §9.

For each source you rely on, note the URL or path, its date or version, the section, and the claim the passage directly supports. A homepage or index page does not support a specific claim. If a fact needs network access you do not have, label it unverified; do not fill it in from memory.

## 3. Classify every material claim

- **Verified:** stated explicitly in a source you opened, or directly visible in the data.
- **Inferred:** derived from verified premises. State the premises and limits.
- **Unverified:** evidence is missing, conflicting, or covers a different version, population or period.

Do not present an inference as if a source said it. Do not generalize from one case to a whole population, version family or time range.

## 4. Check the data contract before analysis

Before computing anything, confirm field definitions, units, missing-value conventions, time basis, coverage and update time. Also confirm any filtering, deduplication and aggregation rules, and check that denominators and comparison periods are consistent. Look for selection bias or exclusions that could change the reading. Keep computations reproducible: show the query or code and the input version. State any sampling or truncation in the conclusion.

## 5. Numbers and citations

- Put each citation next to the claim it supports.
- Keep units, periods, sample definitions and counting rules with every number.
- Do not compare values whose definitions, populations or versions differ. Either align them or state that they are incompatible.
- When credible sources conflict, present the conflict and its likely causes instead of picking one silently.
- Never produce a precise-looking number the source does not give.

## 6. Editing documentation

Before editing, read the target section and enough of its surroundings, along with related definitions, cross-references and version notes. Re-check the behavior the document describes against the version-matched implementation or spec. Read the whole document before changes that cross sections or touch the table of contents. Integrate corrections directly; do not add change logs, self-critique or obsolete text to the body.

## 7. Delivery

Deliver verified claims, plus inferences labeled as such. If evidence is missing, state what is confirmed and what the gap is. Do not turn "probably" into a definite statement. Re-check time-sensitive facts before delivery, and give the observation date when it matters.
