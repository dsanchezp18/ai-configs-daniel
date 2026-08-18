---
applyTo: "**"
---

# Copilot AI Skills and Agents

Use this routing when responding in this repository.

## Source of truth by AI folder

- Claude skills: `.claude/skills/*/SKILL.md`
- Claude agents: `.claude/agents/*.md`
- Claude coding rules: `.claude/rules/r-code-conventions.md`
- Codex skills: `.codex/skills/*/SKILL.md`
- Codex agent metadata: `.codex/skills/*/agents/openai.yaml`

Do not mix locations. Keep Claude references in `.claude/*` and Codex references in `.codex/*`.

## Invocation routing

- Use **r-coder** behavior for writing or substantially revising one R script.
- Use **r-reviewer** behavior for audit/review tasks and report generation.
- Use **r-build-and-review** behavior for two-step write-then-review orchestration.
- Use **research-data-workflow** for folder structure, reproducibility, and data lifecycle setup.
- Use **modern-workflow-r**, **tidyverse-patterns**, and **r-style-guide** as implementation and style standards for R code.

## Conflict resolution

If instructions conflict, prefer:
1. `.claude/rules/r-code-conventions.md`
2. The role-specific skill/agent file
3. `.github/copilot-instructions.md`
