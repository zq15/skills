---
name: code-review-issue
description: "Automatically review recent code commits, identify security vulnerabilities and code quality issues, and create GitHub issues with detailed findings. Use when you need to: (1) Review the latest commit for security problems, (2) Perform comprehensive code analysis for common vulnerabilities (SQL injection, hardcoded secrets, input validation), (3) Document findings in a structured GitHub issue, (4) Create a remediation branch and pull request with fixes."
---

# Code Review and Issue Creation

Automated workflow to review code commits, identify issues, and track them in GitHub.

## Quick Start

1. **Ensure GitHub integration** is configured with appropriate permissions
2. **Run the review** on the latest commit or specify a commit SHA
3. **Issues are automatically created** with categorized findings
4. **Optionally create a fix branch** and submit a PR

## Workflow

### 1. Review Latest Commit

View the most recent commit with full diff:

```bash
git show HEAD
```

This provides:
- Commit metadata (author, date, message)
- Full diff of all changes
- Context for understanding the scope

### 2. Perform Security Analysis

Analyze the code changes for common issues:

**🔴 Critical Security Issues:**
- Hardcoded credentials (passwords, API keys, tokens)
- Exposed secrets in configuration files
- Sensitive data in version control

**⚠️ Security Risks:**
- SQL injection vulnerabilities
- Command injection risks
- Insufficient input validation
- Missing authentication/authorization checks
- Unsafe deserialization
- XSS vulnerabilities

**📝 Code Quality Issues:**
- Poor error handling
- Missing logging
- Inconsistent documentation
- Lack of input sanitization
- Performance concerns

### 3. Create GitHub Issue

Document findings in a structured issue:

```json
{
  "title": "Code Review - Commit <SHA> (<subject>)",
  "body": "## Code Review\n\n### 🔴 Critical Issues\n...\n### ⚠️ Security Risks\n...\n### 📝 Code Quality\n..."
}
```

Issue format:
- Clear categorization by severity
- File paths and line numbers
- Specific problem descriptions
- Actionable recommendations
- Priority guidance

### 4. Create Fix Branch (Optional)

If requested, automatically create a remediation branch:

1. Create branch from main (e.g., `fix/security-issues`)
2. Apply fixes for identified issues
3. Commit changes with descriptive message
4. Push to remote
5. Create pull request linking to the issue

## Common Issues Detected

### Hardcoded Secrets

**Problem:**
```json
{
  "password": "SuperSecret123!"
}
```

**Detection:** Look for keys like `password`, `secret`, `token`, `api_key` with non-placeholder values.

**Fix:** Replace with placeholders in example files, add to `.gitignore`.

### SQL Injection

**Problem:**
```python
cursor.execute(f"SELECT * FROM {table_name}")
```

**Detection:** String formatting in SQL queries without parameterization.

**Fix:** Use parameterized queries or add input validation.

### Missing Input Validation

**Problem:**
```python
def process(user_input):
    return eval(user_input)  # Dangerous!
```

**Detection:** User input used without validation in sensitive operations.

**Fix:** Whitelist validation, type checking, sanitization.

### Inadequate Error Handling

**Problem:**
```python
try:
    risky_operation()
except:
    pass
```

**Detection:** Bare `except` clauses, swallowed exceptions.

**Fix:** Specific exception handling with logging.

## GitHub Integration

### Required Permissions

- `issues:write` - Create and update issues
- `contents:write` - Create branches and push code
- `pull_requests:write` - Create pull requests

### Using the GitHub MCP

The workflow uses GitHub MCP tools:

- `issue_write` - Create issues with findings
- `create_branch` - Create fix branches
- `push_files` - Push remediation code
- `create_pull_request` - Submit PR for review

### Handling Permission Issues

If you encounter 403 errors:

1. Check token permissions in GitHub settings
2. Regenerate token with required scopes
3. Update MCP configuration
4. Retry operations

Alternatively, use SSH for git operations:
```bash
git remote set-url origin git@github.com:user/repo.git
```

## Best Practices

### Review Scope

- Focus on security-critical changes first
- Review configuration files carefully
- Check for exposure of sensitive data
- Verify input validation for user-facing code

### Issue Documentation

- Be specific about file paths and line numbers
- Explain the security impact clearly
- Provide actionable remediation steps
- Prioritize findings by severity

### Remediation

- Fix critical issues immediately
- Group related fixes in single commits
- Test changes before creating PR
- Link PR to the tracking issue

## Example Usage

**Scenario:** Review latest commit and create issue

1. User requests: "Review the latest commit and create an issue"
2. Tool fetches commit with `git show HEAD`
3. Analyzes code for vulnerabilities
4. Creates GitHub issue with structured findings
5. Reports issue URL to user

**Scenario:** Review, fix, and create PR

1. User requests: "Review latest commit, fix issues, and create PR"
2. Tool performs code review
3. Creates tracking issue
4. Creates fix branch
5. Applies security fixes
6. Commits and pushes changes
7. Creates pull request
8. Reports PR URL

## Security Notes

- Never commit real credentials, even in review tools
- Rotate any exposed secrets immediately
- Consider secrets management tools (Vault, AWS Secrets Manager)
- Use `.gitignore` to prevent sensitive file commits
- Enable pre-commit hooks for secret scanning

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE - Common Weakness Enumeration](https://cwe.mitre.org/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
