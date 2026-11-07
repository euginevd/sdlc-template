# Secure agentic SDLC

## 1. Overview

**The secure agentic SDLC is the software development lifecycle with AI coding agents as developers and security built into every stage.**

- **People** own the what and the why: the spec, the plan approval and the deploy approval.
- **Agents** own the how: they plan, write, test and review the code, inside written rules.
- **Controls** check every change before it ships: the pre-push scan, CI checks, an independent review and an approval gate.

## 2. Where the name comes from

**Agentic software development** is the industry's emerging name for building software with AI agents doing much of the work: Forrester's *Agentic Software Development (ASD)*, Gartner's *agentic engineering*. Variants such as *agentic SDLC* and *AI-native SDLC* grew out of use from about 2025; nobody coined them. Keeping "SDLC" in the name says existing security controls still apply.

### 2.1 No single standard yet

The template draws on these named methods and conventions:

| Name | What it is | Here |
|------|------------|------|
| [AI-DLC](https://builder.aws.com/content/3KjWpM4sqd5f0zjUtE67OfUa7rk/ai-driven-development-life-cycle-ai-dlc-on-aws-a-new-approach-to-software-engineering) | AWS's method (July 2025): AI plans and builds, people approve each step | The plan-then-approve loop |
| Spec-driven development | Spec first, then agents plan and build from it; GitHub Spec Kit | `docs/SPEC.md` and `docs/PLAN_<NAME>.md` |
| [AGENTS.md](https://agents.md) | Open, tool-agnostic agent instructions, under the Linux Foundation | `AGENTS.md` |
| DevSecOps | Security built into every stage of delivery | The eight stages in section 5 |
| NIST SSDF (SP 800-218) | The US secure software development framework | The stage mapping in section 6.1 |

### 2.2 The two meanings of ADLC

| | 1. Building *code with* agents | 2. Building *agents with* code |
|---|---|---|
| Stands for | AI-Driven or Agentic Development Lifecycle | Agent Development Lifecycle |
| The agent is | The developer, writing your software | The product you ship |
| Main concern | Accountability for its code: specs, plans, reviews, checks, approvals | Evaluations, observability and controls, because agents vary and drift |
| Who uses it | AWS (AI-DLC), GitHub Spec Kit (spec-driven development) | LangChain, Microsoft Foundry, [IBM](https://www.ibm.com/think/topics/agent-development-lifecycle-adlc), [Salesforce](https://architect.salesforce.com/fundamentals/agent-development-lifecycle) |

This guide is meaning 1. When an app in `apps/` is an AI agent, add meaning 2: evaluations in Test, drift and cost monitoring in Monitor.

### 2.3 Harness, Harden, Humans

What's settled and what isn't (Ed Donner, AI FDE course, 2026):

| Layer | What | Covers | State | In this template |
|-------|------|--------|-------|------------------|
| **Harness** | The agent | State and memory, skills and integrations, subagents | Mostly settled | `AGENTS.md`, `docs/`, the fresh-subagent review |
| **Harden** | The environment | Hooks, linters, CI/CD, sandboxes, tests and evaluations | Partly settled | Pre-push scan, checks, `aws.yml` |
| **Humans** | You | Named accountability, meaningful review, the end-to-end process | Mostly open | You approve plans and applies; the PR carries your name |

### 2.4 Terms to use and avoid

| Term | Use it for |
|------|------------|
| **Agentic software development** | The industry practice, with executives and analysts |
| **Secure agentic SDLC** | This lifecycle, with security, audit and IRAP reviewers |
| Spec-driven development, harness engineering | The practices inside it |
| AI-DLC | Only AWS's named method |
| ~~ADLC~~ | Avoid: two meanings (2.2) |
| ~~AI-SDLC~~ | Avoid in formal writing: also means the lifecycle of ML models |
| ~~Vibe coding~~ | Avoid: means not reading the code, the opposite of this guide |

## 3. Five habits that make it work

- **Context in files, not chat.** The agent knows only what `AGENTS.md` and `docs/` say; anything that should last goes in a doc.
- **Verify, don't trust.** Checks and an independent review catch what the author missed; never weaken a check to pass.
- **Small steps.** One phase, one diff, one review; stop and ask when unclear.
- **People hold the keys.** The agent never changes cloud resources or deploys without your approval.
- **Be the boss.** The PR carries your name, so never push slop; make the agent show evidence.

## 4. Where the agent finds its rules

The agent starts at `AGENTS.md`, which lists these docs in reading order. Each maps to an older document:

| Doc | Answers | Older equivalent |
|-----|---------|------------------|
| `docs/SPEC.md` | What are we building, and what does done mean? | PRD (product requirements) |
| `docs/TECH_STACK.md` | What tools, what checks, how does it deploy? | Architecture doc |
| `docs/CODE_STANDARDS.md` | How should the code be written? | CONTRIBUTING |
| `docs/PROCESS.md` | What happens at each stage? | Definition of done |
| `docs/STATUS.md` | What's built, and what's next? | Progress file; agents forget between sessions |
| `docs/DECISIONS.md` | What's settled, so it isn't reopened? | ADRs |

Other tools use other names (Spec Kit, Kiro), but the pattern is the same: **spec → plan → tasks → progress**. Claude Code, Codex, OpenCode, Copilot and Cursor all read `AGENTS.md`.

> **No `CLAUDE.md`.** Claude Code reads `AGENTS.md` natively from v2.1.277, and skips it if a `CLAUDE.md` exists. For Claude-only extras, add a `CLAUDE.md` starting with `@AGENTS.md`.

## 5. The stages

Eight DevSecOps stages, each with an owner and a security check (side by side in 6.1).

### 5.1 Plan

You write `docs/SPEC.md`, then ask: *"Please plan <the work> in docs/PLAN_<NAME>.md"*. The agent writes the design, security risks and phases with checkbox criteria, and no code. **You approve or redirect the plan**: the cheapest place to catch a mistake.

### 5.2 Code

Ask: *"Please implement the plan for <the work>"*. The agent builds one phase at a time and reports after each. Secrets stay in `.env` locally and in GitHub or AWS secrets, never in code.

### 5.3 Build and 5.4 Test

Per phase: run the checks (lint, types, tests, `terraform validate`), have a **fresh subagent** review the diff, fix what it blocks, update `docs/STATUS.md`, tick off the plan, commit.

### 5.5 Release

The agent pushes; the **pre-push scan** (gitleaks, Trivy) blocks secrets, misconfigurations and vulnerable packages first ([02-git-hooks.md](02-git-hooks.md)). It opens a PR, merges once checks pass and deletes the branch.

### 5.6 Deploy

The `aws` workflow plans changed Terraform units on the PR with a read-only role. After the merge, the apply waits for **your approval**, then applies exactly that plan. OIDC means no access keys.

### 5.7 Operate and 5.8 Monitor

After the last phase, the agent reviews the whole branch, updates `STATUS.md` and `DECISIONS.md`, and deletes the plan. Runbooks go in `guides/`, costs in `docs/FINOPS.md`, surprises in [03-findings.md](03-findings.md), and all of it feeds the next Plan.

---

## 6. Reference

### 6.1 Stages mapped to NIST SSDF

NIST SP 800-218 groups secure development into Prepare the Organization (PO), Protect the Software (PS), Produce Well-Secured Software (PW) and Respond to Vulnerabilities (RV).

| # | Stage | Who | SSDF practices | Evidence here |
|:-:|-------|-----|----------------|---------------|
| 1 | Plan | Person, then agent | PO.1 security requirements, PO.2 roles, PW.1 secure design, PW.2 design review | `SPEC.md` rules, threat model in `docs/SECURITY.md`, the person approves the plan |
| 2 | Code | Agent | PW.5 secure coding, PS.1 protect the code | `CODE_STANDARDS.md`, no secrets in code, changes reach `main` only by PR |
| 3 | Build | Pipeline | PO.3 toolchains, PW.4 well-secured components, PW.6 build settings | Pinned dependencies and actions, lock files, checks |
| 4 | Test | Agent and pipeline | PW.7 code review and analysis, PW.8 testing | Fresh-subagent review, tests with stubs for models and cloud, pre-push scan |
| 5 | Release | Agent | PO.4 criteria for security checks, PS.2 release integrity | Checks before merge (required by a `main` ruleset *(planned)*), the plan artifact applied exactly |
| 6 | Deploy | Pipeline, after your approval | PO.5 secure environments, PW.9 secure defaults | OIDC, least-privilege roles, permissions boundary, approval gate |
| 7 | Operate | Person | PS.3 archive releases, RV.1 find vulnerabilities | Git history and versioned state, re-running the scans, patching and key rotation |
| 8 | Monitor | Person and pipeline | RV.2 remediate, RV.3 root causes | `03-findings.md`, `DECISIONS.md`, findings feed the next Plan |

For IRAP, map the same evidence to ISM controls in the project's SSP. For agents in `apps/`, add the OWASP GenAI Security Project's guidance on LLM and agentic application risks.

### 6.2 Layout and what to change in a new project

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

### 6.3 Rules of thumb for docs

- Each fact lives in one place; everywhere else links to it.
- Keep docs short: tables and one-line rules.
- Write what's true now. Mark future work *(planned)*.
