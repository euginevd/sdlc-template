"""Checks the Claude Code hooks in .claude/settings.json still work: a broken hook fails silently.

Each hook must be on a known event, have a timeout, and run a script that exists and parses;
the guard must still deny a production `.env` edit (#192).
Usage: python3 scripts/check-hooks.py; exits 1 on a problem.
"""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVENTS = {"PreToolUse", "PostToolUse", "Stop", "SubagentStop", "SessionStart", "UserPromptSubmit"}
SCRIPT = re.compile(r"\$CLAUDE_PROJECT_DIR/([\w./-]+\.sh)")
BASH = shutil.which("bash")


def hook_problems(event: str, hook: dict[str, object]) -> list[str]:
    """What's wrong with one hook."""
    command = str(hook.get("command", ""))
    found: list[str] = []
    if event not in EVENTS:
        found.append(f"{event}: not a hook event this check knows; add it here if it's real")
    if hook.get("type") != "command" or not hook.get("timeout"):
        found.append(f"{event}: each hook is a command with a timeout: {command}")
    scripts = SCRIPT.findall(command)
    if not scripts:
        found.append(f"{event}: runs no script under $CLAUDE_PROJECT_DIR: {command}")
    for script in scripts:
        if not (ROOT / script).is_file():
            found.append(f"{event}: {script} doesn't exist")
        elif BASH and subprocess.run([BASH, "-n", str(ROOT / script)], check=False).returncode:
            found.append(f"{event}: {script} doesn't parse")
    return found


def guard_still_denies() -> list[str]:
    """The guard, run as the hook runs it, still denies a production `.env` edit."""
    spec = (ROOT / "docs" / "spec.md").read_text(encoding="utf-8")
    if not BASH or re.search(r"^Profile: .prototype.", spec, re.MULTILINE):
        return []
    payload = {"tool_name": "Edit", "tool_input": {"file_path": str(ROOT / ".env")}}
    out = subprocess.run(
        [BASH, str(ROOT / "scripts" / "agent-guard.sh")],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        check=False,
    ).stdout
    if '"permissionDecision":"deny"' not in out:
        return ["agent-guard.sh no longer denies a production .env edit"]
    return []


def problems() -> list[str]:
    """Everything wrong with the hooks, one line each."""
    try:
        settings = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f".claude/settings.json doesn't load: {error}"]
    found = [
        line
        for event, groups in settings.get("hooks", {}).items()
        for group in groups
        for hook in group.get("hooks", [])
        for line in hook_problems(event, hook)
    ]
    return found or guard_still_denies()


if __name__ == "__main__":
    found = problems()
    for line in found:
        print(f"::error file=.claude/settings.json::{line}")
    print("Agent hooks: ok" if not found else f"Agent hooks: {len(found)} problem(s)")
    sys.exit(1 if found else 0)
