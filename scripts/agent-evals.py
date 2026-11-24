"""Evals for the agent's own config (#207): does Claude Code still follow AGENTS.md after a change?

Runs each case in .claude/evals/cases.json through `claude -p` in plan mode, which edits
nothing, and checks the answer. Needs the Claude Code CLI and an ANTHROPIC_API_KEY; each run
costs a few API calls. Usage: python3 scripts/agent-evals.py [--model <id>]; exits 1 on a failure.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASES = ROOT / ".claude" / "evals" / "cases.json"


def judge(answer: str, expect: list[str], reject: list[str]) -> list[str]:
    """Why an answer fails its case: each expected pattern missing, each rejected one present."""
    missing = [f"missing /{p}/" for p in expect if not re.search(p, answer, re.IGNORECASE)]
    present = [f"has /{p}/" for p in reject if re.search(p, answer, re.IGNORECASE)]
    return missing + present


def ask(prompt: str, model: str) -> str:
    """The agent's answer to one prompt, in plan mode, from the repo root."""
    out = subprocess.run(
        ["claude", "-p", prompt, "--output-format", "json", "--permission-mode", "plan"]
        + ["--max-turns", "8", "--model", model],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
    )
    try:
        return str(json.loads(out.stdout).get("result", ""))
    except json.JSONDecodeError:
        return out.stdout + out.stderr


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="claude-sonnet-5-5")
    model = parser.parse_args().model
    failed = 0
    for case in json.loads(CASES.read_text(encoding="utf-8"))["cases"]:
        reasons = judge(ask(case["prompt"], model), case["expect"], case["reject"])
        print(f"{'FAIL' if reasons else 'ok  '} {case['name']} {'; '.join(reasons)}")
        failed += bool(reasons)
    print(f"Agent evals: {failed} failed" if failed else "Agent evals: all passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
