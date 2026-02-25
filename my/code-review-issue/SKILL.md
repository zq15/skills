---
name: code-review-issue
description: "Review recent code commits for security vulnerabilities and quality issues, then create a GitHub issue with findings. Use when: 'review latest commit', 'code review', 'security audit', 'create review issue'."
---

# Code Review & Issue Creation

Review a commit for security and quality issues, then create a GitHub issue with structured findings.

## Workflow

### Step 1: Analyze with Codex

Use the `collaborating-with-codex` skill. Pass the current project directory as `--cd`. Prompt:

```
Run the following commands to get the commit info:
  git show <SHA_OR_HEAD> --stat
  git show <SHA_OR_HEAD>

Then analyze all changed files for:
- 🔴 Critical: hardcoded secrets (passwords, API keys, tokens, private keys)
- ⚠️  Medium: SQL/command injection, missing input validation, path traversal, unsafe deserialization
- 📝 Low: bare except clauses, swallowed exceptions, missing logging

For each issue report: severity, file path + line number, description, recommended fix.
If no issues found, say so clearly.
```

Replace `<SHA_OR_HEAD>` with the target commit (default: `HEAD`).

### Step 2: Create GitHub Issue

Based on Codex findings, run:

```bash
gh issue create --title "Code Review - <short-sha>: <one-line summary>" --body "$(cat <<'EOF'
## Code Review Report

**Commit:** <sha>
**Message:** <commit message>
**Date:** <date>

### 🔴 Critical Issues

<findings or "None">

### ⚠️ Security Risks

<findings or "None">

### 📝 Code Quality Issues

<findings or "None">

### Priority

1. Fix 🔴 critical issues immediately
2. Address ⚠️ risks in next release
3. Add 📝 quality issues to tech debt backlog
EOF
)"
```

Always confirm with the user before creating the issue.

### Step 3: Fix Branch (optional)

If the user wants auto-fix:

```bash
git checkout -b fix/review-<short-sha>
# apply fixes
git commit -m "fix: address code review findings from <short-sha>"
git push -u origin HEAD
gh pr create --title "Fix code review issues from <short-sha>" --body "Fixes #<issue-number>"
```
