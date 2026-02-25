---
name: register-project
description: "Register the current project into ~/.claude/CLAUDE.md under the ## Projects section. Use when the user says: 'register this project', 'register current project', 'add this project to CLAUDE.md', '注册当前项目', '把这个项目加到 CLAUDE.md'."
---

# Register Project

Registers the current project's name, path, and description into the `## Projects` section of `~/.claude/CLAUDE.md`, so Claude can discover and reference it from any working directory.

## Steps

1. **Get project description** — if the user didn't provide one, ask:
   > "请简单描述一下这个项目（可选，直接回车跳过）："

2. **Run the registration script:**

   Without description:
   ```bash
   python3 /root/ai/skills/my/register-project/scripts/register.py
   ```

   With description:
   ```bash
   python3 /root/ai/skills/my/register-project/scripts/register.py --desc "项目描述"
   ```

   Optional overrides:
   ```bash
   python3 /root/ai/skills/my/register-project/scripts/register.py \
     --desc "描述" \
     --name "custom-name" \
     --path "/custom/path"
   ```

3. **Show the result** — display the written entry and confirm success to the user.

## Entry Format

```
## Projects

- **repo-name** (`/absolute/path`): 项目简介
```

## Notes

- The script auto-detects the project name from `git remote get-url origin`, falling back to the directory name.
- If the project path is already registered, the entry is updated in place.
- If the `## Projects` section doesn't exist in `CLAUDE.md`, it is created automatically.
