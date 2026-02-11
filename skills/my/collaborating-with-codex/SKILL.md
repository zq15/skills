---
name: collaborating-with-codex
description: Delegates coding tasks to Codex CLI for prototyping, debugging, and code review. Use when needing algorithm implementation, bug analysis, or code quality feedback. Supports multi-turn sessions via SESSION_ID.
---

## Quick Start

```bash
# 基本用法（默认 10 分钟超时）
python scripts/codex_bridge.py --cd "/path/to/project" --PROMPT "Your task"

# 自定义超时时间（单位：秒）
python scripts/codex_bridge.py --cd "/path/to/project" --PROMPT "Complex task" --timeout 1200
```

**Output:** JSON with `success`, `SESSION_ID`, `agent_messages`, and optional `error`.

> 💡 **遇到超时问题？** 如果任务在默认 10 分钟内未完成，可以尝试增加超时时间至 20 分钟：`--timeout 1200`

## Parameters

```
usage: codex_bridge.py [-h] --PROMPT PROMPT --cd CD [--sandbox {read-only,workspace-write,danger-full-access}] [--SESSION_ID SESSION_ID] [--skip-git-repo-check]
                       [--return-all-messages] [--image IMAGE] [--model MODEL] [--yolo] [--profile PROFILE] [--timeout TIMEOUT]

Codex Bridge

options:
  -h, --help            show this help message and exit
  --PROMPT PROMPT       Instruction for the task to send to codex.
  --cd CD               Set the workspace root for codex before executing the task.
  --sandbox {read-only,workspace-write,danger-full-access}
                        Sandbox policy for model-generated commands. Defaults to `read-only`.
  --SESSION_ID SESSION_ID
                        Resume the specified session of the codex. Defaults to `None`, start a new session.
  --skip-git-repo-check
                        Allow codex running outside a Git repository (useful for one-off directories).
  --return-all-messages
                        Return all messages (e.g. reasoning, tool calls, etc.) from the codex session. Set to `False` by default, only the agent's final reply message is
                        returned.
  --image IMAGE         Attach one or more image files to the initial prompt. Separate multiple paths with commas or repeat the flag.
  --model MODEL         The model to use for the codex session. This parameter is strictly prohibited unless explicitly specified by the user.
  --yolo                Run every command without approvals or sandboxing. Only use when `sandbox` couldn't be applied.
  --profile PROFILE     Configuration profile name to load from `~/.codex/config.toml`. This parameter is strictly prohibited unless explicitly specified by the user.
  --timeout TIMEOUT     Maximum execution time in seconds (default: 600s/10min). Set to 0 for no timeout.
```

## Multi-turn Sessions

**Always capture `SESSION_ID`** from the first response for follow-up:

```bash
# Initial task
python scripts/codex_bridge.py --cd "/project" --PROMPT "Analyze auth in login.py"

# Continue with SESSION_ID
python scripts/codex_bridge.py --cd "/project" --SESSION_ID "uuid-from-response" --PROMPT "Write unit tests for that"
```

## Common Patterns

**Prototyping (read-only, request diffs):**
```bash
python scripts/codex_bridge.py --cd "/project" --PROMPT "Generate unified diff to add logging"
```

**Debug with full trace:**
```bash
python scripts/codex_bridge.py --cd "/project" --PROMPT "Debug this error" --return-all-messages
```

## Timeout Control

### Default Behavior
- Default timeout: **600 seconds (10 minutes)**
- Tasks exceeding the timeout will be gracefully terminated
- The `SESSION_ID` is preserved even on timeout, allowing you to resume

### Custom Timeout Examples

```bash
# Short timeout for quick queries (2 minutes)
python scripts/codex_bridge.py --cd "/project" --PROMPT "List files" --timeout 120

# Extended timeout for complex tasks (20 minutes)
python scripts/codex_bridge.py --cd "/project" --PROMPT "Comprehensive refactoring" --timeout 1200

# Disable timeout (not recommended)
python scripts/codex_bridge.py --cd "/project" --PROMPT "Long task" --timeout 0
```

### Handling Timeout Errors

If you encounter a timeout:
1. **Increase the timeout**: Try `--timeout 1200` (20 minutes)
2. **Break down the task**: Split complex tasks into smaller steps
3. **Resume with SESSION_ID**: Use the returned SESSION_ID to continue the conversation

```bash
# First attempt times out
python scripts/codex_bridge.py --cd "/project" --PROMPT "Complex analysis" --timeout 600
# Returns: {"success": false, "SESSION_ID": "abc-123", "error": "[TIMEOUT] ..."}

# Resume with the same SESSION_ID
python scripts/codex_bridge.py --cd "/project" --SESSION_ID "abc-123" --PROMPT "Continue the analysis, focus on key areas" --timeout 1200
```
