---
name: github
description: "Interact with GitHub using the `gh` CLI. Use this skill whenever the user mentions PRs, pull requests, issues, CI/CD, workflow runs, GitHub Actions, releases, branches, code review, or any GitHub-related operations — even if phrased as 'check the build', 'create a ticket', 'look at the repo', 'why did CI fail', 'merge this PR', or 'open a PR'. Use `gh issue`, `gh pr`, `gh run`, `gh api`, and `gh search` to accomplish tasks."
metadata:
  {
    "openclaw":
      {
        "emoji": "🐙",
        "requires": { "bins": ["gh"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "gh",
              "bins": ["gh"],
              "label": "Install GitHub CLI (brew)",
            },
            {
              "id": "apt",
              "kind": "apt",
              "package": "gh",
              "bins": ["gh"],
              "label": "Install GitHub CLI (apt)",
            },
          ],
      },
  }
---

# GitHub Skill

Use the `gh` CLI to interact with GitHub. Always specify `--repo owner/repo` when not in a git directory, or use URLs directly.

## Pull Requests

List open PRs:

```bash
gh pr list --repo owner/repo
```

Create a PR:

```bash
gh pr create --repo owner/repo --title "Title" --body "Description" --base main --head feature-branch
```

View PR details and CI status:

```bash
gh pr view 55 --repo owner/repo
gh pr checks 55 --repo owner/repo
```

Review, approve, or request changes:

```bash
gh pr review 55 --repo owner/repo --approve
gh pr review 55 --repo owner/repo --request-changes --body "Please fix X"
gh pr review 55 --repo owner/repo --comment --body "Looks good, one nit"
```

Merge a PR:

```bash
gh pr merge 55 --repo owner/repo --squash   # squash merge
gh pr merge 55 --repo owner/repo --merge    # regular merge
gh pr merge 55 --repo owner/repo --rebase   # rebase merge
```

## CI / Workflow Runs

List recent workflow runs:

```bash
gh run list --repo owner/repo --limit 10
```

View a run and see which steps failed:

```bash
gh run view <run-id> --repo owner/repo
gh run view <run-id> --repo owner/repo --log-failed
```

## Issues

List issues:

```bash
gh issue list --repo owner/repo --state open --label bug
```

Create an issue:

```bash
gh issue create --repo owner/repo --title "Title" --body "Body" --label bug
```

If `gh issue create` fails with `Resource not accessible by personal access token`, fall back to REST:

```bash
gh api repos/owner/repo/issues \
  --method POST \
  --field title="Issue title" \
  --field body="$(cat draft.md)" \
  2>&1 | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('html_url', d))"
```

Close an issue:

```bash
gh issue close 42 --repo owner/repo
```

## Search

Search issues and PRs across GitHub:

```bash
gh search issues "label:bug repo:owner/repo" --state open
gh search prs "review-requested:@me" --state open
```

## Releases

List releases:

```bash
gh release list --repo owner/repo
```

Create a release:

```bash
gh release create v1.0.0 --repo owner/repo --title "v1.0.0" --notes "Release notes"
```

## API for Advanced Queries

The `gh api` command is useful for data not available through other subcommands.

```bash
# Get PR with specific fields
gh api repos/owner/repo/pulls/55 --jq '.title, .state, .user.login'

# List PR comments
gh api repos/owner/repo/issues/55/comments --jq '.[].body'
```

## JSON Output

Most commands support `--json` and `--jq` for structured output:

```bash
gh issue list --repo owner/repo --json number,title --jq '.[] | "\(.number): \(.title)"'
gh pr list --repo owner/repo --json number,title,headRefName,state
```

## Tips

- Always use `--repo owner/repo` when not inside a git directory
- Use `gh auth status` to check authentication state
- `gh browse` opens the current repo in the browser
