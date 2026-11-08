<div align="center">

# travel-claims

**An AI agent decides routine travel insurance claims in minutes, so handlers spend their time only on claims that need judgement.**

![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-OIDC-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-Cloud-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)

[Claimants](#-claimants) · [Handlers](#️-handlers) · [Apps](#-apps)

</div>

> This is [sdlc-template](https://github.com/euginevd/sdlc-template), with `travel-claims` as its worked example. To start a project from it: [guides/01-agentic-sdlc.md](guides/01-agentic-sdlc.md), section 2.

## 🧳 Claimants

1. Sign in and start a claim: tell us what happened, then add your receipts (PDF, JPEG or PNG).
2. Track it on the claim page: **Submitted**, then **Approved**, **Declined** or **Referred** to a handler, then **Paid**.
3. Every decision shows its reasons and the policy wording it relies on. Not happy with it? Ask for a person to review it.

## 🗂️ Handlers

1. The queue shows what's waiting, decided today and paid this week.
2. Open a claim to see the claimant's story, the receipts and the agent's decision with its reasons.
3. Approve, decline or send it back. Claims the agent approves under $1,000 are paid automatically *(in `dev`; `prod` after the bank's sign-off)*; everything else waits for you.

## 📦 Apps

```mermaid
flowchart LR
  claimant([Claimant])
  handler([Handler])

  subgraph aws ["AWS account, ap-southeast-2"]
    cognito[Cognito sign-in]
    web["web<br/>S3 and CloudFront"]
    api["api<br/>Lambda, HTTP API"]
    agent["agent<br/>Lambda"]
    db[(Claims database)]
    bucket[(Receipt bucket)]
  end

  claude{{Claude on Bedrock}}
  bank[Bank API]

  claimant & handler --> cognito
  claimant & handler --> web
  web --> api
  api <--> agent
  agent --> claude
  api --> db
  api --> bucket
  api --> bank
```

<sub>Full data flow and trust boundaries: [threat-model.md](docs/threat-model.md).</sub>

| App | What | Runs on |
|-----|------|---------|
| `web` | Claimants submit and track claims; handlers review them | S3 and CloudFront |
| `api` | Claims, receipts, decisions and payments | Lambda behind an HTTP API |
| `agent` | Decides each claim against the policy wording | Lambda, Claude on Bedrock |

Developers: [AGENTS.md](AGENTS.md), then [docs/](docs/).
