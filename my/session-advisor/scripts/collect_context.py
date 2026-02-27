#!/usr/bin/env python3
"""
Collect Claude Code session context for analysis:
- Tool call statistics from ~/.claude/tool_calls.log
- Installed skills from ~/.claude/skills/
- CLAUDE.md content
- Recent Bash commands for pattern detection
"""

import json
import sys
from pathlib import Path
from collections import defaultdict

LOG_FILE = Path.home() / ".claude" / "tool_calls.log"
SKILLS_DIR = Path.home() / ".claude" / "skills"
CLAUDE_MD = Path.home() / ".claude" / "CLAUDE.md"


def load_logs(limit=500):
    if not LOG_FILE.exists():
        return []
    logs = []
    with open(LOG_FILE) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    logs.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return logs[-limit:]


def analyze_tools(logs):
    stats = defaultdict(lambda: {"count": 0, "total_ms": 0})
    for log in logs:
        t = log.get("tool_name", "unknown")
        stats[t]["count"] += 1
        stats[t]["total_ms"] += log.get("duration_ms", 0)
    return sorted(
        [{"tool": t, "count": s["count"], "avg_ms": round(s["total_ms"] / s["count"])}
         for t, s in stats.items()],
        key=lambda x: x["count"], reverse=True
    )


def extract_bash_commands(logs, top_n=30):
    """Extract recent unique Bash commands for pattern analysis."""
    commands = []
    for log in reversed(logs):
        if log.get("tool_name") == "Bash":
            cmd = log.get("input", {}).get("command", "")
            if cmd:
                commands.append(cmd[:200])
    return commands[:top_n]


def list_skills():
    if not SKILLS_DIR.exists():
        return []
    skills = []
    for d in sorted(SKILLS_DIR.iterdir()):
        if d.is_dir():
            skill_md = d / "SKILL.md"
            desc = ""
            if skill_md.exists():
                for line in skill_md.read_text().splitlines():
                    if line.startswith("description:"):
                        desc = line.replace("description:", "").strip().strip('"')
                        break
            skills.append({"name": d.name, "description": desc[:120]})
    return skills


def read_claude_md():
    if not CLAUDE_MD.exists():
        return ""
    return CLAUDE_MD.read_text()[:3000]


def main():
    logs = load_logs()
    data = {
        "log_total": len(logs),
        "tool_stats": analyze_tools(logs),
        "recent_bash_commands": extract_bash_commands(logs),
        "installed_skills": list_skills(),
        "claude_md": read_claude_md(),
    }
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
