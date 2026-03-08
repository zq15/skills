---
name: session-advisor
description: "Analyze Claude Code session data and provide personalized usage recommendations. Use when the user asks for: session analysis, usage suggestions, workflow optimization, skill recommendations, 分析会话、给出使用建议、推荐 skill、优化工作流, or similar requests to reflect on how Claude is being used."
---

# Session Advisor

Analyze the current session and historical usage data, then provide actionable recommendations.

## Step 1: Collect Context

Run the data collection script:

```bash
python3 ~/.claude/skills/session-advisor/scripts/collect_context.py
```

> **Note**: Tool stats and bash command history depend on `~/.claude/tool_calls.log`. If this file is empty or missing, the analysis will rely solely on the current session conversation. To enable tool logging, configure a `PostToolUse` hook in Claude Code settings.

This outputs JSON with:
- `tool_stats` — tool call frequency and avg duration
- `recent_bash_commands` — recent shell commands (pattern detection)
- `installed_skills` — available skills with descriptions
- `claude_md` — global CLAUDE.md content
- `log_total` — number of log entries analyzed

## Step 2: Analyze

Combine collected data with the **current session conversation** to analyze:

### A. New Skill Opportunities
Look for repetitive patterns in `recent_bash_commands` and current session tasks:
- Same script paths called repeatedly → candidate for a skill
- Multi-step workflows done manually → wrap in a skill
- Domain-specific queries (DB, API, deploy) → create specialized skill

### B. Workflow Improvements
Examine `tool_stats`:
- High `Bash` count with long avg_ms → identify automatable commands
- High `Read`/`Grep` count → suggest using codebase-retrieval or Serena tools
- Repeated file edits on same paths → consider if a script would be faster

### C. Skill Recommendations
Cross-reference what the user did manually in the session vs `installed_skills`:
- If user ran git operations manually but `github` skill exists → recommend it
- If user queried DB via Bash but `mysql-database` skill exists → recommend it
- Identify installed skills not yet used that match recent tasks

### D. Error Patterns
Look in current session for:
- Commands that failed and were retried
- Repeated debugging cycles
- Confusion about file paths or tool behavior → suggest CLAUDE.md customization

## Step 3: Output Recommendations

Structure the output as follows:

```
## 会话分析报告

**分析范围：** 最近 N 条工具调用 + 当前会话

### 🔧 建议创建的新 Skill
- **skill-name**: [具体原因，基于观察到的重复操作]

### ⚡ 工作流改进
- [具体建议，说明当前做法和改进方向]

### 📦 推荐使用的现有 Skill
- **skill-name**: [为什么现在适合用它]

### 🐛 发现的问题模式
- [问题描述 + 解决建议]

### 📊 工具使用概览
[简短的工具使用统计摘要]
```

## Notes

- Focus on **actionable** recommendations, not just observations
- Prioritize recommendations by frequency of occurrence
- If data is sparse (< 50 log entries), rely more on current session analysis
- Skip sections with no findings rather than filling with generic advice
