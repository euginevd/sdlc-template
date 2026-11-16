#!/usr/bin/env bash
# One command for the checks CI runs (AGENTS.md rule 3). CI's python and web jobs call this script, so a pass here
# is a pass there; security.yml runs the same Terraform checks from a pinned image.
# Usage: bash scripts/check.sh [python|web|terraform|all]. With no argument, it checks what differs from origin/main,
# committed or not. Paste its last lines as the evidence when reporting a task done (AGENTS.md rule 13).
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

failed=()
passed=()
run() {
  local name=$1
  shift
  echo "--- $name"
  if "$@"; then
    passed+=("$name")
  else
    failed+=("$name")
    return 1
  fi
}

check_python() {
  [ -f pyproject.toml ] || return 0
  run "uv sync" uv sync --locked || return 0
  run "ruff format" uv run ruff format --check
  run "ruff" uv run ruff check
  run "pyright" uv run pyright
  run "pytest" uv run pytest -q
}

web() { npm --prefix apps/web "$@"; }
check_web() {
  [ -f apps/web/package-lock.json ] || return 0
  run "npm ci" web ci || return 0
  run "web lint" web run lint
  run "web typecheck" web run typecheck
  run "web test" web test
  run "web build" web run build
}

tf_validate() { terraform -chdir="$1" init -backend=false -input=false > /dev/null && terraform -chdir="$1" validate; }
check_terraform() {
  if ! command -v terraform > /dev/null; then
    echo "terraform isn't installed: run bash scripts/setup.sh"
    failed+=("terraform")
    return 0
  fi
  run "terraform fmt" terraform -chdir=infra/aws fmt -check -recursive -diff
  for dir in infra/aws/*/; do
    ls "$dir"*.tf > /dev/null 2>&1 || continue
    run "terraform validate ${dir%/}" tf_validate "$dir"
  done
}

# What changed, sorted the way ci.yml's changes job sorts it.
changed() {
  local base files
  base=$(git merge-base origin/main HEAD 2> /dev/null) || { echo "python web terraform"; return; }
  files=$( { git diff --name-only "$base"; git ls-files --others --exclude-standard; } | sort -u)
  local python=false web=false terraform=false
  while IFS= read -r f; do
    case "$f" in
      "") ;;
      apps/web/*) web=true ;;
      apps/* | *.py | pyproject.toml | uv.lock | .python-version) python=true ;;
      infra/*) terraform=true ;;
      *.md | docs/* | guides/* | LICENSE | .vscode/*) ;;
      .github/workflows/* | *.sh) python=true; web=true; terraform=true ;;
      *) python=true; web=true ;;
    esac
  done <<< "$files"
  local out=""
  $python && out+="python "
  $web && out+="web "
  $terraform && out+="terraform"
  echo "$out"
}

case "${1:-changed}" in
  python | web | terraform) targets=$1 ;;
  all) targets="python web terraform" ;;
  changed) targets=$(changed) ;;
  *) echo "Usage: bash scripts/check.sh [python|web|terraform|all]"; exit 2 ;;
esac

[ -n "$targets" ] || { echo "Nothing to check: only docs changed."; exit 0; }
for t in $targets; do "check_$t"; done

echo
echo "Checked: $targets"
[ ${#passed[@]} -eq 0 ] || echo "Passed: ${passed[*]}"
if [ ${#failed[@]} -gt 0 ]; then
  echo "FAILED: ${failed[*]}"
  exit 1
fi
echo "All checks passed."
