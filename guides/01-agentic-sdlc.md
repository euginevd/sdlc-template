# Secure agentic SDLC

## 1. Overview

**The secure agentic SDLC is the software development lifecycle with AI coding agents as developers and security built into every stage.**

- **People** own the what and the why: the spec, the plan approval and the deploy approval. You're accountable for what ships, so anything that should last goes in a doc, not chat, and the agent shows evidence before you approve.
- **Agents** own the how: they plan, write, test and review the code, inside written rules.
- **Controls** check every change before it ships: the pre-push scan, CI checks, an independent review and an approval gate.

## 2. Where the name comes from

**Agentic software development** is the industry's emerging term (Forrester's *Agentic Software Development*, Gartner's *agentic engineering*); there's no single standard yet. This lifecycle is the **secure agentic SDLC**: keeping "SDLC" says existing security controls still apply. It draws on AWS's [AI-DLC](https://builder.aws.com/content/3KjWpM4sqd5f0zjUtE67OfUa7rk/ai-driven-development-life-cycle-ai-dlc-on-aws-a-new-approach-to-software-engineering) (AI plans, people approve), spec-driven development (GitHub Spec Kit), [AGENTS.md](https://agents.md), DevSecOps, and the NIST Secure Software Development Framework (SSDF, SP 800-218).

> **Note:** avoid the term ADLC. It's used both for this and for building AI agents as a product (the Agent Development Lifecycle).

## 3. The stages

The eight DevSecOps stages, the core security activities in each, and the open-source tools most teams reach for.

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

This template already runs Gitleaks and Trivy in the pre-push scan; the README's Lifecycle table shows who does what at each stage. Admission control, Argo CD, Kyverno and Trivy Operator apply once a project runs on Kubernetes.

## 4. The template repo

New projects start from [euginevd/sdlc-template](https://github.com/euginevd/sdlc-template): `gh repo create <project> --template euginevd/sdlc-template --private --clone`.

```
sdlc-template/
├── AGENTS.md              the agent's entry point
├── README.md              front page for people
├── apps/                  one folder per app: web, API, agent
├── aws/
│   ├── _template/         starting files for a new Terraform unit
│   └── bootstrap/         CloudFormation: OIDC, state bucket, pipeline roles
├── docs/                  what the agent builds from
│   ├── SPEC.md            what and why
│   ├── TECH_STACK.md      tools, checks, deploy
│   ├── CODE_STANDARDS.md  how to write the code
│   ├── PROCESS.md         plan, build, review, ship
│   ├── STATUS.md          what's built and what's next
│   └── DECISIONS.md       what's settled and why
├── guides/                reference for people, numbered 01, 02, …
├── scripts/               one-time setup and the security scan
├── .github/workflows/     aws.yml: plan on PR, apply after approval
├── .lefthook/             the pre-push hook
└── lefthook.yml           runs the scan on every push
```
