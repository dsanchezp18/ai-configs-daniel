# Git Workflow

Language-agnostic Git conventions for keeping changes intentional, reviewable,
recoverable, and associated with the correct GitHub account.

## 1. Confirm scope and identity

Before changing Git state:

\`\`\`powershell
git status --short --branch
git remote -v
git branch --show-current
\`\`\`

Confirm the repository, remote, branch, and existing user changes. Never
discard, reset, overwrite, or delete user changes without explicit approval.
If the worktree contains unrelated changes, stage only the files belonging to
the current task.

## 2. Credentials and account separation

Keep personal and work GitHub accounts separate. For personal-repository work,
check the saved account first:

\`\`\`powershell
git credential-manager github list
\`\`\`

A repository-local remote URL can help select the destination, but saved Git
Credential Manager credentials are system-wide. Changing a remote URL does not
change the saved account.

Never commit passwords, tokens, private keys, API keys, credential exports, or
local environment files. If a credential is exposed, revoke it immediately
and follow the repository's security process.

## 3. Branches

Use the default branch only for intentional maintenance or when a direct push
was explicitly requested. For normal feature work:

\`\`\`powershell
git switch main
git pull --ff-only origin main
git switch -c feature/short-description
\`\`\`

Use short, lowercase, hyphenated names such as:

- \`feature/add-validation\`
- \`fix/path-resolution\`
- \`docs/update-workflow\`
- \`chore/refresh-configs\`

Do not reuse a branch for unrelated work.

## 4. Before committing

Inspect the complete scope and run relevant checks:

\`\`\`powershell
git status --short --branch
git diff
git diff --stat
git diff --check
\`\`\`

For code, also run the project's formatter, linter, tests, parser, build, or
render command when available. Do not claim verification merely because a
command exited successfully if its outputs were not checked.

Stage intentionally:

\`\`\`powershell
git add path/to/file1 path/to/file2
git diff --cached --stat
git diff --cached --check
\`\`\`

Use \`git add -A\` only when the entire worktree has been inspected and every
change belongs to the same task.

## 5. Commits

Each commit should represent one coherent, reviewable change. Use a short
imperative subject, normally no more than 72 characters:

\`\`\`text
Add Git workflow guide
Fix path resolution in data loader
Update validation instructions
\`\`\`

Avoid vague messages such as \`changes\`, \`updates\`, or \`fix stuff\`. Do not mix
unrelated refactors, formatting-only edits, generated files, and functional
changes unless the task requires it.

\`\`\`powershell
git commit -m "Short imperative description"
git show --stat --oneline --summary HEAD
git status --short --branch
\`\`\`

## 6. Updating from the remote

If the local branch has no local commits, prefer fast-forward-only pulls:

\`\`\`powershell
git pull --ff-only origin main
\`\`\`

If local commits exist and the remote moved, preserve remote history:

\`\`\`powershell
git fetch origin main
git rebase origin/main
\`\`\`

Resolve conflicts deliberately: inspect each marker, choose the correct
content, remove all markers, run checks, stage the file, and continue:

\`\`\`powershell
git add path/to/resolved-file
git rebase --continue
\`\`\`

If the rebase cannot be resolved safely, stop and report the exact state.
Do not use a destructive reset as a shortcut.

## 7. Pushing

Before pushing, confirm the destination:

\`\`\`powershell
git branch --show-current
git remote get-url origin
git log -1 --oneline --decorate
git status --short --branch
\`\`\`

Push a new branch with tracking:

\`\`\`powershell
git push -u origin feature/short-description
\`\`\`

Push an existing tracked branch:

\`\`\`powershell
git push origin main
\`\`\`

Never force-push shared branches by default. Use \`--force-with-lease\` only
when history rewriting is explicitly approved and the current remote state has
been checked. Never use plain \`--force\` for routine work.

If a push is rejected because the remote moved, do not overwrite the remote.
Fetch, inspect divergence, rebase or merge according to repository policy,
rerun checks, and push again.

## 8. Verifying a push

Confirm local and remote-tracking state:

\`\`\`powershell
git status --short --branch
git rev-list --left-right --count HEAD...origin/main
git log -1 --oneline --decorate
\`\`\`

When network access is available, verify the remote directly:

\`\`\`powershell
git ls-remote origin HEAD
\`\`\`

The returned remote commit should match the pushed commit. Distinguish fresh
remote output from cached \`origin/main\` information; cached equality is not
fresh proof if authentication or network access failed.

A completed push should leave no unintended worktree changes, matching local
and remote commits, completed checks, and a confirmed destination account.

## 9. Reviews and pull requests

Use a pull request for non-trivial changes, shared branches, or work that
benefits from review. Describe what changed, why, checks run, limitations, and
follow-up work. Keep review feedback focused on correctness, security,
reproducibility, compatibility, and maintainability.

## 10. Repository hygiene

Do not commit secrets, local caches, logs, temporary files, large raw data, or
generated output unless the repository explicitly versions them. Generated
artifacts should be reproducible from committed source and documented inputs.

Keep \`.gitignore\` aligned with the project. It should normally exclude secrets,
environment files, OS/editor files, logs, dependency caches, build output, and
raw or sensitive data.

## 11. Recovery

Use inspectable, recoverable operations first:

\`\`\`powershell
git reflog
git log --oneline --decorate --graph --all
\`\`\`

Before risky history operations, inspect the contents and create a safety
branch when useful. Remember:

- \`git reset --hard\` can discard uncommitted work;
- \`git clean\` can delete untracked files;
- \`git push --force\` can overwrite shared history; and
- broad restore or deletion commands can affect unrelated files.

When in doubt, stop and report the exact state before discarding data.

## 12. Completion report

Report the repository and remote, branch, commit and subject, changed scope,
checks and results, push result, fresh remote verification, and any remaining
limitation or follow-up.
