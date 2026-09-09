# Copilot repository instructions

Philosophy is the rule. See [`AGENTS.md`](../AGENTS.md).

Use [`R Code Conventions.md`](../R%20Code%20Conventions.md) for formatting,
packages, verbs, paths, and modelling. For Stata, Python, or Julia, use
[`General Code Conventions.md`](../General%20Code%20Conventions.md). Do not
add unsolicited checks. This file supplies repository routing.

## AI routing

- Claude rules: `.claude/rules/`
- Claude agents: `.claude/agents/`
- Claude skills: `.claude/skills/`
- Codex instructions: `.codex/instructions.md`
- Codex skills and metadata: `.agents/skills/`
- Copilot routing: `.github/instructions/ai-skills-routing.instructions.md`

Role mapping:

- `r-coder`: implement or substantially revise one R script;
- `r-reviewer`: review R scripts and produce a quality report;
- `r-build-and-review`: coordinate writing and reviewing an R script;
- `simplifier`: review overengineering, unsolicited checks, and extra folders;
  and
- `documentation-writer`: write methodology and technical documentation.

When a request matches a role, follow the role-specific workflow.
