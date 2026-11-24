#!/usr/bin/env bash
# Claude Code's Stop hook: when the agent ends a turn with edits not yet committed, run the quick checks
# (bash scripts/check.sh, everything but itest and e2e, for what changed) and send any failure back so the
# agent fixes it before stopping. It blocks once: when the agent is already carrying on because of this
# hook, it lets it stop, so it can't loop. Other agents have no hook; the push hook and CI still run.
set -uo pipefail

input=$(cat)
if printf '%s' "$input" | grep -Eq '"stop_hook_active"[[:space:]]*:[[:space:]]*true'; then
  exit 0
fi

cd "$(dirname "$0")/.." || exit 0
# Nothing edited since the last commit: nothing new to check.
[ -n "$(git status --porcelain 2> /dev/null)" ] || exit 0

if out=$(bash scripts/check.sh 2>&1); then
  exit 0
fi
{
  echo "The quick checks failed as you ended your turn. Fix the cause, not the check, then finish:"
  printf '%s\n' "$out" | tail -n 40
} >&2
exit 2
