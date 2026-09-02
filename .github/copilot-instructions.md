# Copilot repository instructions

The canonical coding standard is [`R Code Conventions.md`](../R%20Code%20Conventions.md).
Read it before writing or reviewing R code. For Stata, Python, or Julia code,
read [`General Code Conventions.md`](../General%20Code%20Conventions.md)
instead — its R section only points back to `R Code Conventions.md`. This
file supplies repository routing; it is not a second coding
standard.

## AI routing

- Claude rules: `.claude/rules/`
- Claude agents: `.claude/agents/`
- Claude skills: `.claude/skills/`
- Codex instructions: `.codex/instructions.md`
- Codex skills and metadata: `.agents/skills/`
- Copilot routing: `.github/instructions/ai-skills-routing.instructions.md`

Role mapping:

- `r-coder`: implement or substantially revise one R script;
- `r-reviewer`: review R scripts and produce a quality report; and
- `r-build-and-review`: coordinate writing and reviewing an R script.

When a request matches a role, follow the role-specific workflow after reading
the root master standard.
