#!/usr/bin/env python3
"""Register current project into ~/.claude/CLAUDE.md under ## Projects section."""

import argparse
import os
import subprocess
import sys


CLAUDE_MD = os.path.expanduser("~/.claude/CLAUDE.md")
PROJECTS_HEADER = "## Projects"


def get_project_name(path: str) -> str:
    try:
        url = subprocess.check_output(
            ["git", "remote", "get-url", "origin"],
            cwd=path, stderr=subprocess.DEVNULL, text=True
        ).strip()
        # Extract repo name from URL (handles https and ssh formats)
        name = url.rstrip("/").split("/")[-1]
        if name.endswith(".git"):
            name = name[:-4]
        return name
    except Exception:
        return os.path.basename(path)


def read_claude_md() -> str:
    if not os.path.exists(CLAUDE_MD):
        return ""
    with open(CLAUDE_MD, "r", encoding="utf-8") as f:
        return f.read()


def write_claude_md(content: str) -> None:
    with open(CLAUDE_MD, "w", encoding="utf-8") as f:
        f.write(content)


def format_entry(name: str, path: str, desc: str) -> str:
    if desc:
        return f"- **{name}** (`{path}`): {desc}"
    else:
        return f"- **{name}** (`{path}`)"


def register(path: str, name: str, desc: str) -> None:
    content = read_claude_md()
    new_entry = format_entry(name, path, desc)

    if PROJECTS_HEADER not in content:
        # Append the section
        sep = "\n" if content.endswith("\n") else "\n\n"
        content = content + sep + PROJECTS_HEADER + "\n\n" + new_entry + "\n"
        print(f"Created '{PROJECTS_HEADER}' section and added entry.")
    else:
        lines = content.splitlines(keepends=True)
        in_section = False
        section_start = None
        next_section = None
        existing_entry_line = None

        for i, line in enumerate(lines):
            if line.strip() == PROJECTS_HEADER:
                in_section = True
                section_start = i
                continue
            if in_section:
                if line.startswith("## ") and i != section_start:
                    next_section = i
                    break
                # Check if this path is already registered
                if f"`{path}`" in line:
                    existing_entry_line = i

        if existing_entry_line is not None:
            lines[existing_entry_line] = new_entry + "\n"
            content = "".join(lines)
            print(f"Updated existing entry for '{path}'.")
        else:
            # Insert before next section or at end
            insert_at = next_section if next_section is not None else len(lines)
            # Ensure blank line before next section
            while insert_at > 0 and lines[insert_at - 1].strip() == "":
                insert_at -= 1
            lines.insert(insert_at, new_entry + "\n")
            content = "".join(lines)
            print(f"Added new entry for '{name}'.")

    write_claude_md(content)
    print(f"\nEntry: {new_entry}")
    print(f"Written to: {CLAUDE_MD}")


def main():
    parser = argparse.ArgumentParser(description="Register current project in CLAUDE.md")
    parser.add_argument("--desc", default="", help="Project description")
    parser.add_argument("--path", default=os.getcwd(), help="Project path (default: cwd)")
    parser.add_argument("--name", default="", help="Project name (default: git repo name or dir name)")
    args = parser.parse_args()

    path = os.path.abspath(args.path)
    name = args.name or get_project_name(path)
    desc = args.desc

    print(f"Registering project: {name}")
    print(f"  Path: {path}")
    print(f"  Desc: {desc or '(none)'}")
    print()

    register(path, name, desc)


if __name__ == "__main__":
    main()
