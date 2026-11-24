"""Tests for new-project.py: a new repo gets only what it needs, with nothing stale."""

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "new-project.py"
# CI's python job runs in uv's slim image, which has no git; a developer's machine has it.
pytestmark = pytest.mark.skipif(shutil.which("git") is None, reason="needs git")
COMBOS: dict[str, tuple[str, list[str]]] = {
    "slim prototype": ("prototype", []),
    "prototype with everything": ("prototype", ["--aws", "--ui"]),
    "production with everything": ("production", ["--aws", "--ui"]),
    "production without cloud or screens": ("production", []),
}


def make(dest: Path, profile: str = "prototype", *flags: str, visibility: str = "public") -> str:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(dest), "--name", "demo", "--profile", profile]
        + ["--visibility", visibility, *flags],
        capture_output=True,
        encoding="utf-8",
        check=True,
    )
    return result.stdout


def read(dest: Path, name: str) -> str:
    return (dest / name).read_text(encoding="utf-8")


@pytest.mark.parametrize("combo", COMBOS)
def test_every_combination_has_nothing_stale(tmp_path: Path, combo: str):
    profile, flags = COMBOS[combo]
    out = make(tmp_path / "demo", profile, *flags)
    assert "Still naming" not in out, out


def test_a_slim_prototype_gets_only_the_core(tmp_path: Path):
    dest = tmp_path / "demo"
    make(dest)
    for kept in ["docs/intent.md", "scripts/autopilot.sh", ".claude/agents/plan-reviewer.md"]:
        assert (dest / kept).exists(), kept
    for gone in [
        "infra",
        "docs/aws",
        "docs/web",
        "docs/threat-model.md",
        "SECURITY.md",
        ".github/workflows/aws.yml",
        ".github/workflows/codeql.yml",
        ".claude/skills/deploy",
        ".claude/skills/new-project",
        "scripts/new-project.py",
        "profiles",
        "guides/01-using-the-template.md",
    ]:
        assert not (dest / gone).exists(), gone
    assert sorted(p.name for p in (dest / "guides").iterdir()) == ["README.md"]


def test_a_prototype_gets_the_prototype_rules(tmp_path: Path):
    dest = tmp_path / "demo"
    make(dest)
    agents = read(dest, "AGENTS.md")
    assert "A prototype" in agents
    assert "autopilot" in agents
    assert "<!--" not in agents, "markers are dropped"
    assert "skills/deploy" not in agents
    assert "the project has no cloud" in agents


def test_production_gets_the_full_rules_and_its_docs(tmp_path: Path):
    dest = tmp_path / "demo"
    make(dest, "production", "--aws", "--ui")
    assert read(dest, "AGENTS.md").startswith("# Agent instructions\n\nNumbered")
    for kept in ["docs/threat-model.md", "docs/checklist.md", "infra/aws/api/main.tf", "docs/web"]:
        assert (dest / kept).exists(), kept
    assert (dest / "guides/03-security-trade-offs.md").exists()


def test_markers_keep_one_wording(tmp_path: Path):
    dest = tmp_path / "demo"
    make(dest, "production")
    agents = read(dest, "AGENTS.md")
    assert agents.count("\n12. ") == 1
    assert "the project has no cloud" in agents
    assert "<!--" not in read(dest, "docs/standards.md")


def test_links_to_left_out_files_point_at_the_template(tmp_path: Path):
    dest = tmp_path / "demo"
    make(dest)
    assert "github.com/euginevd/sdlc-template/blob/main/guides/03" in read(
        dest, "docs/decisions.md"
    )


def test_answers_go_in_the_spec_and_project(tmp_path: Path):
    dest = tmp_path / "demo"
    make(dest, visibility="private")
    spec = read(dest, "docs/spec.md")
    assert "Profile: `prototype`." in spec
    assert "Repo: `work` (private)." in spec
    assert "Name: `demo`." in spec
    assert 'name = "demo"' in read(dest, "pyproject.toml")
    assert "fail_under = 50" in read(dest, "pyproject.toml")
    assert not (dest / "CONTRIBUTING.md").exists()


def test_the_result_is_a_staged_git_repo(tmp_path: Path):
    dest = tmp_path / "demo"
    make(dest)
    staged = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        cwd=dest,
        capture_output=True,
        encoding="utf-8",
        check=True,
    ).stdout.splitlines()
    assert "AGENTS.md" in staged
    assert "guides/README.md" in staged
    assert not any(f.startswith("infra/") for f in staged)


@pytest.mark.parametrize("name", ["Bad Name", "a/b", "-x"])
def test_a_bad_name_is_refused(tmp_path: Path, name: str):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(tmp_path / "new"), "--name", name]
        + ["--profile", "prototype", "--visibility", "public"],
        capture_output=True,
        encoding="utf-8",
        check=False,
    )
    assert result.returncode == 2


def test_a_used_folder_is_refused(tmp_path: Path):
    (tmp_path / "x").write_text("x", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(tmp_path), "--name", "demo"]
        + ["--profile", "prototype", "--visibility", "public"],
        capture_output=True,
        encoding="utf-8",
        check=False,
    )
    assert result.returncode == 2


def upgrade(dest: Path, *flags: str) -> str:
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(dest), "--upgrade", *flags],
        capture_output=True,
        encoding="utf-8",
        check=True,
    ).stdout


def test_a_prototype_moves_to_production_keeping_its_own_files(tmp_path: Path):
    dest = tmp_path / "demo"
    make(dest)
    (dest / "docs/intent.md").write_text("Our own intent.\n", encoding="utf-8")
    out = upgrade(dest, "--profile", "production")
    assert read(dest, "docs/intent.md") == "Our own intent.\n"
    assert read(dest, "AGENTS.md").startswith("# Agent instructions\n\nNumbered")
    assert "Profile: `production`." in read(dest, "docs/spec.md")
    assert "fail_under = 80" in read(dest, "pyproject.toml")
    assert "Read(**/.env)" in read(dest, ".claude/settings.json")
    for added in ["docs/threat-model.md", "docs/checklist.md", "SECURITY.md"]:
        assert (dest / added).exists(), added
    assert "AGENTS.md" in out.split("Added")[1].split("\n")[0]


def test_a_part_added_later_lists_what_to_reconcile(tmp_path: Path):
    dest = tmp_path / "demo"
    make(dest)
    out = upgrade(dest, "--aws")
    assert (dest / "infra/aws/api/main.tf").exists()
    assert "Profile: `prototype`." in read(dest, "docs/spec.md")
    assert "docs/standards.md" in out.split("bring each in line")[1]


def test_upgrade_needs_a_project(tmp_path: Path):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(tmp_path), "--upgrade"],
        capture_output=True,
        encoding="utf-8",
        check=False,
    )
    assert result.returncode == 2
