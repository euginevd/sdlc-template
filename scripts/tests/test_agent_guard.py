"""Tests for the PreToolUse guard, agent-guard.sh, in a throwaway repo with each profile."""

import json
import shutil
import subprocess
from pathlib import Path

import pytest

GUARD = Path(__file__).resolve().parent.parent / "agent-guard.sh"
BASH = shutil.which("bash")
pytestmark = pytest.mark.skipif(BASH is None, reason="needs bash")


def repo(tmp_path: Path, profile: str) -> Path:
    """A repo with the guard, a spec naming the profile, and a few existing files."""
    for folder in ("scripts", "docs"):
        (tmp_path / folder).mkdir()
    shutil.copy(GUARD, tmp_path / "scripts" / "agent-guard.sh")
    (tmp_path / "docs" / "spec.md").write_text(f"Profile: `{profile}`\n", encoding="utf-8")
    return tmp_path


def decision(root: Path, tool: str, **tool_input: str) -> str:
    """What the guard decides for one tool call: allow, ask or deny."""
    if "file_path" in tool_input:
        tool_input["file_path"] = str(root / tool_input["file_path"])
    assert BASH
    out = subprocess.run(
        [BASH, str(root / "scripts" / "agent-guard.sh")],
        input=json.dumps({"tool_name": tool, "tool_input": tool_input}),
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return json.loads(out)["hookSpecificOutput"]["permissionDecision"] if out else "allow"


@pytest.mark.parametrize(
    ("tool", "args", "want"),
    [
        ("Edit", {"file_path": ".env"}, "deny"),
        ("Write", {"file_path": "apps/api/.env.local"}, "deny"),
        ("Edit", {"file_path": ".env.example"}, "allow"),
        ("Bash", {"command": "cat .env"}, "deny"),
        ("Bash", {"command": "echo x > apps/api/.env.prod"}, "deny"),
        ("Bash", {"command": "cat .env.example"}, "allow"),
        ("Bash", {"command": 'python -c "import os; print(os.environ)"'}, "allow"),
        ("Bash", {"command": "git status"}, "allow"),
        ("Bash", {"command": 'git commit -m "keep the agent out of .env"'}, "allow"),
        ("Bash", {"command": "gh issue comment 1 --body 'denies .env edits'"}, "allow"),
    ],
)
def test_production_keeps_the_agent_out_of_env(
    tmp_path: Path, tool: str, args: dict[str, str], want: str
):
    assert decision(repo(tmp_path, "production"), tool, **args) == want


def test_a_prototype_may_edit_env(tmp_path: Path):
    root = repo(tmp_path, "prototype")
    assert decision(root, "Edit", file_path=".env") == "allow"
    assert decision(root, "Bash", command="cat .env") == "allow"


@pytest.mark.parametrize(
    "test_file",
    [
        "apps/api/tests/test_handler.py",
        "scripts/tests/test_checks.py",
        "e2e/status.spec.ts",
        "apps/web/src/App.test.tsx",
        "apps/api/handler_test.py",
    ],
)
def test_editing_an_existing_test_asks_first(tmp_path: Path, test_file: str):
    root = repo(tmp_path, "prototype")
    (root / test_file).parent.mkdir(parents=True, exist_ok=True)
    (root / test_file).write_text("x\n", encoding="utf-8")
    assert decision(root, "Edit", file_path=test_file) == "ask"


def test_a_new_test_and_app_code_need_no_question(tmp_path: Path):
    root = repo(tmp_path, "production")
    (root / "apps" / "api").mkdir(parents=True)
    (root / "apps" / "api" / "handler.py").write_text("x\n", encoding="utf-8")
    assert decision(root, "Write", file_path="apps/api/tests/test_new.py") == "allow"
    assert decision(root, "Edit", file_path="apps/api/handler.py") == "allow"


def test_no_profile_yet_counts_as_production(tmp_path: Path):
    assert decision(repo(tmp_path, "*(to fill in)*"), "Edit", file_path=".env") == "deny"
