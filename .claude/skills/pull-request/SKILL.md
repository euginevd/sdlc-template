---
name: pull-request
description: Takes a branch through gate G2 (AGENTS.md rules 10, 11 and 18): fixing review and check findings, improving from what went wrong, and the merge. Use when fixing a PR's findings or merging it.
---

# Pull request

When to open one, per profile: AGENTS.md rule 11; one branch and one PR per work session, with the body from `.github/pull_request_template.md`.

1. Findings, from a review skill during the build or the PR's checks (`bash scripts/pr-findings.sh <pr>`): fix critical and high at their cause before going on, and medium and low when real. Each one left gets a one-line reason: in the PR body, or on its thread, resolved with `bash scripts/pr-findings.sh resolve <thread-id> "<reply>"`. A real problem left for later becomes a GitHub issue; a skip is a last resort.
2. Improve, before the merge: look at what went wrong on this branch (review findings, the user's corrections, failed checks). A mistake made a second time becomes a check, or else a lesson in `docs/lessons.md` under its area. Drop lessons a check now covers or that are out of date.
3. Merge: `gh pr update-branch` if `main` has moved, then squash-merge (a prototype once checks pass, production once a second reviewer approves), and delete the branch locally and on GitHub.
