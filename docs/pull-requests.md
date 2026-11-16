# Pull requests

How the agent takes a branch through gate G2 ([AGENTS.md](../AGENTS.md) rules 10 and 11). When to open one, per profile: rule 11.

1. One branch per work session, one PR per branch. Small changes and follow-ups join the open PR or wait for the next; check for an open PR before opening one.
2. The body follows `.github/pull_request_template.md`, with a Security line: threat model changes, new skips, packages or permissions.
3. Findings, from a review skill during the build or the PR's checks (`bash scripts/pr-findings.sh <pr>`): fix critical and high at their cause before going on, and medium and low when real. Each one left gets a one-line reason: in the PR body, or on its thread, resolved with `bash scripts/pr-findings.sh resolve <thread-id> "<reply>"`. A real issue left for later becomes a `TODO.md` line; a skip is a last resort.
4. Merge: `gh pr update-branch` if `main` has moved, then squash-merge (a prototype once checks pass, production once a second reviewer approves), and delete the branch locally and on GitHub.
