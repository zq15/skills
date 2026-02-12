---
name: auto-fix-issue
description: "Automatically create a fix branch based on GitHub issue details, implement code fixes, and submit a pull request. Use when you need to: (1) Read and analyze a GitHub issue describing bugs or improvements, (2) Create a dedicated fix branch with appropriate naming, (3) Implement code changes to resolve the issue, (4) Commit changes with clear messages, (5) Push to remote and create a PR that closes the issue."
---

# Auto Fix Issue and Create PR

This skill delegates the entire issue-fixing workflow to a specialized subagent that will:
1. Read and analyze the GitHub issue
2. Create an appropriate fix branch
3. Implement code changes
4. Commit and push changes
5. Create a pull request that closes the issue

## Usage Instructions

**IMPORTANT:** When this skill is invoked, you MUST immediately use the Task tool to delegate the work to a general-purpose subagent.

### Step 1: Extract Issue Information

From the user's request, identify:
- **Issue number** (e.g., `#42`, `123`)
- **Issue URL** (e.g., `https://github.com/owner/repo/issues/42`)
- **Repository context** (owner/repo if available)

### Step 2: Launch Subagent

Use the Task tool with `subagent_type: "general-purpose"` to handle the entire workflow:

```
Task tool parameters:
- subagent_type: "general-purpose"
- description: "Fix GitHub issue and create PR"
- prompt: [See template below]
```

### Prompt Template for Subagent

```
Please fix GitHub issue <issue_number_or_url> by following this workflow:

1. **Read the issue** using gh CLI or GitHub MCP:
   - Fetch issue title, body, labels, and comments
   - Identify affected files, functions, and required changes

2. **Create a fix branch** with appropriate naming:
   - Bug fixes: `fix/issue-<number>-<short-description>`
   - Security issues: `fix/security-<description>`
   - Features: `feat/issue-<number>-<description>`
   - Refactoring: `refactor/<description>`

3. **Implement the fixes** systematically:
   - Address each point mentioned in the issue
   - Follow security best practices (no hardcoded secrets, input validation, SQL injection prevention)
   - Improve error handling where needed
   - Update .gitignore if necessary

4. **Test your changes** before committing:
   - Verify the fix addresses the issue
   - Run relevant tests if available
   - Check for regressions

5. **Commit changes** with a clear message:
   ```
   <type>: <short summary>

   <detailed description of changes>

   Fixes:
   - Issue point 1
   - Issue point 2

   Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
   ```

6. **Push to remote** and handle authentication if needed

7. **Create a pull request** using gh CLI:
   ```bash
   gh pr create --title "<type>: <summary>" --body "$(cat <<'EOF'
   ## 概述
   <Brief description>

   ## 解决的问题
   Fixes #<issue-number>

   ## 修复内容
   - <Fix 1>
   - <Fix 2>

   ## 测试建议
   - [ ] Test case 1
   - [ ] Test case 2

   Closes #<issue-number>
   EOF
   )"
   ```

**Important Guidelines:**
- Keep changes minimal and focused on the issue
- Never commit real credentials or sensitive data
- Use conventional commit types (fix:, feat:, refactor:, etc.)
- Link the PR to the issue using "Closes #<number>"
- Ask for user confirmation before pushing or creating the PR
```

### Example Invocations

**Example 1: By issue number**
```
User: "Fix issue #42"

Your action:
Use Task tool with:
  prompt: "Please fix GitHub issue #42 by following this workflow: [full workflow]"
```

**Example 2: By issue URL**
```
User: "Fix https://github.com/user/repo/issues/15"

Your action:
Use Task tool with:
  prompt: "Please fix GitHub issue https://github.com/user/repo/issues/15 by following this workflow: [full workflow]"
```



### Branch Naming Conventions
- **Bug fixes**: `fix/issue-<number>-<short-description>`
- **Security issues**: `fix/security-<description>`
- **Features**: `feat/issue-<number>-<description>`
- **Refactoring**: `refactor/<description>`

### Commit Types
- `fix:` - Bug fixes
- `feat:` - New features
- `refactor:` - Code refactoring
- `docs:` - Documentation
- `test:` - Test additions
- `chore:` - Maintenance tasks

### Security Best Practices

The subagent should follow these security guidelines:

1. **Never commit real credentials** - Replace hardcoded secrets with placeholders
2. **Input validation** - Validate all user inputs, especially for SQL queries
3. **SQL injection prevention** - Use parameterized queries and identifier validation
4. **Error handling** - Use specific exception types instead of bare `except`
5. **Gitignore updates** - Add patterns for sensitive config files

### Common Fix Patterns

**Security Vulnerabilities:**
- Remove hardcoded secrets → Replace with `"your_password"` placeholders
- SQL injection risks → Add `validate_identifier()` function
- Missing input validation → Validate before processing

**Code Quality:**
- Generic error handling → Use specific exception types
- Missing documentation → Add docstrings where needed
- Code duplication → Extract to functions (if simple)

**Configuration:**
- Exposed config files → Add to .gitignore
- Missing examples → Create `.example` files

## Important Notes

- The subagent has full access to all tools (Read, Edit, Write, Bash, Grep, Glob, etc.)
- The subagent will handle git operations, testing, and PR creation autonomously
- Always ask the subagent to confirm with the user before pushing or creating PRs
- The subagent should maintain minimal scope - only fix what's described in the issue

## Troubleshooting Tips for Subagent

Include these tips in the subagent prompt if needed:

**Authentication Issues:**
- Use `gh auth login` for GitHub CLI authentication
- Switch to SSH with `git remote set-url origin git@github.com:user/repo.git`

**Merge Conflicts:**
- Rebase against main branch before pushing
- Resolve conflicts carefully, don't discard user changes

**Test Failures:**
- Run tests locally before pushing
- Fix failing tests or update them if behavior changed intentionally
