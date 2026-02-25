---
name: code-review-issue
description: "Review recent code commits for security vulnerabilities and quality issues, then create a GitHub issue with findings. Use when: 'review latest commit', 'code review', 'security audit', 'create review issue', '代码审查'."
---

# Code Review & Issue Creation

Reviews a commit for security and quality issues, then creates a GitHub issue with structured findings.

## Workflow

### Step 1: Analyze with Codex

Use the `collaborating-with-codex` skill to delegate the analysis (saves Claude tokens — Codex reads the diff and reports findings):

```
Prompt for Codex:
Run `git show HEAD --stat` then `git show HEAD` to get the latest commit diff.
Analyze all changed files for:
- Hardcoded secrets (passwords, API keys, tokens)
- SQL / command injection risks
- Missing input validation
- Poor error handling (bare except, swallowed exceptions)
- Other security or quality issues

For each issue found, report: file path, line number, severity (critical/medium/low), description, and recommended fix.
If no issues found, say so clearly.
```

Adjust the git command if reviewing a specific commit SHA provided by the user.

### Step 2: Create GitHub Issue

Based on the findings, confirm with the user, then create the issue:

```bash
gh issue create --title "Code Review - <short-sha>: <summary>" --body "$(cat <<'EOF'
## Code Review Report

**Commit:** <sha>
**Message:** <commit message>

### 🔴 Critical Issues
<findings or "None">

### ⚠️ Security Risks
<findings or "None">

### 📝 Quality Issues
<findings or "None">

### Priority
1. Fix critical issues immediately
2. Address security risks in next release
3. Add quality issues to tech debt backlog
EOF
)"
```

### Step 3: Optional Fix Branch

If the user wants auto-fix, create a branch `fix/review-<short-sha>`, apply fixes, and open a PR referencing the issue.
