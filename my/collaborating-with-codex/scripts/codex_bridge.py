"""
Codex Bridge Script for Claude Agent Skills.
Wraps the Codex CLI to provide a JSON-based interface for Claude.
"""
from __future__ import annotations

import json
import re
import os
import sys
import queue
import subprocess
import threading
import time
import argparse
from typing import Generator, List, Optional


def run_shell_command(cmd: List[str], timeout: Optional[int] = None) -> Generator[str, None, None]:
    """Execute a command and stream its output line-by-line with optional timeout."""
    process = subprocess.Popen(
        cmd,
        shell=False,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        encoding='utf-8',
        errors='replace',
    )

    output_queue: queue.Queue[Optional[str]] = queue.Queue()
    GRACEFUL_SHUTDOWN_DELAY = 0.3
    start_time = time.time()
    timed_out = False

    def is_turn_completed(line: str) -> bool:
        try:
            data = json.loads(line)
            return data.get("type") == "turn.completed"
        except (json.JSONDecodeError, AttributeError, TypeError):
            return False

    def read_output() -> None:
        if process.stdout:
            for line in iter(process.stdout.readline, ""):
                stripped = line.strip()
                output_queue.put(stripped)
                if is_turn_completed(stripped):
                    time.sleep(GRACEFUL_SHUTDOWN_DELAY)
                    process.terminate()
                    break
            process.stdout.close()
        output_queue.put(None)

    thread = threading.Thread(target=read_output)
    thread.start()

    while True:
        # Check timeout
        if timeout and (time.time() - start_time) > timeout:
            timed_out = True
            try:
                process.terminate()
                time.sleep(2)
                if process.poll() is None:
                    process.kill()
            except:
                pass
            break

        try:
            line = output_queue.get(timeout=0.5)
            if line is None:
                break
            yield line
        except queue.Empty:
            if process.poll() is not None and not thread.is_alive():
                break

    if timed_out:
        yield json.dumps({
            "type": "timeout",
            "error": {"message": f"Codex execution exceeded {timeout}s timeout limit"}
        })

    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
    thread.join(timeout=5)

    while not output_queue.empty():
        try:
            line = output_queue.get_nowait()
            if line is not None:
                yield line
        except queue.Empty:
            break


def main():
    parser = argparse.ArgumentParser(description="Codex Bridge")
    parser.add_argument("--PROMPT", required=True, help="Instruction for the task to send to codex.")
    parser.add_argument("--cd", required=True, help="Set the workspace root for codex before executing the task.")
    parser.add_argument("--sandbox", default="read-only", choices=["read-only", "workspace-write", "danger-full-access"], help="Sandbox policy for model-generated commands. Defaults to `read-only`.")
    parser.add_argument("--SESSION_ID", default="", help="Resume the specified session of the codex. Defaults to `None`, start a new session.")
    parser.add_argument("--skip-git-repo-check", action="store_true", default=True, help="Allow codex running outside a Git repository (useful for one-off directories).")
    parser.add_argument("--return-all-messages", action="store_true", help="Return all messages (e.g. reasoning, tool calls, etc.) from the codex session. Set to `False` by default, only the agent's final reply message is returned.")
    parser.add_argument("--image", action="append", default=[], help="Attach one or more image files to the initial prompt. Separate multiple paths with commas or repeat the flag.")
    parser.add_argument("--model", default="", help="The model to use for the codex session. This parameter is strictly prohibited unless explicitly specified by the user.")
    parser.add_argument("--yolo", action="store_true", help="Run every command without approvals or sandboxing. Only use when `sandbox` couldn't be applied.")
    parser.add_argument("--profile", default="", help="Configuration profile name to load from `~/.codex/config.toml`. This parameter is strictly prohibited unless explicitly specified by the user.")
    parser.add_argument("--timeout", type=int, default=600, help="Maximum execution time in seconds (default: 600s/10min). Set to 0 for no timeout.")
    parser.add_argument(
        "--no-progress",
        action="store_true",
        default=False,
        help="Disable real-time progress output to terminal. Use in CI/CD environments."
    )

    args = parser.parse_args()

    _tty = None
    if not args.no_progress:
        try:
            _tty = open("/dev/tty", "w", buffering=1)  # line-buffered
        except (OSError, FileNotFoundError):
            _tty = None  # CI/CD or no controlling terminal: silent fallback

    def progress(msg: str) -> None:
        if _tty is None:
            return
        try:
            _tty.write(msg + "\n")
            _tty.flush()
        except OSError:
            pass  # terminal closed: silently ignore

    # ANSI escape codes
    BOLD = "\033[1m"
    DIM = "\033[2m"
    CYAN = "\033[36m"
    YELLOW = "\033[33m"
    GREEN = "\033[32m"
    RED = "\033[31m"
    RESET = "\033[0m"

    def strip_md(text: str) -> str:
        """Convert common markdown to ANSI terminal styles."""
        # **bold** or __bold__ → ANSI bold
        text = re.sub(r'\*\*(.+?)\*\*', rf'{BOLD}\1{RESET}', text)
        text = re.sub(r'__(.+?)__', rf'{BOLD}\1{RESET}', text)
        # *italic* or _italic_ (but not inside words like file_name)
        text = re.sub(r'(?<!\w)\*(.+?)\*(?!\w)', rf'{DIM}\1{RESET}', text)
        # `code` → cyan
        text = re.sub(r'`(.+?)`', rf'{CYAN}\1{RESET}', text)
        # ### headings → bold (strip leading #s)
        text = re.sub(r'^#{1,6}\s+', BOLD, text)
        return text

    def fmt_args(raw: str) -> str:
        try:
            parsed = json.loads(raw)
            parts = [f'{k}={str(v).replace(chr(10), " ")!r}' for k, v in parsed.items()]
            result = ", ".join(parts)
        except (json.JSONDecodeError, AttributeError):
            result = str(raw).replace("\n", " ")
        return result

    def fmt_snippet(text: str) -> str:
        """Collapse text to a single line and convert markdown to ANSI."""
        return strip_md(" ".join(text.split()))

    cmd = ["codex", "exec", "--sandbox", args.sandbox, "--cd", args.cd, "--json"]

    if args.image:
        cmd.extend(["--image", ",".join(args.image)])

    if args.model:
        cmd.extend(["--model", args.model])

    if args.profile:
        cmd.extend(["--profile", args.profile])

    if args.yolo:
        cmd.append("--yolo")

    if args.skip_git_repo_check:
        cmd.append("--skip-git-repo-check")

    if args.SESSION_ID:
        cmd.extend(["resume", args.SESSION_ID])

    cmd += ['--', args.PROMPT]

    # Execution Logic
    all_messages = []
    agent_messages = ""
    success = True
    err_message = ""
    thread_id = None
    timeout_val = None if args.timeout == 0 else args.timeout
    _session_shown = False
    _start_time = time.time()

    def elapsed() -> str:
        return f"{int(time.time() - _start_time)}s"

    for line in run_shell_command(cmd, timeout=timeout_val):
        try:
            line_dict = json.loads(line.strip())
            all_messages.append(line_dict)

            # Handle timeout
            if line_dict.get("type") == "timeout":
                progress(f"{DIM}[codex]{RESET} {RED}Timed out after {args.timeout}s{RESET}")
                success = False
                err_message = f"[TIMEOUT] Execution exceeded {args.timeout}s limit. "
                err_message += "Try increasing timeout with --timeout 1200 (20 minutes)."
                if agent_messages:
                    err_message += f"\n\nPartial results: {agent_messages[:200]}"
                break

            item = line_dict.get("item", {})
            item_type = item.get("type", "")
            if item_type == "agent_message":
                text = item.get("text", "")
                agent_messages = agent_messages + text
                if text:
                    progress(f"{DIM}[codex]{RESET} {BOLD}Responding:{RESET} {fmt_snippet(text)}")
                else:
                    progress(f"{DIM}[codex]{RESET} {BOLD}Responding...{RESET}")
            elif item_type == "function_call":
                name = item.get("name", "?")
                raw_args = item.get("arguments", "{}")
                progress(f"{DIM}[codex]{RESET} {GREEN}>>{RESET} {name}({fmt_args(raw_args)})")
            elif item_type == "function_call_output":
                output = item.get("output", "") or item.get("content", "") or item.get("result", "")
                if output:
                    progress(f"{DIM}[codex]{RESET} {YELLOW}<<{RESET} {fmt_snippet(str(output))}")
                else:
                    progress(f"{DIM}[codex]{RESET} {YELLOW}<<{RESET} {DIM}(no output){RESET}")
            elif item_type == "command_execution":
                cmd_str = item.get("command", "")
                agg_output = item.get("aggregated_output", "")
                if agg_output:
                    # completed: show output
                    exit_code = item.get("exit_code", "")
                    if exit_code and str(exit_code) != "0":
                        prefix = f"{RED}<< (exit={exit_code}){RESET} "
                    else:
                        prefix = f"{YELLOW}<<{RESET} "
                    progress(f"{DIM}[codex]{RESET} {prefix}{fmt_snippet(str(agg_output))}")
                elif cmd_str:
                    # started: show command
                    progress(f"{DIM}[codex]{RESET} {GREEN}>>{RESET} shell({fmt_snippet(str(cmd_str))})")
            elif item_type == "reasoning":
                text = item.get("text", "") or item.get("content", "")
                if text:
                    progress(f"{DIM}[codex]{RESET} {DIM}Thinking:{RESET} {fmt_snippet(text)}")
                else:
                    progress(f"{DIM}[codex]{RESET} {DIM}Thinking...{RESET}")
            else:
                # catch-all: print any unrecognized item type
                if item_type:
                    snippet = item.get("text", "") or item.get("content", "") or item.get("output", "")
                    if snippet:
                        progress(f"{DIM}[codex]{RESET} {DIM}[{item_type}]{RESET} {fmt_snippet(str(snippet))}")
                    else:
                        # dump item keys to help debug unknown item structures
                        keys = [k for k in item.keys() if k != "type"]
                        progress(f"{DIM}[codex]{RESET} {DIM}[{item_type}] keys={keys}{RESET}")
            if line_dict.get("thread_id") is not None:
                thread_id = line_dict.get("thread_id")
                if not _session_shown:
                    progress(f"{DIM}[codex]{RESET} Session: {CYAN}{thread_id[:8]}...{RESET}")
                    _session_shown = True
            top_type = line_dict.get("type", "")
            if top_type == "turn.completed":
                progress(f"{DIM}[codex]{RESET} {GREEN}Done.{RESET} ({elapsed()})")
            elif "fail" in top_type:
                success = False if len(agent_messages) == 0 else success
                fail_msg = line_dict.get("error", {}).get("message", "")
                progress(f"{DIM}[codex]{RESET} {RED}Error:{RESET} {fail_msg[:60]}")
                err_message += "\n\n[codex error] " + fail_msg
            elif "error" in top_type:
                error_msg = line_dict.get("message", "")
                is_reconnecting = bool(re.match(r'^Reconnecting\.\.\.\s+\d+/\d+$', error_msg))

                if not is_reconnecting:
                    success = False if len(agent_messages) == 0 else success
                    progress(f"{DIM}[codex]{RESET} {RED}Error:{RESET} {error_msg[:60]}")
                    err_message += "\n\n[codex error] " + error_msg
            elif top_type and top_type not in ("item.created", "item.updated", "item.completed",
                                                "item.started",
                                                "response.created", "response.completed",
                                                "thread.started", "turn.started"):
                # catch-all: print unrecognized top-level type for debugging
                progress(f"[codex] [{top_type}]")

        except json.JSONDecodeError:
            err_message += "\n\n[json decode error] " + line
            continue

        except Exception as error:
            err_message += "\n\n[unexpected error] " + f"Unexpected error: {error}. Line: {line!r}"
            success = False
            break

    if thread_id is None and success:
        success = False
        err_message = "Failed to get `SESSION_ID` from the codex session. \n\n" + err_message

    if len(agent_messages) == 0 and success:
        success = False
        err_message = "Failed to get `agent_messages` from the codex session. \n\n You can try to set `return_all_messages` to `True` to get the full reasoning information. " + err_message

    if success:
        result = {
            "success": True,
            "SESSION_ID": thread_id,
            "agent_messages": agent_messages,
        }

    else:
        result = {"success": False, "error": err_message}
        # Include partial SESSION_ID even on failure for potential resume
        if thread_id:
            result["SESSION_ID"] = thread_id

    if args.return_all_messages:
        result["all_messages"] = all_messages

    print(json.dumps(result, indent=2, ensure_ascii=False))

    if _tty is not None:
        try:
            _tty.close()
        except OSError:
            pass

if __name__ == "__main__":
    main()
