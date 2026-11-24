"""Tests for check-hooks.py, which keeps a broken agent hook from failing silently (#192)."""

import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "check_hooks", Path(__file__).resolve().parent.parent / "check-hooks.py"
)
assert spec
assert spec.loader
check_hooks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_hooks)


def test_the_repos_hooks_pass():
    assert check_hooks.problems() == []


def test_a_missing_script_is_a_problem():
    command = 'bash "$CLAUDE_PROJECT_DIR/scripts/gone.sh"'
    hook = {"type": "command", "command": command, "timeout": 5}
    assert check_hooks.hook_problems("Stop", hook) == ["Stop: scripts/gone.sh doesn't exist"]


def test_a_hook_without_a_timeout_or_script_is_a_problem():
    found = check_hooks.hook_problems("Stopp", {"type": "command", "command": "echo hi"})
    assert len(found) == 3
