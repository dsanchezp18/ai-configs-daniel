# Copilot repository instructions

Philosophy is the rule. See [`AGENTS.md`](../AGENTS.md).

Use [`R Code Conventions.md`](../R%20Code%20Conventions.md) for formatting,
packages, verbs, paths, and modelling. For Stata, Python, or Julia, use
[`General Code Conventions.md`](../General%20Code%20Conventions.md). Do not
follow Check inputs, Check results, or unsolicited assertions in those
files. This file supplies repository routing.

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
- `r-build-and-review`: coordinate writing and reviewing an R script; and
- `simplifier`: review overengineering, unsolicited checks, and extra folders.

When a request matches a role, follow the role-specific workflow. Philosophy
in `AGENTS.md` wins over conflicting convention sections.
