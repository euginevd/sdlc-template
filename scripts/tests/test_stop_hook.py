"""Tests for the Stop hook, agent-stop-check.sh, in a throwaway repo with a stand-in check.sh."""

import shutil
import subprocess
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
