# Secure agentic SDLC

## 1. Overview

**The secure agentic SDLC is the software development lifecycle with AI coding agents as developers and security built into every stage.**

- **People** own the what and the why: the spec, and approving the plan, the merge and the deploy. You're accountable for what ships, so anything that should last goes in a doc, not chat, and the agent shows evidence before you approve.
- **Agents** own the how: they plan, write, test and review the code, inside written rules.
- **Controls** check every change before it ships: the pre-push scan, an independent review, the Terraform checks in CI and an approval gate.

## 2. Where the name comes from

**Agentic software development** is the industry's emerging term (Forrester's *Agentic Software Development*, Gartner's *agentic engineering*); there's no single standard yet. This lifecycle is the **secure agentic SDLC**: keeping "SDLC" says existing security controls still apply. It draws on AWS's [AI-DLC](https://builder.aws.com/content/3KjWpM4sqd5f0zjUtE67OfUa7rk/ai-driven-development-life-cycle-ai-dlc-on-aws-a-new-approach-to-software-engineering) (AI plans, people approve), spec-driven development (GitHub Spec Kit), [AGENTS.md](https://agents.md), DevSecOps, and the NIST Secure Software Development Framework (SSDF, SP 800-218).

> **Note:** avoid the term ADLC. It's used both for this and for building AI agents as a product (the Agent Development Lifecycle).

## 3. The stages

The eight DevSecOps stages, the core security activities in each, and the open-source tools most teams reach for. Who does what is in the workflow (section 4).

| # | Stage | Core components | Open-source tools |
|:-:|-------|-----------------|-------------------|
| 1 | Plan | Data classification · threat modelling · security requirements and architecture | OWASP Threat Dragon |
| 2 | Code | Secrets detection · static analysis (SAST, SCA, IaC) · repo hardening and code review | Gitleaks · Semgrep |
| 3 | Build | Image scanning and build gates · SBOM and signing · CI pipeline hardening | Trivy · Cosign |
| 4 | Test | DAST, API and pen testing · security regression tests · AI security testing | OWASP ZAP · promptfoo |
| 5 | Release | Artifact re-scan and promotion by digest · infrastructure plan review · release approval | Checkov · Trivy |
| 6 | Deploy | Admission control · GitOps deployment · secure workload configuration | Argo CD · Kyverno |
| 7 | Operate | Posture management · vulnerability management · AI posture management | Prowler · Trivy Operator |
| 8 | Monitor | Threat detection and logging · incident response · AI monitoring | Falco · Wazuh |

## 4. Workflow: spec-driven development

The end-to-end flow, stage by stage, for both a new project and each change after it: **a new project starts at step 1; every later change, such as a feature or a fix, starts at step 2.** You write the spec, the agent plans and builds from it, and every gate feeds findings back to the agent (↺) until the work is clean.

| # | Stage | Step | Who |
|:-:|-------|------|-----|
| 1 | Plan | You |
| 2 | Plan | You |
| 3 | Plan | You, then agent |
| 4 | Plan | You |
| 5 | Code | You |
| 6 | Code | Agent |
| 7 | Code | Agent |
| 8 | Build and test | **PR checks:** the workflows run the checks and the Terraform plan (app checks *(planned)*). ↺ The agent fixes any finding on the same PR | Pipeline, then agent |
| 9 | Release | **Review and merge:** you review the diff and the plan and approve; the agent squash-merges and deletes the branch | You, then agent |
| 10 | Deploy | **Apply:** you read the Terraform plan and approve; Terraform applies exactly that plan through OIDC | You, then pipeline |
| 11 | Operate and monitor | **Close the loop:** the agent updates `status.md` and `decisions.md` and deletes the plan; findings and alerts become the next spec (back to 2) | Agent and you |

## 5. The template repo

What step 1 creates from [euginevd/sdlc-template](https://github.com/euginevd/sdlc-template), in order of importance:

```
sdlc-template/
├── AGENTS.md              01 the agent's rules; every agent reads this first
├── README.md              02 front page: what it is and how to start
├── docs/                  03 what the agent builds from, in reading order:
│   ├── spec.md               what we're building and what done means
│   ├── tech-stack.md         tools, checks and how it deploys
│   ├── code-standards.md     how to write the code
│   ├── process.md            how to plan, build, review and ship
│   ├── status.md             what's built and what's next
│   ├── decisions.md          what's settled and why
│   ├── threat-model.md       data classification, threats and controls
│   └── costs.md              what costs money, budget and alerts
├── apps/                  04 the product: one folder per app (web, API, agent)
├── aws/                   05 the infrastructure, as Terraform
│   ├── bootstrap/            CloudFormation, deployed once: OIDC, state bucket, pipeline roles
│   ├── iam/                  sample: app role with the permissions boundary
│   ├── storage/              sample: private, encrypted S3 bucket
│   └── api/                  sample: Lambda behind an HTTP API, with logs
├── .github/workflows/     06 aws.yml: plan on the PR, apply after your approval
├── lefthook.yml           07 runs the security scan on every push
├── .lefthook/             08 the pre-push hook script
├── scripts/               09 setup.sh installs the tools; scan.sh runs Gitleaks and Trivy;
│                             protect-main.sh adds the main ruleset
├── guides/                10 reference for people, numbered 01, 02, …
└── SECURITY.md            11 how to report a vulnerability (GitHub's policy file)
```
