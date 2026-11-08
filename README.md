<div align="center">

# travel-claims

**An AI agent decides routine travel insurance claims in minutes, so handlers spend their time only on claims that need judgement.**

![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-OIDC-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-Cloud-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)

[Apps](#-apps) · [Docs](#-docs) · [Bootstrap](#-bootstrap) · [Cleanup](#-cleanup) · [New project](#-new-project)

</div>

---

A worked example built from [sdlc-template](https://github.com/euginevd/sdlc-template), the starting point for every project. How it's built: [guides/01-agentic-sdlc.md](guides/01-agentic-sdlc.md).

## 🧪 Apps

| App | What | Runs on |
|-----|------|---------|
| `web` | Claimants submit and track claims; handlers review them | S3 and CloudFront |
| `api` | Claims, receipts, decisions and payments | Lambda behind an HTTP API |
| `agent` | Decides each claim against the policy wording | Lambda, Claude on Bedrock |

`apps/` holds a sample `api` health check in the template; the docs describe all three.

## 📚 Docs

| File | What |
|------|------|
| [AGENTS.md](AGENTS.md) | Rules for every coding agent |
| [business-context.md](docs/business-context.md) | The business: Wattle Travel Insurance (fictional) |
| [spec.md](docs/spec.md) | The project and what done means |
| [code-standards.md](docs/code-standards.md) | How to write the code |
| [status.md](docs/status.md) | What's built and what's next |
| [decisions.md](docs/decisions.md) | Key decisions and why |
| [design-system.md](docs/design-system.md) | Look and feel, from the ArcVault design system |
| [threat-model.md](docs/threat-model.md), [costs.md](docs/costs.md) | Threats and controls; what it costs |
| [02-security-trade-offs.md](guides/02-security-trade-offs.md) | The template's accepted risks, and what to change for production |

## 🚀 Bootstrap

Once per AWS account (`dev`, then `prod`), as an admin:

1. **AWS Console:** CloudFormation → upload [bootstrap.yaml](aws/bootstrap/bootstrap.yaml) as `travel-claims-bootstrap`, with `ProjectName` `travel-claims`, `GitHubOwner` and `GitHubRepo` as in the repo URL, and `Target` `dev` or `prod` (`CreateOidcProvider` false if the account already has GitHub's).
2. **GitHub:** Settings → Environments: `aws-<target>-plan`, and `aws-<target>-apply` with yourself as required reviewer and deployment branches limited to `main`.
3. **GitHub:** Settings → Variables: `PROJECT_NAME` (`travel-claims`) for the repo. Then on each environment, from that account's stack outputs: `AWS_PLAN_ROLE_ARN` on `-plan`, `AWS_DEPLOY_ROLE_ARN` on `-apply`, and `TF_STATE_BUCKET` on both.

**Deploying:** a merge to `main` applies to `dev` after your approval. To promote to `prod`: Actions → `aws` → Run workflow → target `prod`, `all`, `apply`, then approve.

## 🧹 Cleanup

1. **GitHub:** Actions → `aws` → Run workflow → each target, `all`, `destroy`.
2. **AWS Console:** empty the state bucket, then delete the bootstrap stack.
3. **GitHub:** delete the plan and apply environments.

## 🆕 New project

1. `gh repo create <name> --template euginevd/sdlc-template --private --clone`, then `bash scripts/setup.sh` and `bash scripts/protect-main.sh` (Actions limits, squash-only merges, GitHub's security features and the `main` ruleset). A private repo needs a paid GitHub plan for the ruleset and the approval environments; a public repo gets them free.
2. Replace the worked example: `business-context.md` per business; `spec.md`, `status.md`, this README and the root `pyproject.toml` name (then `uv lock`) per project; `decisions.md`. Keep `design-system.md`, `threat-model.md` and `costs.md` only if needed. Replace or delete `LICENSE` (MIT, for the template).
3. Keep `AGENTS.md`, `code-standards.md`, the workflow and the scripts as they are.
4. Ask the agent to plan. The full flow: [guides/01-agentic-sdlc.md](guides/01-agentic-sdlc.md), section 2.
