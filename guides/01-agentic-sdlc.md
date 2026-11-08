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

Listed in order of importance:

```
sdlc-template/
├── AGENTS.md              01 the agent's rules; every agent reads this first
├── README.md              02 front page: what it is, how to start, the lifecycle
├── docs/                  03 what the agent builds from, in reading order:
│   ├── SPEC.md               what we're building and what done means
│   ├── TECH_STACK.md         tools, checks and how it deploys
│   ├── CODE_STANDARDS.md     how to write the code
│   ├── PROCESS.md            how to plan, build, review and ship
│   ├── STATUS.md             what's built and what's next
│   └── DECISIONS.md          what's settled and why
├── apps/                  04 the product: one folder per app (web, API, agent)
├── aws/                   05 the infrastructure, as Terraform
│   ├── _template/            copy to aws/<unit>/ for each new unit
│   └── bootstrap/            CloudFormation, deployed once: OIDC, state bucket, pipeline roles
├── .github/workflows/     06 aws.yml: plan on the PR, apply after your approval
├── lefthook.yml           07 runs the security scan on every push
├── .lefthook/             08 the pre-push hook script
├── scripts/               09 setup.sh installs the tools; scan.sh runs gitleaks and Trivy
└── guides/                10 reference for people, numbered 01, 02, …
```
