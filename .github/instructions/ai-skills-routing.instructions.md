---
applyTo: "**"
---

# Copilot AI routing

Read the root [`R Code Conventions.md`](../../R%20Code%20Conventions.md) first
for all coding standards. Keep the following folders separate by tool:

- Claude skills: `.claude/skills/*/SKILL.md`
- Claude agents: `.claude/agents/*.md`
- Claude rule loader: `.claude/rules/r-code-conventions.md`
- Codex skills: `.codex/skills/*/SKILL.md`
- Codex agent metadata: `.codex/skills/*/agents/openai.yaml`

Use:

- `r-coder` for writing or substantially revising one R script;
- `r-reviewer` for audit and review reports; and
- `r-build-and-review` for write-then-review orchestration.

## Keeping tool formats in sync

The R role definitions exist twice: as Claude agents under `.claude/agents/`
and as Codex skills under `.codex/skills/`. The two copies paraphrase the
same behavior; they are not generated from one source. When you edit one
copy of a role, make the matching substantive edit to the other copy in the
same commit, and check `git diff main -- .claude/agents .codex/skills`
before committing so the pair does not drift.

If instructions conflict, prefer:

1. `R Code Conventions.md`;
2. the role-specific skill or agent; and
3. general project context in `.github/copilot-instructions.md`.
