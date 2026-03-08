#!/usr/bin/env python3
"""Sync skills from /root/ai/skills/my/ to ~/.claude/skills/"""

import re
import shutil
import sys
from pathlib import Path

SRC = Path(__file__).parent.parent.parent
DST = Path.home() / ".claude/skills"
PROMPT_SRC = SRC.parent / "prompt" / "CLAUDE.md"
PROMPT_DST = Path.home() / ".claude" / "prompt" / "CLAUDE.md"

# Sections managed by sync (these will be updated from source)
MANAGED_SECTIONS = ["## Projects", "## 项目", "## 常用工具", "## 工具", "## 其他"]


def parse_sections(content: str) -> dict:
    """Parse a CLAUDE.md file into sections."""
    sections = {}
    current_section = ""
    current_content = []

    for line in content.split("\n"):
        # Check if this is a section header
        match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if match:
            # Save previous section
            if current_section:
                sections[current_section] = "\n".join(current_content).strip()
            # Start new section
            current_section = match.group(2)
            # Check if it's a managed section
            for managed in MANAGED_SECTIONS:
                if managed in current_section:
                    current_section = managed
                    break
            current_content = [line]
        else:
            current_content.append(line)

    # Save last section
    if current_section:
        sections[current_section] = "\n".join(current_content).strip()

    return sections


def merge_claude_md(source_content: str, target_content: str) -> str:
    """Merge source into target, updating only managed sections."""
    source_sections = parse_sections(source_content)
    target_sections = parse_sections(target_content)

    # Update managed sections from source, keep others from target
    for section in source_sections:
        if section in MANAGED_SECTIONS:
            target_sections[section] = source_sections[section]

    # Build merged content
    lines = []
    for section, content in target_sections.items():
        if lines:
            lines.append("")  # Empty line between sections
        lines.append(content)

    return "\n".join(lines)


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
        shutil.copytree(skill_dir, dest, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))
        synced.append(skill_dir.name)

    print(f"Synced {len(synced)} skills to {DST}:")
    for name in synced:
        print(f"  ✓ {name}")

    # Sync global CLAUDE.md
    if PROMPT_SRC.exists():
        PROMPT_DST.parent.mkdir(parents=True, exist_ok=True)
        source_content = PROMPT_SRC.read_text()

        if not PROMPT_DST.exists():
            shutil.copy2(PROMPT_SRC, PROMPT_DST)
            print(f"\nSynced global CLAUDE.md to {PROMPT_DST}")
        else:
            # Merge with existing file
            target_content = PROMPT_DST.read_text()
            merged_content = merge_claude_md(source_content, target_content)
            PROMPT_DST.write_text(merged_content)
            print(f"\nMerged global CLAUDE.md to {PROMPT_DST}")


if __name__ == "__main__":
    sync()
