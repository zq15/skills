#!/usr/bin/env python3
"""Sync skills from /root/ai/skills/my/ to ~/.claude/skills/"""

import shutil
import sys
from pathlib import Path

SRC = Path("/root/ai/skills/my")
DST = Path.home() / ".claude/skills"


def sync():
    DST.mkdir(parents=True, exist_ok=True)
    synced = []

    for skill_dir in sorted(SRC.iterdir()):
        if not skill_dir.is_dir():
            continue
        if not (skill_dir / "SKILL.md").exists():
            continue

        dest = DST / skill_dir.name
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(skill_dir, dest)
        synced.append(skill_dir.name)

    print(f"Synced {len(synced)} skills to {DST}:")
    for name in synced:
        print(f"  ✓ {name}")


if __name__ == "__main__":
    sync()
