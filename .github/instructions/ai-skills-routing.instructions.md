---
applyTo: "**"
---

# Copilot AI routing

Philosophy is the rule. Read [`AGENTS.md`](../../AGENTS.md) first. Use
[`R Code Conventions.md`](../../R%20Code%20Conventions.md) for formatting,
packages, verbs, paths, and modelling. Do not follow Check inputs, Check
results, or unsolicited assertions in that file.

Keep the following folders separate by tool:

- Claude skills: `.claude/skills/*/SKILL.md`
- Claude agents: `.claude/agents/*.md`
- Claude rule loader: `.claude/rules/r-code-conventions.md`
- Codex skills: `.agents/skills/*/SKILL.md`
- Codex agent metadata: `.agents/skills/*/agents/openai.yaml`

Use:

- `r-coder` for writing or substantially revising one R script;
- `r-reviewer` for audit and review reports;
- `r-build-and-review` for write-then-review orchestration; and
- `simplifier` for overengineering review.

## Keeping tool formats in sync

The R role definitions exist twice: as Claude agents under `.claude/agents/`
and as Codex skills under `.agents/skills/`. The two copies paraphrase the
same behavior; they are not generated from one source. When you edit one
copy of a role, make the matching substantive edit to the other copy in the
same commit, and check `git diff main -- .claude/agents .agents/skills`
before committing so the pair does not drift.

If instructions conflict, prefer:

1. `AGENTS.md` working approach (philosophy);
2. the role-specific skill or agent;
3. `R Code Conventions.md`, except Check inputs, Check results, and
   unsolicited assertions; and
4. general repository routing in `.github/copilot-instructions.md`.
