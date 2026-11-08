# <project>

## Context

*(Replace: what this product is, who uses it, and where it runs.)*

- Account: `<aws-account-name>`, `ap-southeast-2`
- Users: *(who uses it)*
- Developer: on Windows (PowerShell, or Git Bash)

## Start here

IMPORTANT: read these in full before you plan, change or answer questions about anything:

1. `docs/SPEC.md`: what we need and what done means
2. `docs/TECH_STACK.md`: the tools and how it deploys
3. `docs/CODE_STANDARDS.md`: how to write the code
4. `docs/PROCESS.md`: how to plan, build, review and ship, stage by stage
5. `docs/STATUS.md`: what's built and what's next
6. `docs/DECISIONS.md`: what's settled and why; don't reopen it unasked
7. `guides/03-findings.md`: what the account or tools do that we didn't expect
8. `docs/THREAT_MODEL.md`: data classification, threat model and controls, if the project uses it
9. `docs/COSTS.md`: one row per cost-bearing resource, if the project uses it

`THREAT_MODEL.md` and `COSTS.md` are used only if required. If the project doesn't need one, delete it and its line above.

Add these only when needed, and list them above once they exist:

- `docs/PLAN_<NAME>.md`: when asked to plan a piece of work
- `docs/DESIGN.md`: UX decisions and look, once there's a UI
- `guides/<NN>-<topic>.md`: how-tos and reference for people

## Your role

- The user directs the work one step at a time. Do the step asked, report, then stop.
- Build only what `docs/` asks for. Don't build ahead or add side proposals.
- Ask when a requirement is unclear or two documents conflict.
- Explain your work when asked, at the level asked for.

## Conventions

- One app per folder in `apps/<app>/`, each with its own dependencies, tests and README.
- One Terraform root per deployable unit in `aws/<unit>/`, state key `<project>/<unit>.tfstate`. Copy `aws/_template/` to start one.
- Names: resources `<project>-<unit>-<what>`, roles `<project>-<unit>[-<purpose>]`.
- Every role Terraform creates has the `<project>-boundary` permissions boundary.
- A new AWS service needs plan and deploy permissions in the bootstrap stack first.

## Folders

- `apps/<app>/`: the apps (web, API, agent)
- `aws/<unit>/`: Terraform, one root and state per deployable unit
- `aws/_template/`: the starting files for a new unit; never deployed
- `aws/bootstrap/`: the CloudFormation stack for OIDC, state and the pipeline roles
- `.github/workflows/`: one workflow per top-level folder; plan on PR, apply after approval
- `.lefthook/`, `lefthook.yml`: the pre-push scan
- `scripts/`: one-time `setup.sh`, and `scan.sh`, the scan the pre-push hook runs
- `docs/`: the documents the agent builds from
- `guides/`: reference for people, such as findings and how-tos, named `<NN>-<topic>.md` (`01`, `02`, …) so they sort in reading order
- `local/`: personal scratch, not in git

## Repo layout

Prefer one repo per product, not per app, cloud or component:

- A top-level folder per kind of deployable part (`apps/`, `aws/`), each self-contained.
- One workflow per folder, triggered only by changes under its path, with its own credentials and environments named `<cloud>-<target>-plan` and `<cloud>-<target>-apply` (`aws-dev-plan`, `aws-dev-apply`); only `-apply` needs approval.
- One Terraform root and state per deployable unit inside `aws/`.
- Shared docs at the root (`AGENTS.md`, `docs/`, `guides/`).

## Rules

- Work on a branch and open a PR. Merge once checks pass, then delete the branch; only `main` remains.
- Never create, change or delete cloud resources yourself; the pipeline and the user do. Read-only checks are fine.
- One-line commit messages, human author only. No AI co-author or attribution lines.
