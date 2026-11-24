<div align="center">

# sdlc-template

**Start every project with a coding agent and a pipeline that's already safe.**<br>
Pick a prototype the agent builds and ships on its own, or a production system with a person at every gate.

[Quick start](#quick-start) · [Two profiles](#two-profiles) · [What's inside](#whats-inside) · [What always runs](#what-always-runs) · [Guides](#guides)

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="guides/assets/flow-dark.png">
  <img src="guides/assets/flow.png" width="900" alt="Six stages, kick off to release, on two tracks. Prototype: one stop, your yes to each item; the agent drafts the docs at kickoff, builds with main-path tests at 50% coverage, merges on green checks and the pipeline applies to dev on merge; there is no prod. Production: you approve the spec, threat model and costs, then the plan; the agent builds with abuse-case tests at 80% coverage and a review per phase; a second reviewer approves the PR, the dev apply and the prod release. Always on in both: Gitleaks and Trivy before every push, Semgrep, Checkov, CodeQL and app tests on every PR, a full rescan and SBOM on main and weekly, pipeline-only deploys over OIDC with no stored keys, and actual cost checked the day after a deploy.">
</picture>

</div>

## Why

Coding agents write code fast. What they don't bring is the rest: a spec to build against, a place to stop and ask, security scans, a safe way into AWS, and a record of what was decided. This template is that rest. Every agent reads the same numbered rules in [AGENTS.md](AGENTS.md), keeps the docs current as it works, and leaves AWS to a pipeline that scans, plans and applies for it.

It's for one developer or a small team, on Windows with VS Code, deploying to AWS with Terraform. It works with any agent that reads `AGENTS.md`.

You'll need: a GitHub account with the `gh` CLI, Git Bash or similar, and an AWS account once you're ready to deploy. A private repo needs a paid GitHub plan (Pro or Team) for the `main` ruleset and deploy environments. `setup.sh` installs the rest (Gitleaks, Trivy, lefthook, uv and Terraform).

## Quick start

```bash
gh repo create my-project --template euginevd/sdlc-template --public --clone  # --private for a work project
cd my-project
bash scripts/setup.sh         # tools and the Git hooks
bash scripts/protect-main.sh  # security features, the main ruleset, main-only deploys
```

Then tell your coding agent:

> Kick off my-project: *your notes on the business, the problem, the users and the stack*

It checks your machine and asks whether this is a prototype or production. A prototype's agent then drafts the docs from your notes and keeps going: *"Build the sign-up page"* builds it, and once you say the batch is ready, opens one PR, merges and ships it to `dev`. In production it waits for your approval at each gate, and *"Commit and push"* starts the PR. Every step: [guides/01-using-the-template.md](guides/01-using-the-template.md).

## Two profiles

You pick one at kickoff. The agent works on its own between gates and stops at the ones its profile has ([AGENTS.md](AGENTS.md) rule 5).

| | Prototype: speed first | Production: gates at key stages |
|---|---|---|
| For | No real users, customer data or payments | Anything that has them |
| You approve | Each issue's spec and mockup, before code | Kickoff, and every plan |
| A second reviewer approves | Nothing | Every PR and every apply, `dev` and `prod`, enforced by GitHub |
| Environments | `dev` only | `dev`, then `prod` |
| Tests | Main paths and anything sensitive, 50% coverage | Abuse cases too, 80% coverage |
| When unsure | The agent decides, records it and says so | The agent asks |
| Commits, PRs, merges | The agent, unasked | Only when you ask |

A prototype still stops before spending past the spec's monthly limit, weakening its own floor (no direct AWS changes, secrets in output, skipped hooks or AI attribution), or taking real users, customer data or payments. Moving a prototype up: [guide 01](guides/01-using-the-template.md) section 7.

## What's inside

| | |
|---|---|
| [AGENTS.md](AGENTS.md) | The numbered rules every coding agent reads: gates per profile, the workflow, what to ask first and what never to do |
| [docs/](docs/) | What the agent reads and keeps current: spec, features, decisions, lessons by area, threat model, costs, design system and go-live checklist. Each starts with a *(to fill in)* line for what your project decides |
| [apps/api/](apps/api/), [infra/aws/api/](infra/aws/api/) | The starter: a Lambda with a `/health` route and its Terraform, proving the pipeline end to end. Keep it, build on it or replace it |
| [.github/workflows/](.github/workflows/) | `ci` for changed apps, `security` and `codeql` scans, `rules` checks, `images` for signed images, `aws` to plan, cost, apply and scan `dev`, `factory` to build labelled issues |
| [infra/aws/bootstrap/](infra/aws/bootstrap/) | One stack per AWS account, deployed by you: the GitHub sign-in, a read-only plan role, a bounded deploy role, a read-only troubleshoot role, the state bucket, budget alert and optional GuardDuty |
| [scripts/](scripts/) | `setup.sh` installs and checks a machine, `protect-main.sh` locks down the repo, `pr-findings.sh` lists what a PR still has to fix, and the agent's hooks |

## What always runs

The same in both profiles:

1. **While the agent works:** Claude Code's hooks keep it out of `.env` in production and run the quick checks as each turn ends.
2. **Before every push:** Gitleaks and Trivy scan the pushed commits, so a secret added and then removed is still caught.
3. **On every PR:** secrets (Gitleaks), vulnerable packages and misconfiguration (Trivy, Checkov), static analysis (Semgrep, and CodeQL on public repos), `terraform validate`, tflint and a required Terraform plan, lint for workflows and scripts (actionlint, zizmor, shellcheck), rule checks (kickoff finished, references, agent hooks, no AI attribution), and lint, types and tests for the apps it changes. One comment lists the findings for the agent to fix.
4. **On `main` and weekly:** the full scans again, so a newly published vulnerability still fails a run, and an SBOM.
5. **Deploys:** only the pipeline touches AWS, signing in through GitHub OIDC with no stored keys. It plans with a read-only role and applies a saved plan, `dev` on merge and `prod` by hand. ZAP then scans `dev`, passively.
6. **Supply chain:** actions pinned by commit, images by digest, packages at least a week old, and each pushed image signed with its provenance and SBOM.

What it doesn't cover is written down too: [guides/03-security-trade-offs.md](guides/03-security-trade-offs.md) lists each risk accepted for speed, with its fix.

## Guides

1. [Using the template](guides/01-using-the-template.md): what you say and the agent does, from empty repo to deployed app.
2. [The files](guides/02-the-files.md): what every file is and why it's there.
3. [Security trade-offs](guides/03-security-trade-offs.md): the risks the template accepts, and the fix for each.
4. [The guardrails](guides/04-the-guardrails.md): how each checklist control works, by stage.
5. [Cleaning up AWS](guides/05-aws-cleanup.md): removing a project and proving nothing is charged.
6. [The secure agentic SDLC](guides/06-secure-agentic-sdlc.md): the six stages, their controls and gates.
7. [Template decisions](guides/07-template-decisions.md): what audits found, and the decisions made.
8. [Incident runbook](guides/08-incident-runbook.md): when a package, action or token is compromised.

To contribute, read [CONTRIBUTING.md](CONTRIBUTING.md); report vulnerabilities through [SECURITY.md](SECURITY.md). [MIT licence](LICENSE).
