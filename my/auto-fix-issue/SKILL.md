---
name: auto-fix-issue
description: "Automatically create a fix branch based on GitHub issue details, implement code fixes, and submit a pull request. Use when you need to: (1) Read and analyze a GitHub issue describing bugs or improvements, (2) Create a dedicated fix branch with appropriate naming, (3) Implement code changes to resolve the issue, (4) Commit changes with clear messages, (5) Push to remote and create a PR that closes the issue."
---

# Auto Fix Issue and Create PR

Automated workflow to resolve GitHub issues by creating fix branches, implementing solutions, and submitting pull requests.

## Quick Start

1. **Identify the issue** to fix (by issue number or URL)
2. **Analyze issue details** to understand the problem
3. **Create fix branch** with descriptive name
4. **Implement fixes** addressing all points in the issue
5. **Commit, push, and create PR** linking back to the issue

## Workflow

### 1. Read GitHub Issue

Fetch the issue details using GitHub MCP:

```javascript
// Get issue information
issue_read({
  method: "get",
  owner: "username",
  repo: "repository",
  issue_number: 1
})
```

Extract from the issue:
- **Title**: Brief description of the problem
- **Body**: Detailed explanation with code snippets, file paths
- **Labels**: Priority, type (bug, security, enhancement)
- **Comments**: Additional context or suggestions

### 2. Analyze Issue Content

Parse the issue to identify:

**Problem Areas:**
- Affected files and line numbers
- Specific functions or methods
- Configuration issues
- Security vulnerabilities

**Required Changes:**
- Code modifications needed
- New files to create
- Files to delete
- Configuration updates

**Acceptance Criteria:**
- Expected behavior after fix
- Test cases to verify
- Performance requirements

### 3. Create Fix Branch

Create a descriptive branch name based on issue type:

**Branch Naming Convention:**
- `fix/issue-<number>-<short-description>` - Bug fixes
- `fix/security-<description>` - Security issues
- `feat/issue-<number>-<description>` - New features
- `refactor/<description>` - Code improvements

```bash
git checkout -b fix/mysql-security-issues
```

Branch from:
- `main` or `master` - For direct fixes
- `develop` - For feature branches
- Specific tag - For hotfixes

### 4. Implement Fixes

Apply fixes systematically for each issue point:

#### Security Fixes

**Hardcoded Secrets:**
```bash
# Before
{
  "password": "RealPassword123!"
}

# After
{
  "password": "your_password"
}
```

**SQL Injection:**
```python
# Before
cursor.execute(f"SELECT * FROM {table}")

# After
if not validate_identifier(table):
    raise ValueError(f"Invalid table name: {table}")
cursor.execute(f"SELECT * FROM `{table}`")
```

**Input Validation:**
```python
# Add validation function
def validate_identifier(identifier: str) -> bool:
    """Validate SQL identifier to prevent injection."""
    if not identifier:
        return False
    pattern = r'^[a-zA-Z0-9_-]+$'
    return bool(re.match(pattern, identifier))
```

#### Error Handling

**Improve Exception Handling:**
```python
# Before
except Exception as e:
    print(f"Error: {e}")
    return False

# After
except KeyError as e:
    print(f"Missing configuration: {e}", file=sys.stderr)
    return False
except pymysql.MySQLError as e:
    print(f"Database error: {e}", file=sys.stderr)
    return False
except Exception as e:
    print(f"Unexpected error: {e}", file=sys.stderr)
    return False
```

#### Configuration Files

**Update .gitignore:**
```bash
# Prevent sensitive files from being committed
**/config.json
**/*.env
**/secrets.yml
```

### 5. Test Changes

Before committing, verify fixes:

**Manual Testing:**
- Run affected functionality
- Test edge cases mentioned in issue
- Verify no regression in other areas

**Automated Testing:**
```bash
# Run unit tests
pytest tests/

# Run linters
flake8 .
pylint module/

# Security scans
bandit -r .
```

### 6. Commit Changes

Create clear, descriptive commit messages:

**Commit Message Format:**
```
<type>: <short summary>

<detailed description>

Fixes:
- Issue point 1
- Issue point 2
- Issue point 3

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Types:**
- `fix:` - Bug fixes
- `feat:` - New features
- `refactor:` - Code refactoring
- `docs:` - Documentation
- `test:` - Test additions
- `chore:` - Maintenance

**Example:**
```bash
git add file1.py file2.json .gitignore
git commit -m "$(cat <<'EOF'
fix: 修复 MySQL skill 安全问题

解决 Issue #1 中的安全问题：

🔴 严重问题修复：
- 移除硬编码的真实密码，替换为占位符

⚠️ 安全风险修复：
- 添加 SQL 标识符验证函数，防止 SQL 注入
- 限制 execute_query 仅允许 SELECT 语句

📝 代码质量改进：
- 改进错误处理，提供更详细的错误信息
- 添加 .gitignore 规则防止真实配置文件被提交

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

### 7. Push to Remote

Push the fix branch to GitHub:

**Using SSH:**
```bash
# Set remote to SSH (if not already)
git remote set-url origin git@github.com:user/repo.git

# Push branch
git push -u origin fix/issue-name
```

**Using HTTPS:**
```bash
# Push with credentials
git push -u origin fix/issue-name
```

**Handle Authentication:**
- SSH keys for git operations
- Personal Access Token for GitHub API
- GitHub CLI (`gh auth login`)

### 8. Create Pull Request

Submit PR linking to the issue:

**PR Title Format:**
```
<type>: <concise description>
```

**PR Body Template:**
```markdown
## 概述
Brief description of the changes

## 解决的问题
Fixes #<issue-number>

## 🔴 严重问题修复
- Bullet point for each critical fix

## ⚠️ 安全风险修复
- Security improvements

## 📝 代码质量改进
- Code quality enhancements

## 测试建议
- [ ] Test case 1
- [ ] Test case 2

## 关联 Issue
Closes #<issue-number>
```

**Using GitHub MCP:**
```javascript
create_pull_request({
  owner: "username",
  repo: "repository",
  title: "fix: 修复 MySQL skill 安全问题",
  head: "fix/mysql-security-issues",
  base: "main",
  body: "PR description..."
})
```

**Using gh CLI:**
```bash
gh pr create \
  --title "fix: Security fixes" \
  --body "Closes #1" \
  --base main \
  --head fix/issue-1
```

## Common Fix Patterns

### Security Vulnerability Fixes

**Pattern 1: Remove Hardcoded Secrets**
1. Identify all hardcoded credentials
2. Replace with placeholders
3. Update .gitignore
4. Document in README how to configure

**Pattern 2: Add Input Validation**
1. Create validation functions
2. Apply to all user inputs
3. Add error messages
4. Write unit tests

**Pattern 3: Parameterize SQL Queries**
1. Find dynamic SQL construction
2. Replace with parameterized queries
3. Add identifier validation
4. Test with malicious inputs

### Code Quality Improvements

**Pattern 1: Improve Error Handling**
1. Identify bare `except` clauses
2. Specify exception types
3. Add descriptive error messages
4. Log errors appropriately

**Pattern 2: Add Documentation**
1. Document public APIs
2. Add docstrings
3. Update README
4. Include examples

**Pattern 3: Refactor for Clarity**
1. Extract complex logic into functions
2. Improve variable naming
3. Remove code duplication
4. Add comments for complex sections

## Handling Edge Cases

### Multiple Files Modified

**Strategy:**
- Group related changes in commits
- Test after each major change
- Create checklist to track progress

### Breaking Changes

**Strategy:**
- Version bump if needed
- Update CHANGELOG
- Document migration steps
- Notify in PR description

### Dependency Updates

**Strategy:**
- Update requirements.txt or package.json
- Test with new versions
- Document breaking changes
- Consider backwards compatibility

### Complex Issues

**Strategy:**
- Break into smaller sub-tasks
- Create multiple commits
- Request clarification if needed
- Add TODO comments for follow-up

## Best Practices

### Code Changes

- **Minimal scope**: Only fix what the issue describes
- **No over-engineering**: Avoid unnecessary refactoring
- **Test coverage**: Ensure changes are tested
- **Backwards compatible**: Avoid breaking existing functionality

### Commit Hygiene

- **Atomic commits**: One logical change per commit
- **Clear messages**: Describe what and why
- **Sign commits**: Use GPG if required
- **No secrets**: Never commit sensitive data

### Pull Request Quality

- **Self-review**: Check your own PR first
- **Description**: Explain changes clearly
- **Link issues**: Use "Closes #N" syntax
- **Request reviews**: Tag appropriate reviewers

### Communication

- **Issue updates**: Comment on progress
- **Ask questions**: Clarify ambiguities early
- **Document decisions**: Explain trade-offs
- **Request feedback**: Engage with reviewers

## Troubleshooting

### Git Push Failed

**Problem:** Authentication or permission errors

**Solutions:**
```bash
# Switch to SSH
git remote set-url origin git@github.com:user/repo.git

# Or use gh CLI
gh auth login

# Or use credential helper
git config credential.helper store
```

### GitHub API 403 Errors

**Problem:** Insufficient token permissions

**Solutions:**
1. Check token scopes in GitHub Settings
2. Regenerate token with required permissions:
   - `repo` - Full repository access
   - `workflow` - Update workflows
3. Update MCP configuration

### Merge Conflicts

**Problem:** Branch diverged from base

**Solutions:**
```bash
# Update base branch
git checkout main
git pull origin main

# Rebase fix branch
git checkout fix/issue-branch
git rebase main

# Resolve conflicts and continue
git add resolved-file.py
git rebase --continue

# Force push (carefully!)
git push -f origin fix/issue-branch
```

### Tests Failing

**Problem:** Changes broke existing tests

**Solutions:**
1. Run tests locally before pushing
2. Fix the failing tests or update if behavior changed
3. Add new tests for new functionality
4. Ensure CI passes before requesting review

## Security Considerations

### Credential Rotation

If secrets were exposed:
1. Rotate compromised credentials immediately
2. Check git history for exposure scope
3. Use tools like `git-secrets` or `truffleHog`
4. Consider rewriting history (dangerous!)

### Secure Development

- Review all changes for security impact
- Use static analysis tools (Bandit, SonarQube)
- Follow OWASP guidelines
- Enable security scanning in CI

### Access Control

- Use least-privilege tokens
- Limit branch protection rules
- Require reviews for sensitive changes
- Enable 2FA for GitHub account

## Example End-to-End Workflow

**Scenario:** Fix security issues in MySQL skill (Issue #1)

1. **Read issue:**
   ```bash
   # Issue describes hardcoded password, SQL injection, missing validation
   ```

2. **Create branch:**
   ```bash
   git checkout -b fix/mysql-security-issues
   ```

3. **Fix hardcoded password:**
   ```bash
   # Edit mysql_config.example.json
   # Replace real password with placeholder
   ```

4. **Add input validation:**
   ```python
   # Add validate_identifier() function
   # Apply to describe_table() and list_tables()
   ```

5. **Restrict SQL operations:**
   ```python
   # Modify execute_query() to only allow SELECT
   ```

6. **Update .gitignore:**
   ```bash
   # Add mysql_config.json exclusion
   ```

7. **Commit changes:**
   ```bash
   git add -A
   git commit -m "fix: 修复 MySQL skill 安全问题"
   ```

8. **Push to remote:**
   ```bash
   git push -u origin fix/mysql-security-issues
   ```

9. **Create PR:**
   ```bash
   # Use GitHub MCP or gh CLI
   # Link to Issue #1 with "Closes #1"
   ```

10. **Result:**
    - PR created: https://github.com/user/repo/pull/2
    - Linked to issue
    - Ready for review

## Resources

- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Best Practices](https://git-scm.com/book/en/v2)
- [GitHub Pull Request Best Practices](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests)
