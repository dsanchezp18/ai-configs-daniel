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
- `r-reviewer` for audit and review reports;
- `r-build-and-review` for write-then-review orchestration; and
- `research-data-workflow` for folder structure, reproducibility, and data
  lifecycle setup.

If instructions conflict, prefer:

1. `R Code Conventions.md`;
2. the role-specific skill or agent; and
3. general project context in `.github/copilot-instructions.md`.
