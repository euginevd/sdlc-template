# Secure agentic SDLC

## 1. Overview

**The secure agentic SDLC is the software development lifecycle with AI coding agents as developers and security built into every stage.**

- **People** own the what and the why: the spec, the plan approval and the deploy approval. You're accountable for what ships, so anything that should last goes in a doc, not chat, and the agent shows evidence before you approve.
- **Agents** own the how: they plan, write, test and review the code, inside written rules.
- **Controls** check every change before it ships: the pre-push scan, CI checks, an independent review and an approval gate.

## 2. Where the name comes from

**Agentic software development** is the industry's emerging term (Forrester's *ASD*, Gartner's *agentic engineering*); there's no single standard yet. This lifecycle is the **secure agentic SDLC**: keeping "SDLC" says existing security controls still apply. It draws on AWS's [AI-DLC](https://builder.aws.com/content/3KjWpM4sqd5f0zjUtE67OfUa7rk/ai-driven-development-life-cycle-ai-dlc-on-aws-a-new-approach-to-software-engineering) (AI plans, people approve), spec-driven development (GitHub Spec Kit), [AGENTS.md](https://agents.md), DevSecOps, and the NIST Secure Software Development Framework (SSDF, SP 800-218; section 3).

> **Note:** not to be confused with ADLC, which can also mean building AI agents as a product (the Agent Development Lifecycle).

## 3. The stages

The eight DevSecOps stages, with the AWS AI-DLC phase and the SSDF practices each one meets. Every stage ends at a gate.

| # | Stage | AI-DLC phase | NIST SSDF | Gate |
|:-:|-------|--------------|-----------|------|
| 1 | Plan | Inception | PO.1, PO.2, PW.1, PW.2 | You approve the plan |
| 2 | Code | Construction | PW.5, PS.1 | Pre-push scan |
| 3 | Build | Construction | PO.3, PW.4, PW.6 | CI checks |
| 4 | Test | Construction | PW.7, PW.8 | Fresh-subagent review and tests |
| 5 | Release | Operations | PO.4, PS.2 | Checks pass, PR merged |
| 6 | Deploy | Operations | PO.5, PW.9 | You approve the apply |
| 7 | Operate | Operations | PS.3, RV.1 | Fix within SLA |
| 8 | Monitor | Operations | RV.2, RV.3 | Lessons feed the next Plan |

SSDF groups: PO prepare the organisation, PS protect the software, PW produce well-secured software, RV respond to vulnerabilities. For IRAP, map the same evidence to ISM controls in the project's SSP.

Each stage below says what you do, what you need to know, and what to add when the app is itself an AI agent.

### 3.1 Plan

**You do**
- Write `docs/SPEC.md`: the problem, the goal, success criteria and what's out.
- Classify the data and note what applies: the Privacy Act, APRA CPS 234 and CPS 230 if regulated, IRAP if government.
- Ask: *"Please plan <the work> in docs/PLAN_<NAME>.md"*. Read the design, risks and phases, then approve or redirect. This is the cheapest place to catch a mistake.

**Know**
- Spec-driven development: spec → plan → tasks → progress. The agent writes no code until you approve.
- Threat model with STRIDE: map the data flows and trust boundaries, then turn each threat into a control with an owner and the stage that enforces it. It lives in `docs/SECURITY.md`.
- Least privilege and secure defaults are designed here, not added later. If a rule can't be tested, it isn't a rule.

**Agent app:** add the OWASP Top 10 for LLM and Agentic Applications (prompt injection, excessive agency, poisoning). The model decides, but deterministic code acts: limits live in the API, not the prompt. Design the kill switch now.

### 3.2 Code

**You do**
- Ask: *"Please implement the plan for <the work>"*. Read each phase's report and diff.
- Keep secrets in `.env` locally and in GitHub or AWS Secrets Manager, never in code.

**Know**
- The pre-push scan (gitleaks, Trivy) blocks secrets, misconfigurations and vulnerable packages before they leave your machine ([02-git-hooks.md](02-git-hooks.md)). A secret that's pushed must be rotated.
- SAST, SCA and IaC scanning run on every PR *(planned)*. A `main` ruleset makes them required checks *(planned)*.

**Agent app:** prompts and agent config are code. Version them in the repo, with CODEOWNERS on those paths.

### 3.3 Build

**You do**
- Pin dependencies exactly and commit the lock files.

**Know**
- The pipeline holds the keys to production, so secure it like production: actions pinned to a commit SHA, OIDC to AWS with no access keys, least-privilege tokens.
- Once there's a container: a hardened base image, an image scan that fails on critical CVEs, an SBOM, and a signed image.

**Agent app:** record an AI-BOM: the models, prompts, agent config and MCP servers.

### 3.4 Test

**You do**
- Read the fresh-subagent review and what the agent changed because of it.
- Ask for evidence: the test run, the diff, a screenshot.

**Know**
- Tests use stubs for models, cloud and paid services.
- Turn the threat model's abuse cases into regression tests, such as one customer can't read another's data.
- Once there's an API: DAST (OWASP ZAP) against staging, and a pen test before go-live.

**Agent app:** test the behaviour, not just the config. Prompt injection, tool misuse and data leakage tests (promptfoo, PyRIT or Garak) run in CI on every prompt, model or config change. A prompt change is a code change. Evals catch drift.

### 3.5 Release

**You do**
- Nothing routine: the agent opens the PR, merges once checks pass and deletes the branch.
- Approve any exception, time-boxed, and record it in `docs/DECISIONS.md`.

**Know**
- Ship exactly what you tested: promote images by digest, not tag, and re-scan them in the registry, since new CVEs land after the build.
- The Terraform plan saved on the PR is the one that's applied.

### 3.6 Deploy

**You do**
- Read the Terraform plan in the job summary, then approve or reject the apply in the `aws-<target>-apply` environment.

**Know**
- Git is the only way in: no person or agent changes the cloud directly.
- The deploy role is least privilege, and every role it creates has the permissions boundary.
- Secrets come from Secrets Manager at runtime.

**Agent app:** one identity per agent, scoped to the models and data it needs. Private endpoints to Bedrock, and an egress allow-list for its tool calls.

### 3.7 Operate

**You do**
- Patch within the Essential Eight timeframes: 48 hours when an exploit exists for an internet-facing system.
- Rotate keys, review access, and track costs in `docs/FINOPS.md`.

**Know**
- Posture management watches for misconfiguration and drift; vulnerability scanning covers running workloads.
- Every fix goes back through the pipeline. Hot patches quietly undo your gates.

**Agent app:** check that guardrails are attached, model access is limited to approved model IDs, and no shadow AI has appeared.

### 3.8 Monitor

**You do**
- Watch the alerts. Record surprises in [03-findings.md](03-findings.md), and decisions in `docs/DECISIONS.md`.
- Turn each incident into a new test, rule or threat-model entry, then update `docs/STATUS.md` and delete the finished plan.

**Know**
- Centralise CloudTrail and app logs, and turn on threat detection (GuardDuty).
- Rehearse the response: the NDB scheme gives 30 days to assess a suspected breach, and CPS 234 requires telling APRA within 72 hours of a material incident.

**Agent app:** watch the agent's decisions, not just the infrastructure: guardrail triggers, unexpected tool calls, unusual payouts and cost spikes. The kill switch is a feature flag in your app: security tools can kill a process, but only your app can stop the payments.

---

## 4. Reference

### 4.1 Layout and what to change in a new project

The repo's shape (one repo per product, one workflow per folder, one Terraform state per unit) is set out in `AGENTS.md` → Repo layout.

| Path | For | In a new project |
|------|-----|------------------|
| `AGENTS.md` | The agent's entry point | Rewrite Context; keep the rest |
| `docs/CODE_STANDARDS.md`, `docs/PROCESS.md` | How to write code; what happens at each stage | As-is |
| `docs/SPEC.md`, `TECH_STACK.md`, `STATUS.md` | What and why; tools and deploy; current state | Fill in under the headings |
| `docs/DECISIONS.md` | Decision log; never deleted, only superseded | Keep the template's entries, add your own |
| `apps/` | The apps | One folder per app |
| `aws/` | Terraform units, `_template/`, `bootstrap/` | Copy `_template/` per unit |
| `.github/workflows/aws.yml` | Plan and apply | As-is |
| `lefthook.yml`, `.lefthook/`, `scripts/` | Pre-push scan and setup | As-is |
| `guides/` | Reference for people, numbered `<NN>-<topic>.md` | Add per project |
| `local/` | Personal scratch | Gitignored |

### 4.2 Rules of thumb for docs

- Each fact lives in one place; everywhere else links to it.
- Keep docs short: tables and one-line rules.
- Write what's true now. Mark future work *(planned)*.
