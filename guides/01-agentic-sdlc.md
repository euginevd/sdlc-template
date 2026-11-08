# Secure agentic SDLC

## 1. Overview

**The secure agentic SDLC is the software development lifecycle with AI coding agents as developers and security built into every stage.**

- **People** own the what and the why: the spec, the plan approval and the deploy approval. You're accountable for what ships, so anything that should last goes in a doc, not chat, and the agent shows evidence before you approve.
- **Agents** own the how: they plan, write, test and review the code, inside written rules.
- **Controls** check every change before it ships: the pre-push scan, CI checks, an independent review and an approval gate.

## 2. Where the name comes from

**Agentic software development** is the industry's emerging term (Forrester's *ASD*, Gartner's *agentic engineering*); there's no single standard yet. This lifecycle is the **secure agentic SDLC**: keeping "SDLC" says existing security controls still apply. It draws on AWS's [AI-DLC](https://builder.aws.com/content/3KjWpM4sqd5f0zjUtE67OfUa7rk/ai-driven-development-life-cycle-ai-dlc-on-aws-a-new-approach-to-software-engineering) (AI plans, people approve), spec-driven development (GitHub Spec Kit), [AGENTS.md](https://agents.md), DevSecOps, and the NIST Secure Software Development Framework (SSDF, SP 800-218).

> **Note:** not to be confused with ADLC, which can also mean building AI agents as a product (the Agent Development Lifecycle).

## 3. The stages

The eight DevSecOps stages and the core security activities in each.

| # | Stage | Core components |
|:-:|-------|-----------------|
| 1 | Plan | Threat modelling · security requirements and architecture |
| 2 | Code | Secrets detection · static analysis (SAST, SCA, IaC) · repo hardening and code review |
| 3 | Build | Image scanning and build gates · SBOM and signing · CI pipeline hardening |
| 4 | Test | DAST, API and pen testing · security regression tests · AI security testing |
| 5 | Release | Artifact re-scan and promotion by digest · infrastructure plan review · release approval |
| 6 | Deploy | Admission control · GitOps deployment · secure workload configuration |
| 7 | Operate | Posture management · vulnerability management · AI posture management |
| 8 | Monitor | Threat detection and logging · incident response · AI monitoring |
