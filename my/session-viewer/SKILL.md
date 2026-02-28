---
name: session-viewer
description: "View and query Claude Code session history from multiple dimensions: list sessions by date/project, show session messages, search keywords across sessions, or list all projects. Use when the user asks to: view sessions, find a past conversation, search session history, list today's sessions, 查看会话、搜索历史会话、列出今天的会话."
---

# Session Viewer

Query Claude Code session history stored in `~/.claude/projects/`.

## Script

```
~/.claude/skills/session-viewer/scripts/sessions.py
```

## Commands

### List sessions
```bash
# All sessions
python3 sessions.py list

# Filter by date
python3 sessions.py list --date 2026-02-28

# Filter by project name (partial match)
python3 sessions.py list --project lixiang-mall
```

### Today's sessions (shortcut)
```bash
python3 sessions.py today
```

### Show session messages
```bash
# Full session (session_id prefix, min 4 chars)
python3 sessions.py show fe75

# Limit to first N messages
python3 sessions.py show fe75 --limit 10
```

### Search keyword across sessions
```bash
# Search all sessions
python3 sessions.py search "物流"

# Limit to a specific date
python3 sessions.py search "minGrossProfit" --date 2026-02-28
```

### List all projects
```bash
python3 sessions.py projects
```

## Usage Instructions

When this skill is invoked:

1. **Determine which command** fits the user's request:
   - "今天的会话" / "today's sessions" → `today`
   - "列出会话" / "list sessions" + optional date/project → `list`
   - "查看某个会话内容" / "show session X" → `show SESSION_ID`
   - "搜索XX关键词" / "search for X" → `search KEYWORD`
   - "有哪些项目" / "list projects" → `projects`

2. **Run the command** using Bash tool with full script path:
   ```bash
   python3 ~/.claude/skills/session-viewer/scripts/sessions.py <command> [args]
   ```

3. **Present results** directly to the user.

## Output Format

### `list` / `today`
```
Time         Session ID Branch           Msgs  First message
fe75592f     dev              137  帮我搜索项目中的物流信息表...
             project: -mnt-d-bian-lixiang-mall
```

### `show`
```
Session : fe75592f-...
Project : -mnt-d-bian-lixiang-mall
Branch  : dev
Time    : 02-28 14:42 → 02-28 15:08
Messages: 137
---
[02-28 14:42] USER: 帮我搜索项目中的物流信息表...
[02-28 14:42] ASSISTANT: 先搜索物流相关的表名...
```

### `search`
```
[02-28 14:42] fe75592f | -mnt-d-bian-lixiang-mall
  帮我搜索项目中的物流信息表有哪些位置写入
  ...匹配上下文片段...
```
