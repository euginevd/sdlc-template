#!/usr/bin/env bash
# A prototype's long run (AGENTS.md rule 7): while it's on, the Stop hook sends the agent back to the next
# open issue each time it tries to stop, until the backlog is empty, the time budget is spent, or the agent
# stops it for a reason rule 6 names. The state is one local, git-ignored file: .claude/autopilot.
# Usage: bash scripts/autopilot.sh start [hours]   on, for that many hours (default 8)
#        bash scripts/autopilot.sh stop "<why>"    off, with the reason the agent reports
#        bash scripts/autopilot.sh status
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
state=.claude/autopilot

case "${1:-status}" in
  start)
    hours=${2:-8}
    [[ "$hours" =~ ^[0-9]+$ ]] && [ "$hours" -gt 0 ] || { echo "Hours is a whole number above 0."; exit 2; }
    grep -qE '^Profile: .prototype.' docs/spec.md 2> /dev/null || {
      echo "Autopilot is for a prototype: production stops at its gates (AGENTS.md rule 5)."
      exit 1
    }
    mkdir -p .claude
    printf 'until=%s\nidle=0\nhead=%s\n' "$(($(date +%s) + hours * 3600))" "$(git rev-parse HEAD 2> /dev/null)" > "$state"
    echo "Autopilot on for $hours hours: the agent keeps building open issues until they're done."
    ;;
  stop)
    [ -n "${2:-}" ] || { echo "Say why: bash scripts/autopilot.sh stop \"<why>\""; exit 2; }
    rm -f "$state"
    echo "Autopilot off: $2"
    ;;
  status)
    if [ -f "$state" ]; then
      until=$(sed -n 's/^until=//p' "$state")
      echo "Autopilot on: $(((until - $(date +%s)) / 60)) minutes left."
    else
      echo "Autopilot off."
    fi
    ;;
  *) echo "Usage: bash scripts/autopilot.sh start [hours] | stop \"<why>\" | status"; exit 2 ;;
esac
