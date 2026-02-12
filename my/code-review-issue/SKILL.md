---
name: code-review-issue
description: "Automatically review recent code commits, identify security vulnerabilities and code quality issues, and create GitHub issues with detailed findings. Use when you need to: (1) Review the latest commit for security problems, (2) Perform comprehensive code analysis for common vulnerabilities (SQL injection, hardcoded secrets, input validation), (3) Document findings in a structured GitHub issue, (4) Create a remediation branch and pull request with fixes."
---

# Code Review and Issue Creation

This skill delegates the code review workflow to a specialized subagent that will:
1. Review code commits for security and quality issues
2. Identify vulnerabilities and problems
3. Create detailed GitHub issues with findings
4. Optionally create fix branches and pull requests

## Usage Instructions

**IMPORTANT:** When this skill is invoked, you MUST immediately use the Task tool to delegate the work to a general-purpose subagent.

### Step 1: Identify Review Scope

From the user's request, determine:
- **Commit to review** (default: latest commit / HEAD)
- **Specific commit SHA** (if provided)
- **Whether to create fixes** (auto-fix mode)
- **Repository context** (if needed)

### Step 2: Launch Subagent

Use the Task tool with `subagent_type: "general-purpose"` to handle the review workflow:

```
Task tool parameters:
- subagent_type: "general-purpose"
- description: "Review code and create issue"
- prompt: [See template below]
```

### Prompt Template for Subagent

```
Please perform a comprehensive code review by following this workflow:

## Review Target
<Specify: "latest commit" or specific commit SHA>

## Workflow Steps

1. **Fetch commit details** using git:
   ```bash
   git show HEAD  # or specific commit SHA
   git show --stat HEAD  # for file list
   ```
   This provides commit metadata, full diff, and context.

2. **Analyze code changes** for security and quality issues:

   **🔴 Critical Security Issues (HIGH PRIORITY):**
   - Hardcoded credentials (passwords, API keys, tokens, secrets)
   - Real passwords or sensitive data in configuration files
   - Private keys or certificates committed to repo
   - Database credentials or connection strings

   **⚠️ Security Risks (MEDIUM PRIORITY):**
   - SQL injection vulnerabilities (dynamic query construction)
   - Command injection risks (shell command composition)
   - Insufficient input validation
   - Missing authentication/authorization checks
   - Unsafe deserialization
   - Path traversal vulnerabilities
   - XSS vulnerabilities

   **📝 Code Quality Issues (LOW PRIORITY):**
   - Poor error handling (bare `except` clauses)
   - Missing or inadequate logging
   - Lack of input sanitization
   - Missing documentation
   - Performance concerns
   - Code duplication

3. **OPTIONAL: Use Codex for deeper analysis**

   You can invoke the `collaborating-with-codex` skill to get additional insights:
   - Ask Codex to analyze specific code snippets for security issues
   - Get recommendations for secure coding patterns
   - Request code quality feedback
   - Verify your security findings

   Example:
   ```
   Use Skill tool with:
   skill: "collaborating-with-codex"
   args: "Review this code for SQL injection vulnerabilities: [code snippet]"
   ```

4. **Create GitHub issue** with structured findings:

   Use `gh` CLI to create the issue:
   ```bash
   gh issue create --title "Code Review - Commit <SHA>: <summary>" --body "$(cat <<'EOF'
   ## 代码审查报告

   **审查提交:** <commit SHA>
   **提交信息:** <commit message>
   **审查日期:** <date>

   ### 🔴 严重安全问题

   <List critical issues with:>
   - **文件:** path/to/file:line_number
   - **问题:** Description of the issue
   - **风险:** Security impact explanation
   - **建议:** Remediation steps

   ### ⚠️ 安全风险

   <List medium-priority security issues>

   ### 📝 代码质量问题

   <List code quality issues>

   ### 优先级建议

   1. 立即修复所有 🔴 严重安全问题
   2. 在下一个版本中解决 ⚠️ 安全风险
   3. 将 📝 代码质量问题加入技术债务清单

   ### 相关资源

   - [OWASP Top 10](https://owasp.org/www-project-top-ten/)
   - [CWE - Common Weakness Enumeration](https://cwe.mitre.org/)
   EOF
   )"
   ```

5. **OPTIONAL: Create fix branch and PR** (if user requested auto-fix):

   - Create branch: `fix/code-review-<short-sha>`
   - Apply fixes for identified issues
   - Commit with clear message
   - Push to remote
   - Create PR that references the issue

## Important Guidelines

- **Be thorough** - Check every changed file for security issues
- **Be specific** - Include exact file paths and line numbers
- **Be actionable** - Provide clear remediation steps
- **Prioritize** - Focus on security issues first, then quality
- **Use Codex** - Leverage the `collaborating-with-codex` skill for complex analysis
- **Confirm before creating** - Ask user before creating the GitHub issue

## Common Security Patterns to Check

**Hardcoded Secrets:**
- Look for keys: `password`, `secret`, `token`, `api_key`, `private_key`
- Check if values are real credentials vs placeholders like `"your_password"`
- Verify `.gitignore` excludes sensitive config files

**SQL Injection:**
- String interpolation in SQL: `f"SELECT * FROM {table}"`
- Missing parameterization
- Lack of identifier validation

**Input Validation:**
- User input used in: `eval()`, `exec()`, `os.system()`, SQL queries
- Missing whitelist validation
- No type checking or sanitization

**Error Handling:**
- Bare `except:` clauses
- Swallowed exceptions without logging
- Generic error messages that leak info
```

### Example Invocations

**Example 1: Review latest commit**
```
User: "Review the latest commit and create an issue"

Your action:
Use Task tool with:
  prompt: "Please perform a comprehensive code review... [full template with target: latest commit]"
```

**Example 2: Review specific commit**
```
User: "Review commit abc123 for security issues"

Your action:
Use Task tool with:
  prompt: "Please perform a comprehensive code review... [full template with target: commit abc123]"
```

**Example 3: Review and auto-fix**
```
User: "Review latest commit, create issue, and fix the problems"

Your action:
Use Task tool with:
  prompt: "Please perform a comprehensive code review... [full template + mention to create fix branch and PR]"
```

## Security Analysis Categories

### 🔴 Critical Security Issues
- **Hardcoded credentials** - Real passwords, API keys, tokens
- **Exposed secrets** - Private keys, certificates in repo
- **Sensitive data** - Database credentials, connection strings

### ⚠️ Security Risks
- **SQL injection** - Dynamic query construction without parameterization
- **Command injection** - Shell command composition with user input
- **Input validation** - Missing validation for user-facing inputs
- **Path traversal** - Unsanitized file paths
- **XSS** - Unescaped output in web contexts

### 📝 Code Quality Issues
- **Error handling** - Bare `except:` clauses, swallowed exceptions
- **Logging** - Missing error logging or debug information
- **Documentation** - Missing docstrings or unclear comments
- **Performance** - Inefficient algorithms or resource usage

## Detection Patterns

### Hardcoded Secrets
```python
# BAD - Real credential
{"password": "SuperSecret123!"}

# GOOD - Placeholder
{"password": "your_password"}
```

**Detection:** Keys like `password`, `secret`, `token`, `api_key` with non-placeholder values

### SQL Injection
```python
# BAD - String interpolation
cursor.execute(f"SELECT * FROM {table_name}")

# GOOD - Parameterized or validated
if not validate_identifier(table_name):
    raise ValueError("Invalid table name")
cursor.execute(f"SELECT * FROM `{table_name}`")
```

**Detection:** String formatting in SQL without parameterization or validation

### Missing Input Validation
```python
# BAD - Direct use
def process(user_input):
    return eval(user_input)

# GOOD - Validated
def process(user_input):
    if not is_safe(user_input):
        raise ValueError("Invalid input")
    return safe_process(user_input)
```

**Detection:** User input in sensitive operations (`eval`, `exec`, `os.system`, SQL)

### Poor Error Handling
```python
# BAD - Bare except
try:
    risky_operation()
except:
    pass

# GOOD - Specific handling
try:
    risky_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
    raise
```

**Detection:** Bare `except` clauses, swallowed exceptions

## Using Codex Skill

The subagent can leverage `collaborating-with-codex` skill for:

1. **Deep code analysis** - Ask Codex to analyze complex code patterns
2. **Security validation** - Verify suspected vulnerabilities
3. **Best practices** - Get recommendations for secure coding
4. **Code suggestions** - Request alternative implementations

**Example integration:**
```
# Within subagent
Skill tool call:
  skill: "collaborating-with-codex"
  args: "Analyze this Python function for SQL injection risks: [paste code]"
```

## Important Notes

- The subagent has full access to all tools (Bash, Read, Grep, gh CLI, etc.)
- The subagent can invoke the `collaborating-with-codex` skill for advanced analysis
- Always confirm with user before creating GitHub issues or PRs
- Focus on security issues first, then code quality
- Be specific with file paths and line numbers in findings

## GitHub Integration Notes

**Required permissions:**
- `issues:write` - Create and update issues
- `contents:write` - Create branches (if auto-fixing)
- `pull_requests:write` - Create PRs (if auto-fixing)

**Using gh CLI:**
```bash
# Create issue
gh issue create --title "..." --body "..."

# Create branch
git checkout -b fix/code-review-abc123

# Create PR
gh pr create --title "..." --body "Fixes #N"
```

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE - Common Weakness Enumeration](https://cwe.mitre.org/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
