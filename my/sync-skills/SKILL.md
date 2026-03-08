---
name: sync-skills
description: "Sync custom skills to the Claude global skills directory (~/.claude/skills/). Use when the user wants to: (1) publish or deploy their local skills to Claude, (2) sync skill updates to the global directory, (3) says 'sync skills', 'deploy skills', 'sync my skills', '同步 skill', '发布 skill', '更新 skill', '同步一下' or similar."
---

# Sync Skills

Syncs all skills in the `my/` directory to `~/.claude/skills/`.

## Steps

Run the sync script (installed location):

```bash
python3 ~/.claude/skills/sync-skills/scripts/sync.py
```

The script copies every subdirectory containing a `SKILL.md` from `my/` to `~/.claude/skills/`, overwriting existing versions. After running, confirm the synced skills with the user.
