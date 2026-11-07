<div align="center">

# sdlc-template

**A starting point for new projects: AI and web apps on AWS, built by coding agents through one development lifecycle, with Terraform and GitHub Actions as standard.**

![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-OIDC-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-Cloud-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)

[Use it](#-use-it) · [Lifecycle](#-lifecycle) · [Apps](#-apps) · [Repo](#-repo) · [Bootstrap](#-bootstrap) · [Cleanup](#-cleanup) · [Roadmap](#-roadmap)

</div>

---

## ⚡ At a glance

One repo per product. Apps go in `apps/`, each one self-contained. Cloud infrastructure goes in `aws/` as Terraform, one root and state per deployable unit, planned on a PR and applied after approval. Coding agents start at [AGENTS.md](AGENTS.md) and build from [docs/](docs/).

## 🧰 Use it

```
gh repo create <project> --template euginevd/sdlc-template --private --clone
```

Then replace the placeholders: this README's title and tagline, the Context section of [AGENTS.md](AGENTS.md), and [docs/SPEC.md](docs/SPEC.md).

## 🔁 Lifecycle

DevSecOps: security is built into every stage, not added at the end. The person owns *what* and *why*. The agent owns *how*, inside the rules in [docs/](docs/).

| # | Stage | Who | Output | Security |
|:-:|-------|-----|--------|----------|
| 1 | **Plan** | Person, then agent | [docs/SPEC.md](docs/SPEC.md), then `docs/PLAN_<NAME>.md` with phases and checkbox criteria. The person approves the plan before any code | Threat model in `docs/SECURITY.md` once there are users, data or secrets |
| 2 | **Code** | Agent | One phase at a time, to [docs/CODE_STANDARDS.md](docs/CODE_STANDARDS.md) | No secrets in code; pre-push secret and IaC scan *(planned)* |
| 3 | **Build** | Pipeline | Lint, format, type checks, `terraform validate` | Dependencies pinned; SCA and SAST scans *(planned)* |
| 4 | **Test** | Agent and pipeline | Unit and end-to-end tests, then a fresh-subagent review of the diff | IaC scan; tests never call real models or cloud |
| 5 | **Release** | Agent | PR with checks green, merged, branch deleted | Branch protection; CI actions pinned to a commit SHA |
| 6 | **Deploy** | Pipeline | Terraform plan on the PR, apply after approval | OIDC to least-privilege roles; no access keys |
| 7 | **Operate** | Person | Runbooks in [guides/](guides/), costs in `docs/FINOPS.md` | Patching, key rotation, access reviews |
| 8 | **Monitor** | Person and pipeline | [docs/STATUS.md](docs/STATUS.md) and [docs/DECISIONS.md](docs/DECISIONS.md) updated, the plan deleted | Logs, alerts and cloud security findings feed the next Plan |

## 🧪 Apps

| App | What | Stack | Deploys to |
|-----|------|-------|------------|
| *(none yet)* | | | |

## 📦 Repo

| Path | What |
|------|------|
| [apps/](apps/) | One folder per app (web, API, agent), each self-contained with its own tests |
| [aws/](aws/) | Terraform, one folder and state per deployable unit |
| [aws/bootstrap/](aws/bootstrap/) | OIDC provider, state bucket, plan and deploy roles *(planned)* |
| [.github/workflows/](.github/workflows/) | One workflow per folder, triggered by its path: checks on a PR, apply after approval *(planned)* |
| [scripts/](scripts/) | One-time setup and helper scripts |
| [AGENTS.md](AGENTS.md), [docs/](docs/) | Spec, tech stack, standards, process, status and decisions, for people and coding agents |
| [guides/](guides/) | Reference and how-tos for people |

## 🚀 Bootstrap

Once per project, before the first deploy.

| # | Where | Step |
|:-:|-------|------|
| 1 | **AWS Console** | Deploy the bootstrap stack from [aws/bootstrap/](aws/bootstrap/) *(planned)* |
| 2 | **GitHub** | Settings → Environments: create `aws-<target>-plan`, and `aws-<target>-apply` with yourself as required reviewer |
| 3 | **GitHub** | Settings → Secrets and variables → Actions → Variables: `AWS_PLAN_ROLE_ARN` and `AWS_DEPLOY_ROLE_ARN` from the stack's outputs |

## 🧹 Cleanup

| # | Where | Step |
|:-:|-------|------|
| 1 | **GitHub** | Destroy every Terraform root first, or its resources are orphaned |
| 2 | **AWS Console** | Empty the state bucket, then delete the bootstrap stack |
| 3 | **GitHub** | Settings → Environments: delete the plan and apply environments |

## 🎯 Roadmap

| # | Next | Detail |
|:-:|------|--------|
| 1 | **Docs** | Fill in the generic process, code standards and decision format |
| 2 | **Bootstrap** | OIDC, state bucket and plan and deploy roles for AWS |
| 3 | **Workflows** | Reusable CI for Terraform, Python and TypeScript |
| 4 | **Workstation guardrails** | Pre-push secret and IaC scan through lefthook |
| 5 | **Agent commands** | Shared plan, build, review and ship commands, as a plugin |
