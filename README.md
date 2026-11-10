<div align="center">

# sdlc-template

**Start every project with AI coding agents that plan before they code, and checks that catch what they miss.**

<img src="https://img.shields.io/badge/Terraform-7B42BC?style=flat-square&logo=terraform&logoColor=white" alt="Terraform">
<img src="https://img.shields.io/badge/AWS-FF9900?style=flat-square" alt="AWS">
<img src="https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white" alt="GitHub Actions">
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/uv-DE5FE9?style=flat-square&logo=uv&logoColor=white" alt="uv">
<img src="https://img.shields.io/badge/Trivy-1904DA?style=flat-square&logo=trivy&logoColor=white" alt="Trivy">

[Quick start](#quick-start) · [What you get](#what-you-get) · [Built with](#built-with) · [Guides](#guides)

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="guides/assets/lifecycle-dark.png">
  <img src="guides/assets/lifecycle.png" width="880" alt="The secure agentic SDLC in six stages, Plan, Code, Build and test, Release, Deploy, Operate and monitor, showing for each what the agent does, what the automatic controls check, and what people decide.">
</picture>

</div>

## Quick start

```bash
gh repo create my-project --template euginevd/sdlc-template --private --clone
cd my-project
bash scripts/setup.sh        # tools and the pre-push scan
bash scripts/protect-main.sh # GitHub security features and the main ruleset
```

Then kick off: your agent asks whether this is a `prototype`, built for speed with fewer gates, or `production`. It drafts the business context, spec, and if they apply the threat model, costs and design system, from your notes. You approve each, and record which [trade-offs](guides/02-security-trade-offs.md) you accept in `docs/decisions.md`, before the first *"Plan <the work>"*. Full steps: [guides/01-using-the-template.md](guides/01-using-the-template.md), sections 1 to 3.

## What you get

| | |
|---|---|
| **Agent rules** | [AGENTS.md](AGENTS.md), read by Claude Code, Codex, Cursor, Copilot and most coding agents: plan before code, build in reviewed phases, one PR per plan, never push to `main` |
| **Spec-driven docs** | [docs/](docs/): business context, spec, plan, threat model, decisions, design system and costs, which the agent reads and keeps current |
| **Security checks** | A scan on every push, and on every PR: SAST, secrets, dependencies, IaC and a security summary comment the agent fixes from |
| **Infrastructure** | Terraform on AWS through GitHub OIDC: plan with a read-only role, apply with approval, `dev` on merge and `prod` by hand |
| **A worked example** | `travel-claims`, an insurance claims app, described in [docs/](docs/) to replace with your own; [apps/api/](apps/api/) is a sample Lambda with a `/health` route |

## Built with

| Tool | What it does here | Where |
|------|-------------------|-------|
| Terraform | AWS infrastructure, one root per app | [infra/aws/](infra/aws/) |
| GitHub Actions | App checks, security scans, Terraform plan and apply | [.github/workflows/](.github/workflows/) |
| Python, uv | Apps, scripts and one locked workspace | [pyproject.toml](pyproject.toml) |
| Semgrep, CodeQL | Static analysis | [security.yml](.github/workflows/security.yml), [codeql.yml](.github/workflows/codeql.yml) |
| Gitleaks | Secrets in code and history | [scan.sh](scripts/scan.sh) |
| Trivy, Checkov | Vulnerable packages, images and IaC misconfiguration | [security.yml](.github/workflows/security.yml) |
| Infracost | Cost of each Terraform change, as a PR comment | [aws.yml](.github/workflows/aws.yml) |
| Lefthook, Dependabot | The pre-push scan; weekly package updates | [lefthook.yml](lefthook.yml), [dependabot.yml](.github/dependabot.yml) |

## Guides

1. [Using the template](guides/01-using-the-template.md): what you say and what the agent does, end to end, for a prototype or a production project; the plan skeleton and every file in the appendices.
2. [Security trade-offs](guides/02-security-trade-offs.md): the risks the template accepts, and the fix for production.

To contribute, read [CONTRIBUTING.md](CONTRIBUTING.md); report vulnerabilities through [SECURITY.md](SECURITY.md). MIT licence.
