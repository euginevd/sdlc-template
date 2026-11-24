"""Tests for new-project.py: a new repo gets only the parts it asked for."""

import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "new-project.py"


def make(dest: Path, *flags: str, visibility: str = "public") -> str:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(dest), "--name", "demo", "--profile", "prototype"]
        + ["--visibility", visibility, *flags],
        capture_output=True,
        encoding="utf-8",
        check=True,
    )
    return result.stdout


def read(dest: Path, name: str) -> str:
    return (dest / name).read_text(encoding="utf-8")


def test_everything_kept_but_the_template_only_files(tmp_path: Path):
    dest = tmp_path / "demo"
    out = make(dest)
    for kept in ["AGENTS.md", "infra/aws/api/main.tf", "docs/web", ".github/workflows/aws.yml"]:
        assert (dest / kept).exists(), kept
    assert not (dest / "scripts/new-project.py").exists()
    assert not (dest / ".claude/skills/new-project").exists()
    assert "Still naming" not in out


def test_answers_go_in_the_spec(tmp_path: Path):
    dest = tmp_path / "demo"
    make(dest, visibility="private")
    spec = read(dest, "docs/spec.md")
    assert "Profile: `prototype`." in spec
    assert "Repo: `work` (private)." in spec
    assert "Name: `demo`." in spec
    assert "## Stack" in spec, "only the three lines change"
    assert not (dest / "CONTRIBUTING.md").exists()


def test_no_aws_drops_its_files_and_lines(tmp_path: Path):
    dest = tmp_path / "demo"
    out = make(dest, "--no-aws")
    for gone in ["infra", "docs/aws", ".github/workflows/aws.yml", ".claude/skills/deploy"]:
        assert not (dest / gone).exists(), gone
    assert "terraform" not in read(dest, ".github/dependabot.yml")
    assert "## AWS" not in read(dest, "docs/lessons.md")
    assert "## CI" in read(dest, "docs/lessons.md")
    assert "AGENTS.md:" in out, "AGENTS.md links to docs/aws/costs.md"


def test_no_ui_drops_the_design_system(tmp_path: Path):
    dest = tmp_path / "demo"
    out = make(dest, "--no-ui")
    assert not (dest / "docs/web").exists()
    assert not (dest / ".claude/skills/review-design").exists()
    assert (dest / "infra").exists()
    assert "docs/web/design-system.md" in out


def test_the_result_is_a_staged_git_repo(tmp_path: Path):
    dest = tmp_path / "demo"
    make(dest, "--no-aws", "--no-ui")
    staged = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        cwd=dest,
        capture_output=True,
        encoding="utf-8",
        check=True,
    ).stdout.splitlines()
    assert "AGENTS.md" in staged
    assert not any(f.startswith("infra/") for f in staged)


@pytest.mark.parametrize("name", ["bad name", "a/b"])
def test_a_bad_name_or_used_folder_is_refused(tmp_path: Path, name: str):
    used = tmp_path / "used"
    used.mkdir()
    (used / "x").write_text("x", encoding="utf-8")
    for dest, repo in [(tmp_path / "new", name), (used, "demo")]:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(dest), "--name", repo]
            + ["--profile", "prototype", "--visibility", "public"],
            capture_output=True,
            encoding="utf-8",
            check=False,
        )
        assert result.returncode == 2
