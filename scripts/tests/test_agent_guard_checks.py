"""Tests for the guard's last rule: editing a check's own settings asks a person first (#180)."""

import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    "guard_tests", Path(__file__).with_name("test_agent_guard.py")
)
assert spec
assert spec.loader
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)
pytestmark = guard.pytestmark


@pytest.mark.parametrize(
    "config",
    [
        "pyproject.toml",
        "apps/web/eslint.config.js",
        "apps/web/.prettierrc",
        "apps/web/tsconfig.json",
        "apps/web/.npmrc",
        "infra/aws/.tflint.hcl",
        "lefthook.yml",
        ".lefthook/pre-push-scan.sh",
        ".gitleaks.toml",
        ".github/workflows/ci.yml",
        ".github/dependabot.yml",
        ".claude/settings.json",
        "scripts/check.sh",
        "scripts/check-refs.py",
        "scripts/agent-stop-check.sh",
    ],
)
def test_editing_a_checks_settings_asks_first(tmp_path: Path, config: str):
    root = guard.repo(tmp_path, "prototype")
    (root / config).parent.mkdir(parents=True, exist_ok=True)
    (root / config).write_text("x\n", encoding="utf-8")
    assert guard.decision(root, "Edit", file_path=config) == "ask"


def test_a_new_config_file_needs_no_question(tmp_path: Path):
    root = guard.repo(tmp_path, "production")
    assert guard.decision(root, "Write", file_path="apps/web/eslint.config.js") == "allow"
