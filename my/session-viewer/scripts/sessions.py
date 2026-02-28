#!/usr/bin/env python3
"""
Claude Code session viewer - query sessions from multiple dimensions.

Usage:
  sessions.py list [--date YYYY-MM-DD] [--project NAME]
  sessions.py today
  sessions.py show SESSION_ID [--limit N]
  sessions.py search KEYWORD [--date YYYY-MM-DD]
  sessions.py projects
  sessions.py tokens SESSION_ID
  sessions.py cost [--date YYYY-MM-DD] [--project NAME]
"""

# Sonnet 4.x pricing (USD per 1M tokens) — update if pricing changes
PRICE = {
    "input":          3.00,
    "output":        15.00,
    "cache_write":    3.75,
    "cache_read":     0.30,
}

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone

PROJECTS_DIR = Path.home() / ".claude" / "projects"


def parse_sessions(project_dir: Path) -> list[dict]:
    """Parse all session files in a project directory."""
    sessions = []
    for f in project_dir.glob("*.jsonl"):
        session_id = f.stem
        entries = []
        try:
            with open(f, encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if line:
                        try:
                            entries.append(json.loads(line))
                        except json.JSONDecodeError:
                            pass
        except Exception:
            continue

        messages = [e for e in entries if e.get("type") in ("user", "assistant")]
        if not messages:
            continue

        first = messages[0]
        last = messages[-1]

        first_user = next(
            (e for e in messages if e.get("type") == "user"),
            None,
        )
        first_user_text = ""
        if first_user:
            content = first_user.get("message", {}).get("content", "")
            if isinstance(content, list):
                for c in content:
                    if isinstance(c, dict) and c.get("type") == "text":
                        first_user_text = c["text"]
                        break
            elif isinstance(content, str):
                first_user_text = content

        sessions.append({
            "session_id": session_id,
            "project": project_dir.name,
            "cwd": first.get("cwd", ""),
            "git_branch": first.get("gitBranch", ""),
            "start_time": first.get("timestamp", ""),
            "end_time": last.get("timestamp", ""),
            "message_count": len(messages),
            "first_user_msg": first_user_text[:120].replace("\n", " "),
            "file": f,
            "entries": entries,
        })
    return sessions


def load_all_sessions() -> list[dict]:
    sessions = []
    if not PROJECTS_DIR.exists():
        return sessions
    for project_dir in PROJECTS_DIR.iterdir():
        if project_dir.is_dir():
            sessions.extend(parse_sessions(project_dir))
    sessions.sort(key=lambda s: s["start_time"], reverse=True)
    return sessions


def format_time(iso: str) -> str:
    if not iso:
        return "-"
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone()
        return dt.strftime("%m-%d %H:%M")
    except Exception:
        return iso[:16]


def filter_by_date(sessions: list[dict], date_str: str) -> list[dict]:
    try:
        target = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print(f"Invalid date format: {date_str}. Use YYYY-MM-DD.")
        sys.exit(1)
    result = []
    for s in sessions:
        if not s["start_time"]:
            continue
        try:
            dt = datetime.fromisoformat(s["start_time"].replace("Z", "+00:00")).astimezone()
            if dt.date() == target:
                result.append(s)
        except Exception:
            pass
    return result


def filter_by_project(sessions: list[dict], project: str) -> list[dict]:
    return [s for s in sessions if project.lower() in s["project"].lower()]


def cmd_list(args):
    sessions = load_all_sessions()
    if args.date:
        sessions = filter_by_date(sessions, args.date)
    if args.project:
        sessions = filter_by_project(sessions, args.project)

    if not sessions:
        print("No sessions found.")
        return

    print(f"{'Time':<12} {'Session ID':<10} {'Branch':<16} {'Msgs':>4}  {'First message'}")
    print("-" * 90)
    for s in sessions:
        sid = s["session_id"][:8]
        branch = (s["git_branch"] or "-")[:15]
        msg = s["first_user_msg"][:50]
        print(f"{format_time(s['start_time']):<12} {sid:<10} {branch:<16} {s['message_count']:>4}  {msg}")
        # Show project as sub-line if no filter
        if not args.project:
            print(f"{'':12} project: {s['project']}")


def cmd_today(args):
    today = datetime.now().strftime("%Y-%m-%d")
    args.date = today
    args.project = None
    cmd_list(args)


def cmd_show(args):
    sessions = load_all_sessions()
    matches = [s for s in sessions if s["session_id"].startswith(args.session_id)]
    if not matches:
        print(f"Session not found: {args.session_id}")
        sys.exit(1)

    s = matches[0]
    print(f"Session : {s['session_id']}")
    print(f"Project : {s['project']}")
    print(f"Branch  : {s['git_branch'] or '-'}")
    print(f"Time    : {format_time(s['start_time'])} → {format_time(s['end_time'])}")
    print(f"Messages: {s['message_count']}")
    print("=" * 80)

    messages = [e for e in s["entries"] if e.get("type") in ("user", "assistant")]
    limit = args.limit if args.limit else len(messages)
    for e in messages[:limit]:
        role = e.get("type", "?").upper()
        content = e.get("message", {}).get("content", "")
        if isinstance(content, list):
            parts = []
            for c in content:
                if isinstance(c, dict):
                    if c.get("type") == "text":
                        parts.append(c["text"])
                    elif c.get("type") == "tool_use":
                        parts.append(f"[tool: {c.get('name')}]")
            text = " ".join(parts)
        else:
            text = content or ""

        text = text.strip().replace("\n", " ")[:300]
        ts = format_time(e.get("timestamp", ""))
        print(f"[{ts}] {role}: {text}")


def cmd_search(args):
    keyword = args.keyword.lower()
    sessions = load_all_sessions()
    if args.date:
        sessions = filter_by_date(sessions, args.date)

    found = 0
    for s in sessions:
        hits = []
        messages = [e for e in s["entries"] if e.get("type") in ("user", "assistant")]
        for e in messages:
            content = e.get("message", {}).get("content", "")
            if isinstance(content, list):
                text = " ".join(
                    c.get("text", "") for c in content
                    if isinstance(c, dict) and c.get("type") == "text"
                )
            else:
                text = content or ""
            if keyword in text.lower():
                snippet = text.strip().replace("\n", " ")
                idx = snippet.lower().find(keyword)
                start = max(0, idx - 40)
                hits.append(f"  ...{snippet[start:start+120]}...")

        if hits:
            found += 1
            print(f"\n[{format_time(s['start_time'])}] {s['session_id'][:8]} | {s['project']}")
            print(f"  {s['first_user_msg'][:80]}")
            for h in hits[:3]:
                print(h)

    if found == 0:
        print(f"No sessions found containing: {args.keyword}")
    else:
        print(f"\n--- Found in {found} session(s) ---")


def extract_usage(entries: list[dict]) -> dict:
    """Sum token usage across all assistant turns in a session."""
    u = {"input": 0, "output": 0, "cache_write": 0, "cache_read": 0, "turns": 0}
    for e in entries:
        if e.get("type") != "assistant":
            continue
        usage = e.get("message", {}).get("usage")
        if not usage:
            continue
        u["input"]       += usage.get("input_tokens", 0)
        u["output"]      += usage.get("output_tokens", 0)
        u["cache_write"] += usage.get("cache_creation_input_tokens", 0)
        u["cache_read"]  += usage.get("cache_read_input_tokens", 0)
        u["turns"]       += 1
    return u


def calc_cost(u: dict) -> float:
    return (
        u["input"]       / 1_000_000 * PRICE["input"] +
        u["output"]      / 1_000_000 * PRICE["output"] +
        u["cache_write"] / 1_000_000 * PRICE["cache_write"] +
        u["cache_read"]  / 1_000_000 * PRICE["cache_read"]
    )


def fmt_tok(n: int) -> str:
    if n >= 1_000_000:
        return f"{n/1_000_000:.2f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)


def cache_hit_rate(u: dict) -> str:
    total_in = u["input"] + u["cache_write"] + u["cache_read"]
    if total_in == 0:
        return "N/A"
    return f"{u['cache_read'] / total_in * 100:.1f}%"


def cmd_tokens(args):
    sessions = load_all_sessions()
    matches = [s for s in sessions if s["session_id"].startswith(args.session_id)]
    if not matches:
        print(f"Session not found: {args.session_id}")
        sys.exit(1)

    s = matches[0]
    u = extract_usage(s["entries"])
    cost = calc_cost(u)
    total_in = u["input"] + u["cache_write"] + u["cache_read"]

    print(f"Session : {s['session_id']}")
    print(f"Project : {s['project']}")
    print(f"Time    : {format_time(s['start_time'])} → {format_time(s['end_time'])}")
    print(f"Turns   : {u['turns']}")
    print()
    print(f"{'Token breakdown':}")
    print(f"  Input (non-cached) : {fmt_tok(u['input']):>10}   ${u['input']/1e6*PRICE['input']:.4f}")
    print(f"  Cache write        : {fmt_tok(u['cache_write']):>10}   ${u['cache_write']/1e6*PRICE['cache_write']:.4f}")
    print(f"  Cache read         : {fmt_tok(u['cache_read']):>10}   ${u['cache_read']/1e6*PRICE['cache_read']:.4f}")
    print(f"  Output             : {fmt_tok(u['output']):>10}   ${u['output']/1e6*PRICE['output']:.4f}")
    print(f"  {'─'*40}")
    print(f"  Total input        : {fmt_tok(total_in):>10}")
    print(f"  Cache hit rate     : {cache_hit_rate(u):>10}")
    print(f"  Estimated cost     : {'$' + f'{cost:.4f}':>10}")


def cmd_cost(args):
    sessions = load_all_sessions()
    if args.date:
        sessions = filter_by_date(sessions, args.date)
    if args.project:
        sessions = filter_by_project(sessions, args.project)

    if not sessions:
        print("No sessions found.")
        return

    print(f"{'Time':<12} {'Session':<10} {'Turns':>5} {'CacheHit':>9} {'Input':>8} {'CacheW':>8} {'CacheR':>8} {'Output':>8} {'Cost':>8}")
    print("-" * 100)

    grand = {"input": 0, "output": 0, "cache_write": 0, "cache_read": 0, "turns": 0}
    for s in sessions:
        u = extract_usage(s["entries"])
        cost = calc_cost(u)
        for k in grand:
            grand[k] += u[k]
        print(
            f"{format_time(s['start_time']):<12} "
            f"{s['session_id'][:8]:<10} "
            f"{u['turns']:>5} "
            f"{cache_hit_rate(u):>9} "
            f"{fmt_tok(u['input']):>8} "
            f"{fmt_tok(u['cache_write']):>8} "
            f"{fmt_tok(u['cache_read']):>8} "
            f"{fmt_tok(u['output']):>8} "
            f"${cost:.4f}"
        )

    if len(sessions) > 1:
        grand_cost = calc_cost(grand)
        print("-" * 100)
        print(
            f"{'TOTAL':<12} "
            f"{len(sessions)} sessions"
            f"{grand['turns']:>14} "
            f"{cache_hit_rate(grand):>9} "
            f"{fmt_tok(grand['input']):>8} "
            f"{fmt_tok(grand['cache_write']):>8} "
            f"{fmt_tok(grand['cache_read']):>8} "
            f"{fmt_tok(grand['output']):>8} "
            f"${grand_cost:.4f}"
        )


def cmd_projects(args):
    sessions = load_all_sessions()
    from collections import Counter
    counts = Counter(s["project"] for s in sessions)
    print(f"{'Project':<45} {'Sessions':>8}")
    print("-" * 55)
    for project, count in counts.most_common():
        print(f"{project:<45} {count:>8}")


def main():
    parser = argparse.ArgumentParser(description="Claude Code session viewer")
    sub = parser.add_subparsers(dest="cmd")

    p_list = sub.add_parser("list", help="List sessions")
    p_list.add_argument("--date", help="Filter by date (YYYY-MM-DD)")
    p_list.add_argument("--project", help="Filter by project name")

    sub.add_parser("today", help="List today's sessions")

    p_show = sub.add_parser("show", help="Show session messages")
    p_show.add_argument("session_id", help="Session ID prefix (min 4 chars)")
    p_show.add_argument("--limit", type=int, help="Max messages to show")

    p_search = sub.add_parser("search", help="Search keyword across sessions")
    p_search.add_argument("keyword", help="Keyword to search")
    p_search.add_argument("--date", help="Limit to specific date (YYYY-MM-DD)")

    sub.add_parser("projects", help="List all projects with session counts")

    p_tokens = sub.add_parser("tokens", help="Token usage breakdown for a session")
    p_tokens.add_argument("session_id", help="Session ID prefix")

    p_cost = sub.add_parser("cost", help="Cost analysis across sessions")
    p_cost.add_argument("--date", help="Filter by date (YYYY-MM-DD)")
    p_cost.add_argument("--project", help="Filter by project name")

    args = parser.parse_args()

    dispatch = {
        "list": cmd_list,
        "today": cmd_today,
        "show": cmd_show,
        "search": cmd_search,
        "projects": cmd_projects,
        "tokens": cmd_tokens,
        "cost": cmd_cost,
    }

    if args.cmd in dispatch:
        dispatch[args.cmd](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
