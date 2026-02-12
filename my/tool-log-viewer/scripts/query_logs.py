#!/usr/bin/env python3
"""
Query and analyze Claude Code tool call logs.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Any

LOG_FILE = Path.home() / ".claude" / "tool_calls.log"


def load_logs() -> List[Dict[str, Any]]:
    """Load all log entries from the log file."""
    if not LOG_FILE.exists():
        return []

    logs = []
    with open(LOG_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    logs.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return logs


def format_duration(ms: float) -> str:
    """Format duration in a human-readable way."""
    if ms < 1000:
        return f"{ms:.0f}ms"
    elif ms < 60000:
        return f"{ms/1000:.2f}s"
    else:
        return f"{ms/60000:.1f}m"


def show_summary(logs: List[Dict[str, Any]]):
    """Show summary statistics of all tool calls."""
    if not logs:
        print("No tool calls recorded yet.")
        return

    # Calculate statistics
    tool_stats = defaultdict(lambda: {"count": 0, "total_time": 0, "times": []})

    for log in logs:
        tool = log.get("tool_name", "unknown")
        duration = log.get("duration_ms", 0)

        tool_stats[tool]["count"] += 1
        tool_stats[tool]["total_time"] += duration
        tool_stats[tool]["times"].append(duration)

    # Print summary
    print(f"\n{'='*70}")
    print(f"Tool Call Summary - Total: {len(logs)} calls")
    print(f"{'='*70}\n")

    print(f"{'Tool Name':<20} {'Count':>8} {'Avg Time':>12} {'Total Time':>15}")
    print(f"{'-'*70}")

    # Sort by count
    sorted_tools = sorted(tool_stats.items(), key=lambda x: x[1]["count"], reverse=True)

    for tool, stats in sorted_tools:
        avg_time = stats["total_time"] / stats["count"]
        print(f"{tool:<20} {stats['count']:>8} {format_duration(avg_time):>12} {format_duration(stats['total_time']):>15}")

    print(f"\n{'='*70}\n")


def show_recent(logs: List[Dict[str, Any]], limit: int = 10):
    """Show recent tool calls."""
    if not logs:
        print("No tool calls recorded yet.")
        return

    recent = logs[-limit:]

    print(f"\n{'='*70}")
    print(f"Recent {len(recent)} Tool Calls")
    print(f"{'='*70}\n")

    for i, log in enumerate(reversed(recent), 1):
        timestamp = log.get("timestamp", "N/A")
        tool = log.get("tool_name", "unknown")
        duration = log.get("duration_ms", 0)

        print(f"{i}. [{timestamp}] {tool} - {format_duration(duration)}")

    print(f"\n{'='*70}\n")


def show_detail(logs: List[Dict[str, Any]], index: int = -1):
    """Show detailed information for a specific call."""
    if not logs:
        print("No tool calls recorded yet.")
        return

    if index < 0:
        index = len(logs) + index

    if index < 0 or index >= len(logs):
        print(f"Invalid index: {index}. Valid range: 0-{len(logs)-1}")
        return

    log = logs[index]

    print(f"\n{'='*70}")
    print(f"Tool Call Detail (#{index + 1})")
    print(f"{'='*70}\n")

    print(f"Timestamp:    {log.get('timestamp', 'N/A')}")
    print(f"Tool Name:    {log.get('tool_name', 'unknown')}")
    print(f"Duration:     {format_duration(log.get('duration_ms', 0))}")
    print(f"Working Dir:  {log.get('cwd', 'N/A')}")
    print(f"Session ID:   {log.get('session_id', 'N/A')}")
    print(f"Tool Use ID:  {log.get('tool_use_id', 'N/A')}")

    print(f"\nInput:")
    print(json.dumps(log.get('input', {}), indent=2))

    result = log.get('result', {})
    if result:
        print(f"\nResult:")
        # Limit output length for readability
        result_str = json.dumps(result, indent=2)
        if len(result_str) > 1000:
            print(result_str[:1000] + "\n... (truncated)")
        else:
            print(result_str)

    print(f"\n{'='*70}\n")


def filter_by_tool(logs: List[Dict[str, Any]], tool_name: str):
    """Filter logs by tool name."""
    filtered = [log for log in logs if log.get("tool_name", "").lower() == tool_name.lower()]

    if not filtered:
        print(f"No calls found for tool: {tool_name}")
        return

    print(f"\n{'='*70}")
    print(f"Tool Calls for: {tool_name} ({len(filtered)} calls)")
    print(f"{'='*70}\n")

    for i, log in enumerate(filtered, 1):
        timestamp = log.get("timestamp", "N/A")
        duration = log.get("duration_ms", 0)

        print(f"{i}. [{timestamp}] {format_duration(duration)}")

    # Show statistics
    durations = [log.get("duration_ms", 0) for log in filtered]
    avg_duration = sum(durations) / len(durations)
    min_duration = min(durations)
    max_duration = max(durations)

    print(f"\nStatistics:")
    print(f"  Total Calls: {len(filtered)}")
    print(f"  Avg Time:    {format_duration(avg_duration)}")
    print(f"  Min Time:    {format_duration(min_duration)}")
    print(f"  Max Time:    {format_duration(max_duration)}")

    print(f"\n{'='*70}\n")


def show_slow_calls(logs: List[Dict[str, Any]], threshold_ms: float = 1000, limit: int = 10):
    """Show slowest tool calls."""
    if not logs:
        print("No tool calls recorded yet.")
        return

    # Sort by duration
    sorted_logs = sorted(logs, key=lambda x: x.get("duration_ms", 0), reverse=True)
    slow_calls = [log for log in sorted_logs if log.get("duration_ms", 0) >= threshold_ms][:limit]

    if not slow_calls:
        print(f"No calls slower than {format_duration(threshold_ms)} found.")
        return

    print(f"\n{'='*70}")
    print(f"Slowest Tool Calls (>{format_duration(threshold_ms)}, showing {len(slow_calls)})")
    print(f"{'='*70}\n")

    print(f"{'Tool Name':<20} {'Duration':>12} {'Timestamp'}")
    print(f"{'-'*70}")

    for log in slow_calls:
        tool = log.get("tool_name", "unknown")
        duration = log.get("duration_ms", 0)
        timestamp = log.get("timestamp", "N/A")

        print(f"{tool:<20} {format_duration(duration):>12} {timestamp}")

    print(f"\n{'='*70}\n")


def filter_by_project(logs: List[Dict[str, Any]], project_path: str):
    """Filter logs by project/working directory."""
    filtered = [log for log in logs if project_path in log.get("cwd", "")]

    if not filtered:
        print(f"No calls found for project path containing: {project_path}")
        return

    print(f"\n{'='*70}")
    print(f"Tool Calls in Project: {project_path} ({len(filtered)} calls)")
    print(f"{'='*70}\n")

    # Group by working directory
    by_cwd = defaultdict(list)
    for log in filtered:
        cwd = log.get("cwd", "unknown")
        by_cwd[cwd].append(log)

    for cwd, cwd_logs in sorted(by_cwd.items()):
        print(f"\nWorking Directory: {cwd}")
        print(f"{'-'*70}")

        for i, log in enumerate(cwd_logs, 1):
            timestamp = log.get("timestamp", "N/A")
            tool = log.get("tool_name", "unknown")
            duration = log.get("duration_ms", 0)

            print(f"  {i}. [{timestamp}] {tool} - {format_duration(duration)}")

    # Show statistics
    durations = [log.get("duration_ms", 0) for log in filtered]
    avg_duration = sum(durations) / len(durations) if durations else 0

    print(f"\n{'='*70}")
    print(f"Statistics:")
    print(f"  Total Calls: {len(filtered)}")
    print(f"  Avg Time:    {format_duration(avg_duration)}")
    print(f"  Directories: {len(by_cwd)}")

    print(f"\n{'='*70}\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: query_logs.py <command> [options]")
        print("\nCommands:")
        print("  summary              Show summary statistics")
        print("  recent [N]           Show recent N tool calls (default: 10)")
        print("  detail [index]       Show detailed info for a call (default: -1, last)")
        print("  filter <tool_name>   Filter calls by tool name")
        print("  project <path>       Filter calls by project/working directory")
        print("  slow [threshold_ms]  Show slow calls (default: >1000ms)")
        print("\nExamples:")
        print("  query_logs.py summary")
        print("  query_logs.py recent 20")
        print("  query_logs.py detail -2")
        print("  query_logs.py filter Bash")
        print("  query_logs.py project /root/ai/skills")
        print("  query_logs.py slow 500")
        sys.exit(1)

    command = sys.argv[1].lower()
    logs = load_logs()

    if command == "summary":
        show_summary(logs)
    elif command == "recent":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        show_recent(logs, limit)
    elif command == "detail":
        index = int(sys.argv[2]) if len(sys.argv) > 2 else -1
        show_detail(logs, index)
    elif command == "filter":
        if len(sys.argv) < 3:
            print("Error: filter command requires a tool name")
            sys.exit(1)
        filter_by_tool(logs, sys.argv[2])
    elif command == "project":
        if len(sys.argv) < 3:
            print("Error: project command requires a path")
            sys.exit(1)
        filter_by_project(logs, sys.argv[2])
    elif command == "slow":
        threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 1000
        show_slow_calls(logs, threshold)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
