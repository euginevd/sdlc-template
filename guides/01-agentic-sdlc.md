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

The eight DevSecOps stages, who does each, the core security activities, and the open-source tools most teams reach for.

| # | Stage | Who | Core components | Open-source tools |
|:-:|-------|-----|-----------------|-------------------|
| 1 | Plan | You, then agent | Data classification · threat modelling · security requirements and architecture | OWASP Threat Dragon |
| 2 | Code | Agent | Secrets detection · static analysis (SAST, SCA, IaC) · repo hardening and code review | Gitleaks · Semgrep |
| 3 | Build | Pipeline | Image scanning and build gates · SBOM and signing · CI pipeline hardening | Trivy · Cosign |
| 4 | Test | Agent and pipeline | DAST, API and pen testing · security regression tests · AI security testing | OWASP ZAP · promptfoo |
| 5 | Release | Agent | Artifact re-scan and promotion by digest · infrastructure plan review · release approval | Checkov · Trivy |
| 6 | Deploy | Pipeline, after your approval | Admission control · GitOps deployment · secure workload configuration | Argo CD · Kyverno |
| 7 | Operate | You | Posture management · vulnerability management · AI posture management | Prowler · Trivy Operator |
| 8 | Monitor | You and pipeline | Threat detection and logging · incident response · AI monitoring | Falco · Wazuh |

## 4. Workflow: spec-driven development

The end-to-end flow of a change, through the stages in section 3. This is **spec-driven development**: you write the spec, the agent plans and builds from it, and gates feed findings back to the agent until the change is clean.

```
PLAN       1  Create the repo from the template
           2  Review and update the spec docs
           3  Prompt: "Plan <the work> in docs/plan-<name>.md"
           4  Review, refine and approve the plan  ◄── not right yet: refine
                │
CODE       5  Prompt: "Implement the plan for <the work>"
           6  Agent codes, commits and pushes
                ├─ pre-push scan finds an issue ──► agent fixes, pushes again
                └─ agent opens a PR
                │
BUILD      7  PR checks, scans and reviews
& TEST          ├─ a finding ──► agent fixes, pushes to the PR
                └─ agent review + your review ──► you approve the merge
                │
RELEASE    8  Merge to main: Terraform plan runs
& DEPLOY        └─ you read the plan and approve ──► apply
                │
OPERATE    9  Agent updates status and decisions, deletes the plan
& MONITOR       └─ findings, alerts and lessons ──► next spec (back to 2)
```

**Plan**

1. **Create the repo:** `gh repo create <project> --template euginevd/sdlc-template --private --clone`, then `bash scripts/setup.sh` for the pre-push scan.
2. **Update the spec docs:** `docs/spec.md` (problem, goal, success criteria, what's out), `docs/tech-stack.md`, the Context section of `AGENTS.md`, and `docs/threat-model.md` and `docs/costs.md` if the project needs them. Keep `code-standards.md` and `process.md` as they are.
3. **Prompt the plan:** *"Plan <the work> in docs/plan-<name>.md"*. The agent writes the design, security risks and phases with checkbox criteria, and no code.
4. **Review the plan:** ask for changes until it's right, then approve it. This is the cheapest place to catch a mistake.

**Code**

5. **Prompt the build:** *"Implement the plan for <the work>"*.
6. **The agent writes the code**, one phase at a time: code, local checks, a fresh-subagent review, docs, and a local commit. It pushes only when the PR's phases are all done. The pre-push scan (Gitleaks, Trivy) blocks secrets, misconfigurations and vulnerable packages; the agent reads the findings, fixes them and pushes again. Then it opens one PR.

**Build and test**

7. **PR checks and reviews:** the workflows run the checks and the Terraform plan, and post findings on the PR. The agent fixes each finding on the same PR, and asks for your review only once everything passes. You review the diff and the plan, and approve the merge; the agent squash-merges and deletes the branch.

**Release and deploy**

8. **Deploy:** the merge to `main` runs the Terraform plan. You read it in the job summary and approve the apply; Terraform applies exactly that plan through OIDC.

**Operate and monitor**

9. **Close the loop:** the agent updates `status.md` and `decisions.md` and deletes the plan. Surprises go in `guides/03-findings.md`. Alerts, findings and lessons become the next spec.

### Cadence: how often you're asked

Many commits, few PRs, so you're interrupted only at the gates:

- **Commits:** one per phase, local only. These are the agent's checkpoints; you don't see them.
- **Pushes and PRs:** one PR per plan, or one per group of phases when the plan is big. The plan says which phases go in which PR.
- **Your reviews:** three per plan at most: approve the plan, approve each PR once its checks pass, approve the deploy.
- **Small follow-ups:** batched into the next PR, never a PR of their own.

## 5. The template repo

New projects start from [euginevd/sdlc-template](https://github.com/euginevd/sdlc-template): `gh repo create <project> --template euginevd/sdlc-template --private --clone`.

Listed in order of importance:

```
sdlc-template/
├── AGENTS.md              01 the agent's rules; every agent reads this first
├── README.md              02 front page: what it is, how to start, the lifecycle
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
