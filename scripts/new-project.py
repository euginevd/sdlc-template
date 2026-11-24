"""Makes a new project's folder from this template, keeping only the parts it needs.

Run by the new-project skill, after it has asked the developer what the project is. Copies the
template's files (as git sees them, so nothing ignored), drops the modules the project doesn't use,
records the profile and repo type in docs/spec.md, and stages it all in a fresh Git repo for the
skill to commit and push.
It then lists each line that still mentions a removed file, for the agent to reword or delete.
Usage: python scripts/new-project.py <folder> --name <name> --profile prototype|production
           --visibility public|private [--no-aws] [--no-ui]
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# What only the template needs: making projects is its job, not theirs.
TEMPLATE_ONLY = [
    ".claude/skills/new-project",
    "scripts/new-project.py",
    "scripts/tests/test_new_project.py",
]
# A public repo invites contributions and shows a preview image; a private one has neither.
PUBLIC_ONLY = ["CONTRIBUTING.md", "guides/assets/social.png"]
AWS = [
    "infra",
    "docs/aws",
    ".github/workflows/aws.yml",
    ".github/workflows/images.yml",
    ".claude/skills/deploy",
    "guides/05-aws-cleanup.md",
    "scripts/cost-report.py",
    "scripts/tests/test_cost_report.py",
]
UI = ["docs/web", ".claude/skills/review-design"]


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, encoding="utf-8", check=True
    ).stdout


def copy_template(dest: Path) -> None:
    """Every file Git tracks or would track, as it is on disk now."""
    files = git(ROOT, "ls-files", "--cached", "--others", "--exclude-standard").splitlines()
    for name in files:
        src = ROOT / name
        if src.is_file():
            (dest / name).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest / name)


def remove(dest: Path, paths: list[str]) -> list[str]:
    """Deletes each path that exists; returns the ones it deleted."""
    gone: list[str] = []
    for path in paths:
        target = dest / path
        if target.is_dir():
            shutil.rmtree(target)
        elif target.is_file():
            target.unlink()
        else:
            continue
        gone.append(path)
    return gone


def edit(path: Path, pattern: str, replacement: str, *, across_lines: bool = False) -> None:
    """One regex replacement; ^ and $ are per line, and . crosses lines only when asked."""
    flags = re.MULTILINE | (re.DOTALL if across_lines else 0)
    text = path.read_text(encoding="utf-8")
    path.write_text(re.sub(pattern, replacement, text, count=1, flags=flags), encoding="utf-8")


def drop_aws_text(dest: Path) -> None:
    """The lines outside the deleted files that only make sense with AWS."""
    edit(
        dest / ".github/dependabot.yml",
        r"  - package-ecosystem: terraform\n(?:    .*\n)+",
        "",
    )
    edit(dest / "docs/lessons.md", r"^## AWS\n\n.*?\n\n(?=## )", "", across_lines=True)


def record(dest: Path, name: str, profile: str, visibility: str) -> None:
    """The answers the template's kickoff would otherwise ask again."""
    spec = dest / "docs/spec.md"
    repo = "personal" if visibility == "public" else "work"
    edit(spec, r"^Profile: .*$", f"Profile: `{profile}`.")
    edit(spec, r"^Repo: .*$", f"Repo: `{repo}` ({visibility}).")
    edit(spec, r"^Name: .*$", f"Name: `{name}`.")


LINK = re.compile(r"\]\(([^)#\s]+)")
TICKED = re.compile(r"`([\w.-]+/[\w./<>-]*)`")
# The files every session reads or acts on: here a removed path named in backticks is stale too.
STRICT = ("AGENTS.md", "README.md", "docs/", ".claude/")


def stale(dest: Path, gone: list[str]) -> list[str]:
    """Each line of Markdown that links to a file that's gone or, where it matters, names one."""
    found: list[str] = []
    for path in sorted(dest.rglob("*.md")):
        if ".git" in path.parts:
            continue
        rel = path.relative_to(dest).as_posix()
        strict = rel.startswith(STRICT)
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            broken = [
                target
                for target in LINK.findall(line)
                if "://" not in target
                and not target.startswith("mailto:")
                and not (path.parent / target).exists()
            ]
            if strict:
                broken += [
                    named
                    for named in TICKED.findall(line)
                    if any(named == g or named.startswith(f"{g}/") for g in gone)
                ]
            if broken:
                found.append(f"{rel}:{lineno}: {', '.join(dict.fromkeys(broken))}")
    return found


def parse(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Makes a new project from this template.")
    parser.add_argument("folder", type=Path)
    parser.add_argument("--name", required=True)
    parser.add_argument("--profile", required=True, choices=["prototype", "production"])
    parser.add_argument("--visibility", required=True, choices=["public", "private"])
    parser.add_argument(
        "--no-aws", action="store_true", help="no AWS: drop infra/ and its pipeline"
    )
    parser.add_argument("--no-ui", action="store_true", help="no screens: drop docs/web/")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]  # Windows consoles
    args = parse(argv)
    if not re.fullmatch(r"[A-Za-z0-9._-]+", args.name):
        print(f"{args.name}: a repo name is letters, digits, '.', '_' and '-' only.")
        return 2
    dest: Path = args.folder.resolve()
    if dest.exists() and any(dest.iterdir()):
        print(f"{dest} isn't empty: pick a new folder.")
        return 2
    dest.mkdir(parents=True, exist_ok=True)
    copy_template(dest)

    gone = remove(dest, TEMPLATE_ONLY)
    if args.visibility == "private":
        gone += remove(dest, PUBLIC_ONLY)
    if args.no_aws:
        gone += remove(dest, AWS)
        drop_aws_text(dest)
    if args.no_ui:
        gone += remove(dest, UI)
    record(dest, args.name, args.profile, args.visibility)

    git(dest, "init", "-q", "-b", "main")
    git(dest, "add", "-A")

    kept = [m for m, off in (("AWS", args.no_aws), ("screens", args.no_ui)) if not off]
    parts = ", ".join(kept) or "the core only"
    print(f"Made {dest}: {args.profile}, {args.visibility}, with {parts}.")
    print(f"Removed {len(gone)}: {', '.join(gone)}")
    lines = stale(dest, gone)
    refs = subprocess.run(
        [sys.executable, "scripts/check-refs.py"],
        cwd=dest,
        capture_output=True,
        encoding="utf-8",
        check=False,
    ).stdout.splitlines()[:-1]
    if lines or refs:
        print("\nStill naming a removed file; reword or delete each:")
        print("\n".join(f"  {line}" for line in lines + refs))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
