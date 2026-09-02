# Copilot project context

The canonical coding standard is [`R Code Conventions.md`](../R%20Code%20Conventions.md).
Read it before writing or reviewing R code. This file supplies project context
and routing; it is not a second coding standard.

## Project context

This repository supports Alberta GDP inventory estimation using Statistics
Canada's provincial GDP methodology. The active economic categories are:

- livestock: cattle, hogs, and poultry;
- large crops: wheat, canola, and barley;
- non-farm: wholesale, retail, and manufacturing; and
- potatoes.

The work uses Fisher indices, chained-volume GDP contributions,
quarterly-to-annual aggregation, and historical averages for approved missing
values. Inventory changes are summed across quarters; index values follow the
approved weighted-average or end-of-period rule.

Use project configuration variables such as `ESTIMATION_YEAR`, `BASE_YEAR`,
`INPUT_DIR`, `PROCESSED_DIR`, and `FISHER_OUTPUT_DIR`. Do not hardcode years,
machine paths, or input filenames.

## AI routing

- Claude rules: `.claude/rules/`
- Claude agents: `.claude/agents/`
- Claude skills: `.claude/skills/`
- Codex instructions: `.codex/instructions.md`
- Codex skills and metadata: `.codex/skills/`
- Copilot routing: `.github/instructions/ai-skills-routing.instructions.md`

Role mapping:

- `r-coder`: implement or substantially revise one R script;
- `r-reviewer`: review R scripts and produce a quality report; and
- `r-build-and-review`: coordinate writing and reviewing an R script.

When a request matches a role, follow the role-specific workflow after reading
the root master standard.
