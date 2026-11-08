# travel-claims

An AI agent decides routine travel insurance claims in minutes, so handlers spend their time only on claims that need judgement.

> This is [sdlc-template](https://github.com/euginevd/sdlc-template), with `travel-claims` as its worked example. To start a project from it: [guides/01-agentic-sdlc.md](guides/01-agentic-sdlc.md), section 2.

## 📦 Apps

| App | What | Runs on |
|-----|------|---------|
| `web` | Claimants submit and track claims; handlers review them | S3 and CloudFront |
| `api` | Claims, receipts, decisions and payments | Lambda behind an HTTP API |
| `agent` | Decides each claim against the policy wording | Lambda, Claude on Bedrock |

## 📚 Docs

Agent rules in [AGENTS.md](AGENTS.md); the project in [docs/](docs/), starting with [spec.md](docs/spec.md) and [status.md](docs/status.md); AWS bootstrap, deploys and cleanup in [guides/03-aws-setup.md](guides/03-aws-setup.md); accepted risks in [guides/02-security-trade-offs.md](guides/02-security-trade-offs.md).
