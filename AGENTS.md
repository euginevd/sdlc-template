# <project>

## Context

*(Replace: what this product is, who uses it, the AWS account and region.)*

## Start here

IMPORTANT: read these in full before you plan, change or answer questions about anything:

1. `docs/SPEC.md`: what we need and what done means
2. `docs/TECH_STACK.md`: the tools and how it deploys
3. `docs/CODE_STANDARDS.md`: how to write the code
4. `docs/PROCESS.md`: how to plan, build, review and ship
5. `docs/STATUS.md`: what's built and what's next
6. `docs/DECISIONS.md`: what's settled and why; don't reopen it unasked

Add these only when needed, and list them above once they exist:

- `docs/PLAN_<NAME>.md`: when asked to plan a piece of work
- `docs/SECURITY.md`: threat model and controls, once there are users, data or secrets to protect
- `docs/FINOPS.md`: one row per cost-bearing resource, once there are several
- `docs/DESIGN.md`: UX decisions and look, once there's a UI
- `guides/<topic>.md`: how-tos and reference for people

## Your role

- The user directs the work one step at a time. Do the step asked, report, then stop.
- Build only what `docs/` asks for. Don't build ahead or add side proposals.
- Ask when a requirement is unclear or two documents conflict.

## Folders

- `apps/<app>/`: one folder per app, each self-contained with its own tests
- `aws/<unit>/`: one Terraform root and state per deployable unit
- `aws/bootstrap/`: OIDC, state bucket and pipeline roles
- `.github/workflows/`: one workflow per folder, triggered by its path
- `scripts/`: one-time setup and helpers
- `docs/`: the documents the agent builds from
- `guides/`: reference for people
- `local/`: personal scratch, not in git

## Rules

- Work on a branch and open a PR. Merge once checks pass, then delete the branch; only `main` remains.
- Never create, change or delete cloud resources yourself; the pipeline and the user do. Read-only checks are fine.
- One-line commit messages, human author only.
