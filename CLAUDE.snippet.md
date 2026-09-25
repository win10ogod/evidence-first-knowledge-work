## Mandatory evidence-first knowledge work

For coding, debugging, API/SDK/CLI usage, configuration changes, technical research, data analysis, technical answers, or documentation edits, load and follow `.claude/skills/evidence-first-knowledge-work/SKILL.md` before implementation.

Mandatory behavior:

- Verify relevant first-party documentation for the exact version before relying on API or specification knowledge, even when the API is familiar.
- Read the applicable project documentation and current target contents before every independent edit step.
- Re-read the relevant source/specification and current state before each independent patch, retry, or side-effecting operation.
- Keep each operation within an explicit, minimal scope and validate it immediately afterward.
- Stop the affected step when required evidence, version, permissions, target state, or validation method is missing or conflicting.
- Never claim a check passed unless it was actually run and observed. Mark unrun checks as NOT RUN.

Guided execution is mandatory for engineering work, including smaller or less reliable models. Follow the skill's required-reading table and `.claude/skills/evidence-first-knowledge-work/references/guided-development.md`; do not infer an exemption from confidence or change size.

- Map every requested outcome to observable acceptance and keep a resumable requirement ledger.
- Trace the real entry point before selecting an owning layer; keep one implementation item active by default.
- Use the decision playbook for unknowns and failed checks; run bounded experiments for novel designs without guessing API contracts.
- Preserve failed hypotheses, re-read current evidence after interruption, and do not repeat contradicted approaches without new evidence.
- Before delivery, run the completion review: verify independent expectations, test discovery, current revisions, and actual integration.
- Report process compliance and task outcome separately. Procedural compliance alone is not completion.
