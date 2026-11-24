"""Tests for the guard's MCP rule: no agent calls an MCP server named for prod (#208)."""

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
    ("tool", "want"),
    [
        ("mcp__db-prod__query", "deny"),
        ("mcp__PROD_db__query", "deny"),
        ("mcp__aws-production__describe", "deny"),
        ("mcp__my_prod_db__query", "deny"),
        ("mcp__db-dev__query", "allow"),
        ("mcp__playwright__browser_click", "allow"),
        ("mcp__db-dev__products", "allow"),
    ],
)
@pytest.mark.parametrize("profile", ["prototype", "production"])
def test_no_agent_calls_a_prod_mcp_server(tmp_path: Path, profile: str, tool: str, want: str):
    assert guard.decision(guard.repo(tmp_path, profile), tool) == want
