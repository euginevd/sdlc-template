"""Tests for the Stop hook, agent-stop-check.sh, in a throwaway repo with a stand-in check.sh."""

import os
import shutil
import subprocess
import time
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parent.parent / "agent-stop-check.sh"
BASH = shutil.which("bash")
# CI's python job runs in uv's slim image, which has no git; a developer's machine has both.
pytestmark = pytest.mark.skipif(
    BASH is None or shutil.which("git") is None, reason="needs bash and git"
)


def repo(tmp_path: Path, check_exit: int) -> Path:
    """A git repo with the hook, and a check.sh that prints a finding and exits check_exit."""
    (tmp_path / "scripts").mkdir()
    shutil.copy(HOOK, tmp_path / "scripts" / "agent-stop-check.sh")
    (tmp_path / "scripts" / "check.sh").write_text(
        f"echo 'F401 unused import'\nexit {check_exit}\n", encoding="utf-8", newline="\n"
    )
    identity = ["-c", "user.name=t", "-c", "user.email=t@t"]
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(["git", *identity, "commit", "-qm", "start"], cwd=tmp_path, check=True)
    return tmp_path


def run(root: Path, payload: str) -> subprocess.CompletedProcess[str]:
    assert BASH
    return subprocess.run(
        [BASH, str(root / "scripts" / "agent-stop-check.sh")],
        input=payload,
        capture_output=True,
        text=True,
        check=False,
    )


def test_a_failing_check_blocks_and_reports_it(tmp_path: Path):
    root = repo(tmp_path, check_exit=1)
    (root / "edited.py").write_text("x = 1\n", encoding="utf-8")
    result = run(root, '{"stop_hook_active": false}')
    assert result.returncode == 2
    assert "F401 unused import" in result.stderr


def test_passing_checks_let_the_agent_stop(tmp_path: Path):
    root = repo(tmp_path, check_exit=0)
    (root / "edited.py").write_text("x = 1\n", encoding="utf-8")
    assert run(root, '{"stop_hook_active": false}').returncode == 0


def test_it_blocks_only_once(tmp_path: Path):
    root = repo(tmp_path, check_exit=1)
    (root / "edited.py").write_text("x = 1\n", encoding="utf-8")
    assert run(root, '{"stop_hook_active": true}').returncode == 0


def test_no_edits_means_nothing_to_check(tmp_path: Path):
    root = repo(tmp_path, check_exit=1)
    assert run(root, '{"stop_hook_active": false}').returncode == 0


def autopilot(root: Path, open_issues: int, *, minutes: int = 60, profile: str = "prototype"):
    """Turns the autopilot on, with a stand-in gh that reports open_issues open issues."""
    (root / "docs").mkdir(exist_ok=True)
    (root / "docs" / "spec.md").write_text(f"Profile: `{profile}`.\n", encoding="utf-8")
    (root / ".claude").mkdir(exist_ok=True)
    bin_dir = root / "bin"
    bin_dir.mkdir()
    (bin_dir / "gh").write_text(f"#!/usr/bin/env bash\necho {open_issues}\n", newline="\n")
    (bin_dir / "gh").chmod(0o755)
    # Committed, so only the hook's own state counts as a change.
    subprocess.run(["git", "add", "docs"], cwd=root, check=True)
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "spec"],
        cwd=root,
        check=True,
    )
    (root / ".git" / "info" / "exclude").write_text(".claude/\nbin/\n")
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True, check=True
    ).stdout.strip()
    until = int(time.time()) + minutes * 60
    (root / ".claude" / "autopilot").write_text(f"until={until}\nidle=0\nhead={head}\n")


def run_on_path(root: Path, payload: str) -> subprocess.CompletedProcess[str]:
    assert BASH
    env = {**os.environ, "PATH": f"{root / 'bin'}{os.pathsep}{os.environ['PATH']}"}
    return subprocess.run(
        [BASH, str(root / "scripts" / "agent-stop-check.sh")],
        input=payload,
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )


def test_autopilot_sends_the_agent_back_while_issues_are_open(tmp_path: Path):
    root = repo(tmp_path, check_exit=0)
    autopilot(root, open_issues=3)
    result = run_on_path(root, '{"stop_hook_active": true}')
    assert result.returncode == 2
    assert "3 open issue(s)" in result.stderr


def test_autopilot_ends_when_the_backlog_is_empty(tmp_path: Path):
    root = repo(tmp_path, check_exit=0)
    autopilot(root, open_issues=0)
    assert run_on_path(root, '{"stop_hook_active": true}').returncode == 0
    assert not (root / ".claude" / "autopilot").exists()


def test_autopilot_ends_when_time_is_up(tmp_path: Path):
    root = repo(tmp_path, check_exit=0)
    autopilot(root, open_issues=3, minutes=-1)
    assert run_on_path(root, '{"stop_hook_active": true}').returncode == 0


def test_autopilot_never_runs_in_production(tmp_path: Path):
    root = repo(tmp_path, check_exit=0)
    autopilot(root, open_issues=3, profile="production")
    assert run_on_path(root, '{"stop_hook_active": true}').returncode == 0


def test_autopilot_gives_up_after_two_idle_turns(tmp_path: Path):
    root = repo(tmp_path, check_exit=0)
    autopilot(root, open_issues=3)
    assert run_on_path(root, '{"stop_hook_active": true}').returncode == 2
    result = run_on_path(root, '{"stop_hook_active": true}')
    assert result.returncode == 0
    assert "changed nothing" in result.stderr


def test_autopilot_keeps_going_while_work_lands(tmp_path: Path):
    root = repo(tmp_path, check_exit=0)
    autopilot(root, open_issues=3)
    for n in range(3):
        (root / f"feature{n}.py").write_text("x = 1\n", encoding="utf-8")
        subprocess.run(["git", "add", "-A"], cwd=root, check=True)
        subprocess.run(
            ["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", f"f{n}"],
            cwd=root,
            check=True,
        )
        assert run_on_path(root, '{"stop_hook_active": true}').returncode == 2
