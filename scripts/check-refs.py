"""Checks numbered references: AGENTS.md rules, lessons, and the docs cited by number.

Fails when a list isn't numbered 1, 2, 3 and so on (lessons keep their numbers, so only
need them unique), when a reference names a number the list doesn't have, and, given a base Git
ref, when a line the change didn't touch names an item that has since moved or gone: a rule added
in the middle shifts every number after it. The base is compared from where the branch left it,
so what main changed since doesn't count as a move.
Usage: python scripts/check-refs.py [base-ref]   (CI and the push hook pass the base)
"""

import difflib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NUMS = r"(\d+(?:\s*(?:,|and|to|–|-)\s*\d+)*)"
NUMBERED = r"^(\d+)\. (.*)"
# Bare "(13)" means a rule only inside AGENTS.md; elsewhere it's anything.
BARE = r"\((\d+(?:–\d+)?)(?: on)?\)"


def doc(name: str, *, md: bool = False) -> str:
    """How a doc is cited: "standards 10", "`docs/standards.md` (5–7)" or
    "[docs/intent.md](docs/intent.md) 3". With md, only with its ".md", since a bare name
    is as likely to mean something else."""
    ext = r"\.md" if md else r"(?:\.md)?"
    return rf"\b{name}{ext}`?\)? \(?{NUMS}"


def skill(name: str) -> str:
    """How a skill's step is cited: "the `deploy` skill 2", or "[`deploy`](...) skill 2"."""
    return rf"\b{name}`?(?:\]\([^)]*\))? skill {NUMS}"


# Each list: its files, how an item starts, whether it runs 1, 2, 3, and how other files cite it.
LISTS: dict[str, tuple[list[str], str, bool, list[str]]] = {
    "AGENTS.md rule": (["AGENTS.md"], NUMBERED, True, [rf"\b[Rr]ules? {NUMS}", BARE]),
    "lesson": (
        ["docs/lessons.md", "docs/aws/lessons.md"],
        NUMBERED,
        False,
        [rf"\b[Ll]essons? {NUMS}"],
    ),
    "spec": (["docs/spec.md"], NUMBERED, True, [rf"\bspec {NUMS}"]),
    "standards": (["docs/standards.md"], NUMBERED, True, [doc("standards")]),
    "pull-request skill": (
        [".claude/skills/pull-request/SKILL.md"],
        NUMBERED,
        True,
        [skill("pull-request")],
    ),
    "deploy skill": ([".claude/skills/deploy/SKILL.md"], NUMBERED, True, [skill("deploy")]),
    "trade-offs": (
        ["guides/03-security-trade-offs.md"],
        r"^\| (\d+) \| ([^|]*)",
        True,
        [rf"\btrade-offs {NUMS}"],
    ),
}
SCANNED = {
    *(".md", ".sh", ".yml", ".yaml", ".py", ".hcl", ".toml", ".tf", ".json"),
    *(".ts", ".tsx", ".js", ".html", ".css"),
}


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, encoding="utf-8", check=True
    ).stdout


def items(text: str, pattern: str) -> list[tuple[int, str]]:
    return [(int(m[1]), m[2].strip()) for m in re.finditer(pattern, text, re.MULTILINE)]


def expand(nums: str) -> list[int]:
    """'8 to 10', '17–18' and '8-10' are ranges; ',' and 'and' are lists."""
    out: list[int] = []
    for part in re.split(r"\s*(?:,|and)\s*", nums):
        bounds = [int(n) for n in re.split(r"\s*(?:to|–|-)\s*", part) if n]
        out += list(range(bounds[0], bounds[-1] + 1))
    return out


def references(path: str, text: str, patterns: list[str]) -> list[tuple[int, int, str]]:
    """(line, number, the text cited) for each reference in a file."""
    found: list[tuple[int, int, str]] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for pattern in patterns:
            if pattern == BARE and path != "AGENTS.md":
                continue
            for m in re.finditer(pattern, line):
                found += [(lineno, n, m[0]) for n in expand(m[1])]
    return found


def moves(old: list[tuple[int, str]], new: list[tuple[int, str]]) -> dict[int, int | None]:
    """Old number to new, for the items whose number changed; None for one removed.

    Items are matched by their opening words, so an item edited in place keeps its number."""
    a = [text[:50] for _, text in old]
    b = [text[:50] for _, text in new]
    moved: dict[int, int | None] = {}
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "insert":
            continue
        for k in range(i2 - i1):
            to = (
                new[j1 + k][0]
                if tag == "equal" or (tag == "replace" and i2 - i1 == j2 - j1)
                else None
            )
            if to != old[i1 + k][0]:
                moved[old[i1 + k][0]] = to
    return moved


def changed_lines(base: str, path: str, tracked: set[str]) -> set[int] | None:
    """Line numbers in the working copy of a file that differ from the base; None for a new file."""
    if path not in tracked:
        return None
    lines: set[int] = set()
    for m in re.finditer(
        r"^@@ -\S+ \+(\d+)(?:,(\d+))? @@", git("diff", "-U0", base, "--", path), re.M
    ):
        lines.update(range(int(m[1]), int(m[1]) + int(m[2] or 1)))
    return lines


def at(base: str | None, path: str) -> str:
    """A file as it was at the base; empty without a base or if it didn't exist there."""
    if not base:
        return ""
    return subprocess.run(
        ["git", "show", f"{base}:{path}"],
        cwd=ROOT,
        capture_output=True,
        encoding="utf-8",
        check=False,
    ).stdout


def numbering(sources: list[str], numbers: list[int], in_order: bool) -> list[str]:
    where = " and ".join(sources)
    if in_order and numbers != list(range(1, len(numbers) + 1)):
        return [f"{where}: numbered {numbers}, not 1 to {len(numbers)} in order"]
    repeated = sorted({n for n in numbers if numbers.count(n) > 1})
    return [f"{where}: {n} is used more than once" for n in repeated]


def main(base: str | None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]  # Windows consoles
    errors: list[str] = []
    if base:
        base = git("merge-base", base, "HEAD").strip()
    tracked = set(git("ls-files").splitlines())
    listed = git("ls-files", "--cached", "--others", "--exclude-standard").splitlines()
    # The tests cite made-up numbers on purpose.
    files = [
        f
        for f in listed
        if Path(f).suffix in SCANNED and not f.startswith("scripts/tests/") and (ROOT / f).exists()
    ]
    texts = {f: (ROOT / f).read_text(encoding="utf-8") for f in files}
    for name, (sources, item_pattern, in_order, patterns) in LISTS.items():
        new = [item for source in sources for item in items(texts[source], item_pattern)]
        numbers = [n for n, _ in new]
        errors += numbering(sources, numbers, in_order)
        old = [item for source in sources for item in items(at(base, source), item_pattern)]
        moved = moves(old, new) if base and old else {}
        for path, text in texts.items():
            refs = references(path, text, patterns)
            touched: set[int] | None = set()
            if base and moved and refs:
                touched = changed_lines(base, path, tracked)
            for lineno, n, cited in refs:
                where = f"{path}:{lineno}: '{cited}'"
                if n not in numbers:
                    errors.append(f"{where}: {name} {n} doesn't exist")
                elif n in moved and touched is not None and lineno not in touched:
                    to = moved[n]
                    now = f"is now {to}" if to else "was removed"
                    errors.append(f"{where}: {name} {n} {now}; check what this line means")
    for error in errors:
        print(error)
    print(f"Numbered references: {len(errors)} problem(s)" if errors else "Numbered references: ok")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
