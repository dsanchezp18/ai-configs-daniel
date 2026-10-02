---
name: skills-sync
description: Compare and sync the ai-configs-daniel repo with the live Claude and Codex folders (skills, agents, rules). Shows which side is newer before copying. Use when the user says "sync skills", "sync the configs", or after any change to a skill, agent or rule.
argument-hint: "[--check to compare only]"
allowed-tools: ["Bash", "Read"]
---

# Skills sync

The repo `C:\Users\Daniel\Documents\GitHub\ai-configs-daniel` is the source of truth. The live copies are separate folders, and editing one does not update the others.

| Repo folder | Live copy | Used by |
|---|---|---|
| `.claude/skills/` | `~/.claude/skills/` | Claude Code |
| `.claude/agents/` | `~/.claude/agents/` | Claude Code |
| `.claude/rules/` | `~/.claude/rules/` | Claude Code |
| `.agents/skills/` | `~/.codex/skills/` | Codex |

## Steps

1. Compare each pair:
   `diff -rq --strip-trailing-cr -x __pycache__ <repo folder> <live folder>`
2. For each file that differs or exists on one side only, check which side is newer (modification time and content). Show the user the list with the newer side marked.
3. With `--check`, stop here.
4. Copy repo to live when the repo is newer. If a live file is newer than the repo, do not overwrite it. Ask the user which side wins.
5. Re-run the diff. Report any difference that remains.

## Rules

- Leave Codex-only folders alone: `.system`, `codex-primary-runtime`, `refresh-final-sheet`. They are not in the repo.
- A skill may have files on one side only by design (for example `agents/` folders used by Codex). Show these and do not delete them.
- A skill deleted from the repo is deleted from the live folders only after the user confirms the list.
- Do not commit or push. Do that only when the user asks.
