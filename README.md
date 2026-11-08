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

Then:

1. Replace `<project>` everywhere, the README's title and tagline, and the Context section of [AGENTS.md](AGENTS.md).
2. Run `bash scripts/setup.sh` for the pre-push scan ([git-hooks](guides/02-git-hooks.md)), and `bash scripts/protect-main.sh` for the `main` ruleset (needs a public repo or a paid plan).
3. Fill in [docs/spec.md](docs/spec.md), `tech-stack.md` and `status.md` under their headings. Keep `code-standards.md`, `process.md`, the workflow and the scripts as they are, and add your own entries to `decisions.md`. Keep `threat-model.md` and `costs.md` only if required.
4. Keep the sample Terraform units you need (`aws/iam`, `aws/storage`, `aws/api`) and delete the rest. For a new unit, copy the closest sample.
5. Ask the agent to plan. How it all fits: [guides/01-agentic-sdlc.md](guides/01-agentic-sdlc.md).

## 🔁 Lifecycle

Eight DevSecOps stages, with security built into each, and the flow of a change from spec to deploy: [guides/01-agentic-sdlc.md](guides/01-agentic-sdlc.md).

## 🧪 Apps

| App | What | Stack | Deploys to |
|-----|------|-------|------------|
| *(none yet)* | | | |

## 📦 Repo

| Path | What |
|------|------|
| [apps/](apps/) | One folder per app (web, API, agent), each self-contained with its own tests |
| [aws/](aws/) | Terraform, one folder and state per deployable unit |
| [aws/iam/](aws/iam/), [aws/storage/](aws/storage/), [aws/api/](aws/api/) | Sample units: app role, S3 bucket, Lambda behind an HTTP API |
| [aws/bootstrap/](aws/bootstrap/) | CloudFormation stack: OIDC provider, state bucket, plan and deploy roles, permissions boundary |
| [.github/workflows/](.github/workflows/) | `aws.yml`: plans changed units on a PR, applies after approval |
| [scripts/](scripts/), `lefthook.yml`, `.lefthook/`, `.vscode/` | Developer workstation guardrails: one-time setup, the gitleaks and Trivy pre-push scan, recommended extensions |
| [AGENTS.md](AGENTS.md), [docs/](docs/) | Spec, tech stack, standards, process, status and decisions, for people and coding agents |
| [SECURITY.md](SECURITY.md) | How to report a vulnerability |
| [guides/](guides/) | Reference: [secure agentic SDLC](guides/01-agentic-sdlc.md), [git hooks](guides/02-git-hooks.md), [findings](guides/03-findings.md) |

## 🚀 Bootstrap

Once per project, before the first deploy, as an admin in the project's AWS account.

| # | Where | Step |
|:-:|-------|------|
| 1 | **AWS Console** | CloudFormation → Create stack → Upload [bootstrap.yaml](aws/bootstrap/bootstrap.yaml) → name `<project>-bootstrap` → fill in the parameters (`CreateOidcProvider` false if the account already has GitHub's) → acknowledge IAM resources → Submit |
| 2 | **GitHub** | Settings → Environments: create `aws-<target>-plan`, and `aws-<target>-apply` with yourself as required reviewer |
| 3 | **GitHub** | Settings → Secrets and variables → Actions → Variables: `AWS_PLAN_ROLE_ARN`, `AWS_DEPLOY_ROLE_ARN` and `TF_STATE_BUCKET` from the stack's outputs; `AWS_TARGET` if it isn't `dev` |
| 4 | **GitHub** | When the repo goes public: Settings → Security → turn on Private vulnerability reporting, which [SECURITY.md](SECURITY.md) points to |

A new AWS service: add its permissions to the template, then CloudFormation → `<project>-bootstrap` → Update → Replace existing template.

## 🧹 Cleanup

| # | Where | Step |
|:-:|-------|------|
| 1 | **GitHub** | Destroy every unit first (Actions → `aws` → Run workflow → `all`, `destroy`), or its resources are orphaned |
| 2 | **AWS Console** | Empty the state bucket, then delete the bootstrap stack |
| 3 | **GitHub** | Settings → Environments: delete the plan and apply environments |

## 🎯 Roadmap

| # | Next | Detail |
|:-:|------|--------|
| 1 | **Pipeline scans** | `tflint`, Trivy and gitleaks in CI, so the PR re-checks what the pre-push hook can skip |
| 2 | **App workflows** | CI for Python and TypeScript apps in `apps/` |
| 3 | **Required checks** | Add each project's CI checks to the `main` ruleset once they exist |
| 4 | **Agent commands** | Shared plan, build, review and ship commands, as a plugin |
