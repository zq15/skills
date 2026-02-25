---
name: auto-fix-issue
description: "Fix a GitHub issue: read the issue, create a fix branch, implement changes, and submit a PR. Use when: 'fix issue #N', 'fix https://github.com/.../issues/N', 'auto fix issue', '修复 issue'."
---

# Auto Fix Issue

Reads a GitHub issue, implements the fix, and creates a PR.

## Workflow

Use the Task tool (`subagent_type: "general-purpose"`) with this prompt:

```
Fix GitHub issue <number or URL>:

1. Read the issue: `gh issue view <number> --json title,body,labels,comments`
2. Create a branch:
   - Bug fix → `fix/issue-<number>-<short-description>`
   - Feature  → `feat/issue-<number>-<description>`
   - Refactor → `refactor/<description>`
3. Implement the fix — keep changes minimal and scoped to the issue
4. Commit using conventional format:
   ```
   fix: <summary>

   Closes #<number>

   Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
   ```
5. Confirm with user before pushing
6. Push and create PR:
   ```bash
   gh pr create --title "fix: <summary>" --body "$(cat <<'EOF'
   ## Summary
   <what was changed and why>

   ## Changes
   - <change 1>

   Closes #<number>
   EOF
   )"
   ```
```

Fill in the issue number/URL from the user's request before launching the subagent.
