"""Builds a new project's folder from this template, writing only the files its answers need.

Run by the new-project skill once it has asked the developer about the project. Each file the
template tracks matches one rule in MANIFEST, which says what it's for; a file is written only
when the project needs all of that. A line ending in a marker such as <!-- if:aws --> is kept
only for a project with that part, and the marker itself is dropped. The folder ends up as a
fresh Git repo with everything staged, for the skill to commit and push.
Usage: python scripts/new-project.py <folder> --name <name> --profile prototype|production
           --visibility public|private [--aws] [--ui]
"""

import argparse
import fnmatch
import posixpath
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Each file's first matching pattern says what a project needs before it gets that file:
# "production", "aws", "ui" and "public" are the answers; "template" means no project gets it.
MANIFEST: list[tuple[str, set[str]]] = [
    # The template's own files: making projects, its README and its guides.
    ("README.md", {"template"}),
    ("profiles/*", {"template"}),
    (".claude/skills/new-project/*", {"template"}),
    ("scripts/new-project.py", {"template"}),
    ("scripts/tests/test_new_project.py", {"template"}),
    ("scripts/tests/test_profiles.py", {"template"}),
    ("guides/0[124679]-*", {"template"}),
    ("guides/assets/*", {"template"}),
    # AWS: the infrastructure, its pipeline and its docs.
    ("infra/*", {"aws"}),
    ("docs/aws/*", {"aws"}),
    (".github/workflows/aws.yml", {"aws"}),
    (".github/workflows/images.yml", {"aws"}),
    (".claude/skills/deploy/*", {"aws"}),
    ("scripts/cost-report.py", {"aws"}),
    ("scripts/tests/test_cost_report.py", {"aws"}),
    ("guides/05-aws-cleanup.md", {"aws"}),
    # Screens.
    ("docs/web/*", {"ui"}),
    (".claude/skills/review-design/*", {"ui"}),
    # What only production gates on.
    ("docs/threat-model.md", {"production"}),
    ("docs/checklist.md", {"production"}),
    ("guides/03-security-trade-offs.md", {"production"}),
    ("guides/08-incident-runbook.md", {"production"}),
    ("SECURITY.md", {"production"}),
    ("CONTRIBUTING.md", {"production", "public"}),
    (".github/ISSUE_TEMPLATE/incident.yml", {"production"}),
    (".github/workflows/codeql.yml", {"production"}),
    (".github/workflows/factory.yml", {"production"}),
    (".github/workflows/agent-evals.yml", {"production"}),
    (".claude/evals/*", {"production"}),
    ("scripts/agent-evals.py", {"production"}),
    ("scripts/tests/test_agent_evals.py", {"production"}),
    # Everything else is the core every project gets.
    ("*", set()),
]
# A prototype's AGENTS.md is the shorter one, with the same rule numbers.
RENAMED = {"prototype": {"profiles/prototype-AGENTS.md": "AGENTS.md"}}
TEMPLATE_URL = "https://github.com/euginevd/sdlc-template/blob/main"
MARKER = re.compile(r"\s*<!-- if:(!?)(\w+) -->\s*$")
TEXT = {".md", ".yml", ".yaml", ".json", ".toml", ".sh", ".py", ".html"}


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, encoding="utf-8", check=True
    ).stdout


def needs(path: str) -> set[str]:
    """What a project must have to get this file."""
    return next(tags for pattern, tags in MANIFEST if fnmatch.fnmatch(path, pattern))


def chosen(args: argparse.Namespace) -> set[str]:
    have = {args.profile, args.visibility}
    have |= {"aws"} if args.aws else set()
    return have | ({"ui"} if args.ui else set())


def keep_lines(text: str, have: set[str]) -> str:
    """Drops each line whose marker the project doesn't meet, and the markers on the rest."""
    out: list[str] = []
    for line in text.splitlines(keepends=True):
        m = MARKER.search(line)
        if not m:
            out.append(line)
        elif (m[2] in have) != (m[1] == "!"):
            ending = "\n" if line.endswith("\n") else ""
            out.append(line[: m.start()] + ending)
    return "".join(out)


def files_for(have: set[str]) -> dict[str, str]:
    """Destination path to template path, for every file this project gets."""
    tracked = git(ROOT, "ls-files", "--cached", "--others", "--exclude-standard").splitlines()
    picked: dict[str, str] = {}
    for path in tracked:
        if (ROOT / path).is_file() and needs(path) <= have:
            picked[path] = path
    for src, dest in RENAMED.get(next(iter(have & {"prototype"}), ""), {}).items():
        picked[dest] = src
    return picked


def readme(name: str, profile: str) -> str:
    return f"""# {name}

What it's for and why: [docs/intent.md](docs/intent.md). What gets built:
[docs/spec.md](docs/spec.md), and what's built so far: [docs/features.md](docs/features.md).

Made from [sdlc-template](https://github.com/euginevd/sdlc-template) as a `{profile}`. The agent
works from [AGENTS.md](AGENTS.md). Set up a clone with `bash scripts/setup.sh`, and run the checks
with `bash scripts/check.sh`.
"""


GUIDES = """# Guides

This project's own guides: how to run, use or operate it, written as the project needs them. Each
is a numbered, lowercase file such as `01-running-locally.md`. The template's general guides stay in
[sdlc-template](https://github.com/euginevd/sdlc-template/tree/main/guides).
"""


def relink(text: str, out: str, picked: dict[str, str]) -> str:
    """A link to a template file the project doesn't get now points at it in the template repo."""

    def fix(m: re.Match[str]) -> str:
        target, anchor = m[1], m[2] or ""
        if "://" in target or target.startswith("mailto:"):
            return m[0]
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(out), target))
        if resolved in picked or not (ROOT / resolved).exists():
            return m[0]
        return f"]({TEMPLATE_URL}/{resolved}{anchor})"

    return re.sub(r"\]\(([^)#\s]+)(#[^)\s]*)?\)", fix, text)


def write(dest: Path, picked: dict[str, str], have: set[str], name: str, profile: str) -> None:
    for out, src in picked.items():
        target = dest / out
        target.parent.mkdir(parents=True, exist_ok=True)
        if Path(src).suffix in TEXT:
            text = keep_lines((ROOT / src).read_text(encoding="utf-8"), have)
            if out.endswith(".md"):
                text = relink(text, out, picked)
            target.write_text(text, encoding="utf-8")
        else:
            shutil.copy2(ROOT / src, target)
    (dest / "README.md").write_text(readme(name, profile), encoding="utf-8")
    (dest / "guides").mkdir(exist_ok=True)
    (dest / "guides/README.md").write_text(GUIDES, encoding="utf-8")


def edit(path: Path, pattern: str, replacement: str) -> None:
    text = path.read_text(encoding="utf-8")
    path.write_text(re.sub(pattern, replacement, text, count=1, flags=re.M), encoding="utf-8")


def record(dest: Path, name: str, profile: str, visibility: str) -> None:
    """The answers, in the spec and the project's name."""
    spec = dest / "docs/spec.md"
    repo = "personal" if visibility == "public" else "work"
    edit(spec, r"^Profile: .*$", f"Profile: `{profile}`.")
    edit(spec, r"^Repo: .*$", f"Repo: `{repo}` ({visibility}).")
    edit(spec, r"^Name: .*$", f"Name: `{name}`.")
    edit(dest / "pyproject.toml", r'^name = "starter"$', f'name = "{name}"')
    if profile == "prototype":
        edit(dest / "pyproject.toml", r"^fail_under = 80$", "fail_under = 50")


LINK = re.compile(r"\]\(([^)#\s]+)")
TICKED = re.compile(r"`([\w.-]+/[\w./<>-]*)`")


def stale(dest: Path, left_out: list[str]) -> list[str]:
    """Each Markdown line that links to a missing file or names one the project left out."""
    found: list[str] = []
    for path in sorted(dest.rglob("*.md")):
        if ".git" in path.parts:
            continue
        rel = path.relative_to(dest).as_posix()
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            broken = [
                t
                for t in LINK.findall(line)
                if "://" not in t and not t.startswith("mailto:") and not (path.parent / t).exists()
            ]
            broken += [t for t in TICKED.findall(line) if t in left_out]
            if broken:
                found.append(f"{rel}:{lineno}: {', '.join(dict.fromkeys(broken))}")
    return found


def left_out_paths(picked: dict[str, str]) -> list[str]:
    """Each template file and folder no project file sits in, as the docs name them."""
    tracked = git(ROOT, "ls-files").splitlines()
    kept = set(picked)
    out: set[str] = set()
    for path in tracked:
        if path in kept or path in RENAMED.get("prototype", {}):
            continue
        parts = path.split("/")
        out.add(path)
        for i in range(1, len(parts)):
            folder = "/".join(parts[:i])
            if not any(k.startswith(f"{folder}/") for k in kept):
                out |= {folder, f"{folder}/"}
    return sorted(out)


def parse(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Builds a new project from this template.")
    parser.add_argument("folder", type=Path)
    parser.add_argument("--name", required=True)
    parser.add_argument("--profile", required=True, choices=["prototype", "production"])
    parser.add_argument("--visibility", required=True, choices=["public", "private"])
    parser.add_argument("--aws", action="store_true", help="it deploys to AWS")
    parser.add_argument("--ui", action="store_true", help="it has screens")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]  # Windows consoles
    args = parse(argv)
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", args.name):
        print(f"{args.name}: a repo name here is lowercase letters, digits and hyphens.")
        return 2
    dest: Path = args.folder.resolve()
    if dest.exists() and any(dest.iterdir()):
        print(f"{dest} isn't empty: pick a new folder.")
        return 2
    have = chosen(args)
    picked = files_for(have)
    write(dest, picked, have, args.name, args.profile)
    record(dest, args.name, args.profile, args.visibility)
    git(dest, "init", "-q", "-b", "main")
    git(dest, "add", "-A")

    parts = [p for p, on in (("AWS", args.aws), ("screens", args.ui)) if on]
    print(f"Made {dest}: {args.profile}, {args.visibility}, {len(picked) + 2} files,", end=" ")
    print(f"with {', '.join(parts) or 'the core only'}.")
    problems = stale(dest, left_out_paths(picked))
    problems += subprocess.run(
        [sys.executable, "scripts/check-refs.py"],
        cwd=dest,
        capture_output=True,
        encoding="utf-8",
        check=False,
    ).stdout.splitlines()[:-1]
    if problems:
        print("\nStill naming a file the project doesn't have; reword or delete each:")
        print("\n".join(f"  {p}" for p in problems))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
