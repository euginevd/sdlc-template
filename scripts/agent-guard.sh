#!/usr/bin/env bash
# Claude Code's PreToolUse hook: runs before the agent edits a file or runs a command, and enforces what
# AGENTS.md otherwise only asks. Production denies touching `.env` (rule 4; a prototype may edit it), and
# editing an existing test asks a person first, so the agent fixes the code rather than the test (rule 13).
# Deny rules and other agents: see guide 04, control 5.
set -uo pipefail

input=$(cat)
field() { printf '%s' "$input" | grep -o "\"$1\"[[:space:]]*:[[:space:]]*\"\([^\"\\\\]\|\\\\.\)*\"" | head -1 | sed 's/^[^:]*:[[:space:]]*"//; s/"$//'; }
decide() {
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"%s","permissionDecisionReason":"%s"}}\n' "$1" "$2"
  exit 0
}

# The repo root as Claude Code spells paths: C:/repo on Windows (Git Bash's pwd would say /c/repo).
root=$(cd "$(dirname "$0")/.." && { pwd -W 2> /dev/null || pwd; })
prototype=false
grep -qE '^Profile: .prototype.' "$root/docs/spec.md" 2> /dev/null && prototype=true

# A path as the repo sees it: forward slashes, relative to the root, any case.
path=$(field file_path | sed 's#\\\\#/#g')
rel=$(printf '%s' "$path" | sed "s#^$(printf '%s' "$root" | sed 's#[.[\*^$/]#\\&#g')/##I")
name=${rel##*/}
command=$(field command)

# Only the unquoted words of a command count, so a commit message or comment that mentions .env passes.
unquoted() { sed -E -e 's/\\"([^\\]|\\[^"])*\\"//g' -e "s/'[^']*'//g" <<< "$1"; }
env_named() {
  local words
  words=$(unquoted "$1")
  grep -Eq '(^|[^A-Za-z0-9_.-])\.env(\.[A-Za-z0-9_-]+)?([^A-Za-z0-9_.-]|$)' <<< "$words" && ! grep -Eqx '.*\.env\.example.*' <<< "$words"
}

# 1. `.env` (#178): production never reads or edits it; reading `.env.example` is fine.
if [ "$prototype" = false ]; then
  if [ -n "$name" ] && [[ "$name" == .env* ]] && [ "$name" != .env.example ]; then
    decide deny "Production never edits .env (AGENTS.md rule 4): the developer writes it."
  fi
  if [ -n "$command" ] && env_named "$command"; then
    decide deny "Production never reads or edits .env (AGENTS.md rule 4), even from a shell command."
  fi
fi

[ -n "$rel" ] && [ -f "$root/$rel" ] || exit 0

# 2. An existing test (#179): fix the code, not the test (AGENTS.md rule 13).
case "/$rel" in
  */tests/* | */test/* | */e2e/* | */test_*.py | */*_test.py | */*.test.ts | */*.test.tsx | */*.spec.ts | */*.spec.tsx)
    decide ask "This edits an existing test: approve only if the test itself is wrong (AGENTS.md rule 13)." ;;
esac
exit 0
