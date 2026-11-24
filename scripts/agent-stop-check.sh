#!/usr/bin/env bash
# Claude Code's Stop hook, in two parts.
# 1. When the agent ends a turn with edits not yet committed, run the quick checks (bash scripts/check.sh,
#    everything but itest and e2e, for what changed) and send any failure back so it fixes it first. This
#    blocks once: when the agent is already carrying on because of this hook, the checks wait for next time.
# 2. A prototype's autopilot (scripts/autopilot.sh, AGENTS.md rule 7): while it's on, send the agent back to
#    the next open issue. It lets the agent stop when the backlog is empty, the time is up, GitHub can't be
#    read, or two turns in a row made no progress, so it can't loop on nothing.
# Other agents have no hook; the push hook and CI still run.
set -uo pipefail

input=$(cat)
again=false
printf '%s' "$input" | grep -Eq '"stop_hook_active"[[:space:]]*:[[:space:]]*true' && again=true

cd "$(dirname "$0")/.." || exit 0

# 1. The quick checks, on uncommitted edits.
if [ "$again" = false ] && [ -n "$(git status --porcelain 2> /dev/null)" ]; then
  if ! out=$(bash scripts/check.sh 2>&1); then
    {
      echo "The quick checks failed as you ended your turn. Fix the cause, not the check, then finish:"
      printf '%s\n' "$out" | tail -n 40
    } >&2
    exit 2
  fi
fi

# 2. The autopilot.
state=.claude/autopilot
[ -f "$state" ] || exit 0
grep -qE '^Profile: .prototype.' docs/spec.md 2> /dev/null || { rm -f "$state"; exit 0; }
until=$(sed -n 's/^until=//p' "$state")
idle=$(sed -n 's/^idle=//p' "$state")
last=$(sed -n 's/^head=//p' "$state")
if [ "$(date +%s)" -ge "${until:-0}" ]; then
  rm -f "$state"
  exit 0
fi
open=$(gh issue list --state open --search "-label:blocked" --json number --jq length 2> /dev/null) || exit 0
if [ "${open:-0}" -eq 0 ]; then
  rm -f "$state"
  exit 0
fi
# Progress is a new commit or uncommitted work since the last time this hook sent the agent back.
head=$(git rev-parse HEAD 2> /dev/null)
if [ "$head" = "$last" ] && [ -z "$(git status --porcelain 2> /dev/null)" ]; then
  idle=$((${idle:-0} + 1))
else
  idle=0
fi
if [ "$idle" -ge 2 ]; then
  rm -f "$state"
  echo "Autopilot off: two turns in a row changed nothing." >&2
  exit 0
fi
printf 'until=%s\nidle=%s\nhead=%s\n' "$until" "$idle" "$head" > "$state"
{
  echo "Autopilot: $open open issue(s) and $(((until - $(date +%s)) / 60)) minutes left. Carry on with the oldest"
  echo "open issue without the blocked label (AGENTS.md rule 8). To stop for a reason rule 6 names, first run:"
  echo "bash scripts/autopilot.sh stop \"<why>\""
} >&2
exit 2
