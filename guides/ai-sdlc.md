# AI-SDLC: building with coding agents

How projects from this template are built, with coding agents doing most of the coding and security built into every stage. It starts with the idea, then walks through each stage, and ends with reference tables.

## 1. The idea in one line

**The person owns *what* and *why*. The agent owns *how*, inside written rules.**

You decide what to build and approve each plan. The agent plans, codes, tests and reviews. Rules in files, checks and approvals keep the agent safe.

## 2. Four habits that make it work

Everything else in this guide builds on these.

- **Context in files, not chat.** The agent knows only what `AGENTS.md` and `docs/` tell it. Anything said in chat that should last goes in a doc.
- **Verify, don't trust.** Checks and an independent review catch what the author missed. Never weaken a check to get a green run.
- **Small steps.** One phase, one diff, one review. Stop and ask when stuck or unclear.
- **People hold the keys.** The agent never changes cloud resources, and never deploys without your approval.

## 3. Where the agent finds its rules

The agent starts at `AGENTS.md`, which lists the docs to read in order:

| Doc | Answers |
|-----|---------|
| `docs/SPEC.md` | What are we building, and what does done mean? |
| `docs/TECH_STACK.md` | What tools, what checks, how does it deploy? |
| `docs/CODE_STANDARDS.md` | How should the code be written? |
| `docs/PROCESS.md` | What happens at each stage? |
| `docs/STATUS.md` | What's built, and what's next? |
| `docs/DECISIONS.md` | What's settled, so it isn't reopened? |

The same files work for any coding agent, because they're plain Markdown. That's why there's only `AGENTS.md`, with no tool-specific copies.

## 4. The stages

Work moves through the eight DevSecOps stages. Each one has an owner, an output and its own security check.

### 4.1 Plan

You write `docs/SPEC.md`: the problem, the goal, success criteria and what's out. Then ask the agent: *"Please plan <the work> in docs/PLAN_<NAME>.md"*.

The agent writes the design, the security risks and the phases, each with checkbox criteria. It writes no code. **You review the plan** and approve or redirect it. This is the cheapest place to catch a mistake.

### 4.2 Code

Ask: *"Please implement the plan for <the work>"*. The agent builds one phase at a time, to the code standards. Secrets never go in code; they live in `.env` locally and in GitHub or AWS secrets otherwise.

### 4.3 Build and 4.4 Test

For each phase the agent runs the checks (lint, types, tests, `terraform validate`), then hands the diff to a **fresh subagent** that didn't write it, as a strict reviewer. It fixes what the review blocks on, updates `docs/STATUS.md`, ticks off the plan and commits.

### 4.5 Release

The agent pushes the branch. The **pre-push scan** (gitleaks and Trivy) checks it for secrets, misconfigurations and vulnerable packages before it leaves your machine: [git-hooks.md](git-hooks.md). Then it opens a PR, and merges once every check passes.

### 4.6 Deploy

The `aws` workflow plans each changed Terraform unit on the PR, with a read-only role. After the merge, the apply waits for **your approval** in the `aws-<target>-apply` environment, then applies exactly the reviewed plan. GitHub reaches AWS through OIDC, so there are no access keys to leak.

### 4.7 Operate and 4.8 Monitor

When the plan's last phase is done, the agent reviews the whole branch, then updates `docs/STATUS.md` and `docs/DECISIONS.md` and deletes the plan. Anything surprising goes in [findings.md](findings.md). What you learn here feeds the next Plan.

## 5. A day with the agent

1. Write or update `docs/SPEC.md`.
2. "Please plan the login page in `docs/PLAN_LOGIN.md`." Read the plan; ask for changes until it's right.
3. "Please implement the plan for the login page." The agent works phase by phase and reports after each.
4. The agent pushes, opens the PR and merges once checks pass.
5. Approve the apply in GitHub when the plan looks right.

---

## Reference

### Stages at a glance

| # | Stage | Who | Output | Security |
|:-:|-------|-----|--------|----------|
| 1 | Plan | Person, then agent | Spec, then `docs/PLAN_<NAME>.md` | Threat model in `docs/SECURITY.md` |
| 2 | Code | Agent | One phase at a time | No secrets in code |
| 3 | Build | Pipeline | Lint, types, `terraform validate` | Pinned dependencies |
| 4 | Test | Agent and pipeline | Tests, fresh-subagent review | Stubs for models and cloud |
| 5 | Release | Agent | PR merged, branch deleted | Pre-push scan; actions pinned to a SHA |
| 6 | Deploy | Pipeline | Plan on PR, apply after approval | OIDC, least-privilege roles |
| 7 | Operate | Person | Runbooks, `docs/FINOPS.md` | Patching, key rotation |
| 8 | Monitor | Person and pipeline | Status and decisions updated | Findings feed the next Plan |

### Layout and what to change in a new project

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
| `guides/` | Reference for people | Add per project |
| `local/` | Personal scratch | Gitignored |

### Repo shape

- One repo per product; a top-level folder per kind of deployable part (`apps/`, `aws/`).
- One workflow per folder, triggered by its path. Environments `<cloud>-<target>-plan` and `<cloud>-<target>-apply`; only `-apply` needs approval.
- One Terraform root and state per deployable unit. Plan on the PR; apply the reviewed plan.
- OIDC from CI to cloud, scoped to repo and environment. No access keys.
- Separate repos only when owners, access or release cycles differ.

### Rules of thumb for docs

- Each fact lives in one place; everywhere else links to it.
- Keep docs short: tables and one-line rules.
- Write what's true now. Mark future work *(planned)*.
