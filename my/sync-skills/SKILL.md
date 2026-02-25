---
name: sync-skills
description: "Sync custom skills from /root/ai/skills/my/ to the Claude global skills directory (~/.claude/skills/). Use when the user wants to: (1) publish or deploy their local skills to Claude, (2) sync skill updates to the global directory, (3) says 'sync skills', 'deploy skills', or similar."
---

# Sync Skills

Syncs all skills in `/root/ai/skills/my/` to `~/.claude/skills/`.

## Steps

Run the sync script:

```bash
python3 /root/ai/skills/my/sync-skills/scripts/sync.py
```

The script copies every subdirectory containing a `SKILL.md` from `my/` to `~/.claude/skills/`, overwriting existing versions. After running, confirm the synced skills with the user.
