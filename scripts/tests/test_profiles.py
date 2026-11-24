"""The two AGENTS.md files: the same rule numbers, and the same floor word for word."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FULL = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
PROTOTYPE = (ROOT / "profiles" / "prototype-AGENTS.md").read_text(encoding="utf-8")


def rules(text: str) -> dict[int, str]:
    """Each rule's first line, without the other wording kept for a project missing a part."""
    return {
        int(m[1]): m[2]
        for m in re.finditer(r"^(\d+)\. (.*)$", text, re.M)
        if "<!-- if:!" not in m[2]
    }


def test_both_number_the_same_rules():
    assert sorted(rules(FULL)) == sorted(rules(PROTOTYPE)) == list(range(1, 19))


def test_the_floor_is_the_same_word_for_word():
    for n in (14, 15, 16, 18):
        assert rules(FULL)[n] == rules(PROTOTYPE)[n], f"rule {n}"
