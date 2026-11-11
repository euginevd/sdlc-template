<div align="center">

# sdlc-template

**One template, two speeds: a prototype your coding agent builds on its own, or a production system with a person at every gate.**

[Quick start](#quick-start) · [Two profiles](#two-profiles) · [What's inside](#whats-inside) · [What always runs](#what-always-runs) · [Guides](#guides)

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="guides/assets/overview-dark.png">
  <img src="guides/assets/overview.png" width="880" alt="The two profiles side by side across five stages. Kick off: in both, you approve the spec and the MVP mockup; production adds the threat model and costs. Plan: a prototype's agent writes a short plan and keeps going; in production you approve the plan. Build: a prototype tests the main paths with one review at 50% coverage; production has tests and a review in every phase at 80%. Merge: a prototype's agent merges once the checks pass; in production a second reviewer approves the PR. Deploy: a prototype's dev deploys unattended; in production a second reviewer approves every apply. Always on in both: the pre-push scan, secrets, dependencies, SAST and IaC checks, a protected main, OIDC with no keys, and pipeline-only deploys.">
</picture>

</div>

## Quick start

```bash
gh repo create my-project --template euginevd/sdlc-template --private --clone
cd my-project
bash scripts/setup.sh         # tools and the pre-push scan
bash scripts/protect-main.sh  # GitHub security features and the main ruleset
```

Then tell your coding agent:

> Kick off my-project: *your notes on the business, the problem, the users and the stack*

It checks your machine, asks whether this is a prototype or production, drafts the docs from your notes and waits for your approval. From there, *"Build the sign-up page"* is the whole loop for a prototype: plan, code, tests, PR, merge and a deploy to `dev`. Every step, for both profiles, is in [guides/01-using-the-template.md](guides/01-using-the-template.md).

## Two profiles

You pick one at kickoff, and the agent works differently for each.

| | Prototype: speed first | Production: approval first |
|---|---|---|
| For | No real users, customer data or payments | Anything that has them |
| You approve | Kickoff: the spec, and the MVP mockup if there's UI | Kickoff, and every plan |
| A second reviewer approves | Nothing | Every PR and every deploy, enforced by GitHub |
| Tests | Main paths and anything sensitive, 50% coverage | Every change, abuse cases included, 80% coverage |
| When unsure | The agent takes the simpler option and says so | The agent asks |

A prototype's agent stops and asks before the project takes real users, customer data, payments or a `prod` deploy. Moving up is one prompt and one command, `bash scripts/protect-main.sh production`.

## What's inside

| | |
|---|---|
| [AGENTS.md](AGENTS.md) | The rules the agent follows, numbered so reviews can cite them: what to read, how to plan, build, open a PR and merge, what to ask first and what never to do. Read by Claude Code, Codex, Cursor, Copilot and most coding agents |
| [docs/](docs/) | What the agent reads and keeps current: business context, spec, status, decisions, threat model, costs and a design system. Each starts as a true description of the starter, with a line to fill in for everything your project decides |
| [apps/api/](apps/api/), [infra/aws/api/](infra/aws/api/) | The starter: a Lambda with a `/health` route and the Terraform that deploys it. The smallest thing that proves the pipeline end to end; keep it, build on it or replace it |
| [.github/workflows/](.github/workflows/) | `ci` for the apps a PR changes, `security` and `codeql` for the scans, `aws` for the Terraform plan, the cost comment and the apply |
| [infra/aws/bootstrap/](infra/aws/bootstrap/) | One stack per AWS account, deployed by you: the GitHub sign-in, a read-only plan role, a bounded deploy role, the state bucket and a budget alert |
| [scripts/](scripts/) | `setup.sh` installs and checks a machine, `protect-main.sh` locks down the repo, `pr-findings.sh` lists what a PR still has to fix |

## What always runs

The same in both profiles:

1. **Before every push:** Gitleaks and Trivy scan the pushed commits, so a secret added and then removed is still caught.
2. **On every PR:** secrets (Gitleaks), vulnerable packages and misconfiguration (Trivy, Checkov), static analysis (Semgrep, and CodeQL on public repos), `terraform validate`, and lint, types and tests for the apps it changes. One summary comment lists the findings, and the agent fixes from it.
3. **On `main` and weekly:** the full scans again, so a vulnerability published after a merge still fails a run, plus a list of every package in the code (SBOM).
4. **Deploys:** only the pipeline touches AWS, signing in through GitHub OIDC with no stored keys. It plans with a read-only role and applies a saved plan, `dev` on merge and `prod` by hand.
5. **Supply chain:** actions pinned by commit, scanner images by digest, and packages at least a week old before they're installed.

What it doesn't cover is written down too: [guides/03-security-trade-offs.md](guides/03-security-trade-offs.md) lists each risk the template accepts for speed, with the fix for production.

## Guides

1. [Using the template](guides/01-using-the-template.md): what you say and what the agent does, from an empty repo to a deployed app.
2. [The files](guides/02-the-files.md): what every file is and why it's there.
3. [Security trade-offs](guides/03-security-trade-offs.md): the risks the template accepts, and the fix for each.

To contribute, read [CONTRIBUTING.md](CONTRIBUTING.md); report vulnerabilities through [SECURITY.md](SECURITY.md). [MIT licence](LICENSE).
