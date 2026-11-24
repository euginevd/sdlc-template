"""Fails on AI attribution in a commit message or PR description (AGENTS.md rule 15).

Catches an AI co-author trailer and a "Generated with" footer, which some tools add by themselves.
Usage: python scripts/check-attribution.py FILE...   (the commit-msg hook passes the message file)
"""

import re
import sys
from pathlib import Path

AI = r"(?:claude|anthropic|copilot|chatgpt|openai|codex|gemini|cursor|devin|aider|\bai\b)"
# Each only at the start of a line, where a trailer or footer sits, so a sentence quoting the rule
# passes. Spaces, markdown quote and list marks before it don't count.
LEAD = r"^[\s>*_-]*"
PATTERNS = [
    re.compile(rf"{LEAD}co-authored-by:.*{AI}", re.IGNORECASE),
    re.compile(rf"{LEAD}(?:🤖\s*)?generated (?:with|by)\b.*{AI}", re.IGNORECASE),
    re.compile(rf"{LEAD}🤖"),
]


def problems(text: str) -> list[str]:
    # Git drops lines starting with '#' from a message it opens in an editor.
    lines = [line for line in text.splitlines() if not line.startswith("#")]
    return [line.strip() for line in lines if any(p.search(line) for p in PATTERNS)]


def main(paths: list[str]) -> int:
    found = [
        f"{path}: {line}" for path in paths for line in problems(Path(path).read_text("utf-8"))
    ]
    for line in found:
        print(line)
    if found:
        print("AI attribution found: remove the lines above (AGENTS.md rule 15).")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
