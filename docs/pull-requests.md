# Pull requests

How the agent takes a branch through gate G2 ([AGENTS.md](../AGENTS.md) rule 11). When to open one, per profile, is that rule.

1. One branch per work session, one PR per branch. Small changes and follow-ups join the open PR or wait for the next; check for an open PR before opening one.
2. The body follows `.github/pull_request_template.md`, with a Security line: threat model changes, new skips, packages or permissions.
3. Findings: `bash scripts/pr-findings.sh <pr>`. Fix critical and high at their cause, medium and low when real; answer the rest and resolve the thread (`bash scripts/pr-findings.sh resolve <thread-id> "<reply>"`). A skip is a last resort, with a one-line reason.
4. Merge: `gh pr update-branch` if `main` has moved, then squash-merge (a prototype once checks pass, production once a second reviewer approves), and delete the branch locally and on GitHub.
