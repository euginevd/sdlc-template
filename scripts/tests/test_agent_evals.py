"""Tests for agent-evals.py's judging and its cases; the model calls run only in CI (#207)."""

import importlib.util
import json
import re
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "agent_evals", Path(__file__).resolve().parent.parent / "agent-evals.py"
)
assert spec
assert spec.loader
evals = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evals)


def test_an_answer_that_follows_the_rules_passes():
    assert evals.judge("I won't skip the hook.", ["won't"], ["--no-verify"]) == []


def test_a_missing_or_rejected_pattern_fails():
    reasons = evals.judge("Pushing with --no-verify now.", ["won't"], ["--no-verify"])
    assert reasons == ["missing /won't/", "has /--no-verify/"]


def test_every_case_is_complete_and_its_patterns_compile():
    cases = json.loads(evals.CASES.read_text(encoding="utf-8"))["cases"]
    assert cases
    for case in cases:
        assert case["name"]
        assert case["prompt"]
        assert case["expect"]
        for pattern in case["expect"] + case["reject"]:
            re.compile(pattern)
