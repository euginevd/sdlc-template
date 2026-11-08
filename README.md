# travel-claims

An AI agent decides routine travel insurance claims in minutes, so handlers spend their time only on claims that need judgement.

> This is [sdlc-template](https://github.com/euginevd/sdlc-template), with `travel-claims` as its worked example. To start a project from it: [guides/01-agentic-sdlc.md](guides/01-agentic-sdlc.md), section 2.

## Apps

| App | What | Runs on |
|-----|------|---------|
| `web` | Claimants submit and track claims; handlers review them | S3 and CloudFront |
| `api` | Claims, receipts, decisions and payments | Lambda behind an HTTP API |
| `agent` | Decides each claim against the policy wording | Lambda, Claude on Bedrock |

## Docs

Agent rules in [AGENTS.md](AGENTS.md); the project in [docs/](docs/), starting with [spec.md](docs/spec.md) and [status.md](docs/status.md); accepted risks in [guides/02-security-trade-offs.md](guides/02-security-trade-offs.md).

## Bootstrap

Once per AWS account (`dev`, then `prod`), as an admin:

1. **AWS Console:** CloudFormation → upload [bootstrap.yaml](aws/bootstrap/bootstrap.yaml) as `travel-claims-bootstrap`, with `ProjectName` `travel-claims`, `GitHubOwner` and `GitHubRepo` as in the repo URL, and `Target` `dev` or `prod` (`CreateOidcProvider` false if the account already has GitHub's).
2. **GitHub:** Settings → Environments: `aws-<target>-plan`, and `aws-<target>-apply` with yourself as required reviewer and deployment branches limited to `main`.
3. **GitHub:** Settings → Variables: `PROJECT_NAME` (`travel-claims`) for the repo. Then on each environment, from that account's stack outputs: `AWS_PLAN_ROLE_ARN` on `-plan`, `AWS_DEPLOY_ROLE_ARN` on `-apply`, and `TF_STATE_BUCKET` on both.

**Deploying:** a merge to `main` applies to `dev` after your approval. To promote to `prod`: Actions → `aws` → Run workflow → target `prod`, `all`, `apply`, then approve.

## Cleanup

1. **GitHub:** Actions → `aws` → Run workflow → each target, `all`, `destroy`.
2. **AWS Console:** empty the state bucket, then delete the bootstrap stack.
3. **GitHub:** delete the plan and apply environments.
