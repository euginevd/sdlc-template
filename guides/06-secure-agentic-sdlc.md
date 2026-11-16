# The secure agentic SDLC

The template's lifecycle in six stages, with the security controls and gates in each. My map to build against; the agent's rules are in [AGENTS.md](../AGENTS.md), each control in [04-the-guardrails.md](04-the-guardrails.md).

Agile fixed waterfall's late feedback, DevOps automated slow releases and DevSecOps put security in every stage; this is the next step: agents plan, write, test and fix the code, every DevSecOps control stays, and people make the calls that matter.

## 1. Six stages, design first after intent

The stages follow Anthropic's [AI-native SDLC playbook](https://academy.claude.com/courses/ai-native-sdlc-playbook/introduction): Plan, Design, Build, Test, Deploy, Maintain. They replace my earlier six (Plan, Code, Build and test, Release, Deploy, Operate and monitor).

| Earlier | Now | What moved |
|---|---|---|
| Plan | 1 Plan | Shrinks to intent: the problem, why it matters, the constraints |
| (inside Plan) | 2 Design | Spec, threat model, security requirements and mockup get their own stage and gate |
| Code | 3 Build | The same work, in phases, with self-checks |
| Build and test | 4 Test | Continuous: checks run on every push, not once at the end |
| Release, Deploy | 5 Deploy | One stage with two gates: the merge, then the apply |
| Operate and monitor | 6 Maintain | Ends the loop: each finding becomes a new Plan item |

Why this shape is better for security:

1. **Design gets a gate before any code.** The threat model and security requirements were buried in Plan; a design flaw is cheapest to fix here.
2. **Intent and design split along ownership.** I own the why; the agent drafts the how, and I approve it.
3. **Test matches how agents work:** push, fail, fix the cause, push again, many times a phase.
4. **Maintain closes the loop on purpose.** An incident, CVE or cost gap turns into a TODO item and starts at Plan again.

Where I keep my own version over the playbook's:

1. **Deploy has two gates, not one.** A merge and an apply are different blast radii with different approvers, and GitHub enforces the apply.
2. **Plan has a sign-off.** Someone has to accept that a change is worth building and its risk is acceptable, even if that's only me.
3. **Test includes the running app.** Evals and unit tests run during the build; DAST needs `dev`, so it runs after the first apply.

## 2. The pattern in every stage

1. **The agent does the work, a control checks it, a person decides.** A stage without all three is a gap.
2. **Gate by blast radius.** Checks handle the routine; a merge needs review; a deploy needs an approval GitHub enforces.
3. **Approve before, not after.** A gate I see once the change is live is a report.
4. **One agent writes, subagents review, nothing agentic deploys.** The pipeline holds the AWS roles.
5. **The agent that wrote it can't approve it.** The second reviewer is never the agent or its account (AGENTS.md rule 12).
6. **Every stage leaves a record in Git or GitHub,** so the audit trail costs nothing extra.

Guardrails, weakest to strongest. Anything that matters must be enforced or limited, not just asked.

| Strength | Template | Playbook term | Can the agent get past it? |
|---|---|---|---|
| Asked | `AGENTS.md`, `docs/`, `known-mistakes.md` | `CLAUDE.md`, skills | Yes: a rule is advisory |
| Checked | `.claude/settings.json` deny rules, pre-push scan | Hooks | Partly: a reworded command or skipped hook |
| Enforced | Required checks, the `main` ruleset | Branch protection | Not through a PR |
| Limited | OIDC roles in the pipeline, no AWS keys on the machine | Sandbox, scoped tokens | Not from a PR: it has no access |
| Approved | Merge review, deploy reviewer | Human approval gates | Only while it works as me on GitHub |

## 3. The stages at a glance

| Stage | Agent does | Controls | Gate | Record |
|---|---|---|---|---|
| 1 Plan | Turns a TODO item into a feature, asks the questions that change the build | Data classification, cost check | I accept the item | `TODO.md`, `features.md` |
| 2 Design | Drafts spec, plan, threat model and mockup | STRIDE, ASVS level, cost estimate | **G1**: I approve the plan | `spec.md`, `plan-<name>.md`, `threat-model.md`, `decisions.md` |
| 3 Build | Codes each phase with tests, runs local checks | Subagent review, pre-push scan, deny rules | None: the checks decide | Commits |
| 4 Test | Fixes each failing check at its cause | Tests and coverage, SAST, SCA, IaC, secrets | None: required checks block | PR checks, security summary |
| 5 Deploy | Opens the PR, answers findings, merges when allowed | Ruleset, Terraform plan, cost comment, OIDC roles | **G2** merge; **G3/G4** apply | PR, approvals, plan and apply logs, SBOM |
| 6 Maintain | Reads alerts, checks cost, writes the next TODO item | Weekly rescans, Dependabot, budget alert, logs | **G5**: I check cost and alarms | Runs, alerts, `known-mistakes.md` |

G0, kickoff, sits before all six, once per project ([docs/kickoff.md](../docs/kickoff.md)).

## 4. Plan

**Goal:** decide what's worth building, and why, before anyone designs it.

1. **Input:** an item in [TODO.md](../TODO.md), from me, a Maintain finding or a known mistake.
2. **Agent:** adds it to `features.md` and asks the few questions that change what gets built, each with a recommendation (AGENTS.md rule 23).
3. **Security:** name the data it touches and its class; flag users, auth, endpoints, money or new AWS services early.
4. **Gate:** I accept the item and answer the questions. Production also asks before any new AWS service or cost (rule 22).
5. **Record:** `TODO.md` and `features.md` in Git; answers in `spec.md` and `decisions.md`.

From the playbook: its `intent.md` holds the problem, outcome, affected users and systems, constraints and open questions. A TODO item plus the agent's questions does the same job; a separate intent file is worth it only once intent comes from people outside the repo *(planned, if a team joins)*.

## 5. Design

**Goal:** settle requirements, architecture and risks before code, against written policy.

1. **Agent:** drafts `docs/plan-<name>.md` from the skeleton and updates `spec.md` (rule 14).
2. **Threat model:** for users, data, auth or endpoints, the data flow diagram and STRIDE risks, each with a control and a test (guardrails 1).
3. **Security requirements:** the spec's ASVS level, 1 for a prototype, 2 for production.
4. **Screens:** a mockup in `docs/mockups/<name>.html` with loading, empty and error states.
5. **Cost:** `costs.md` updated when the plan adds a service (guardrails 2).
6. **Gate G1:** I approve the plan, spec and mockup; no code before that, in either profile.
7. **Record:** the plan and threat model in the PR; accepted trade-offs in `decisions.md`.

From the playbook:

1. **Policy as skills.** Security, compliance and UX rules applied while the spec is written, not found in review. Mine live in `code-standards.md` and the threat model; turning the most-broken one into a skill is next *(planned)*.
2. **Plan mode.** The agent reads the code and proposes before it edits. Probe the plan: what could break, which step is riskiest, what was rejected.
3. **The plan test.** Iterate until someone who never saw the conversation could build from the plan alone.
4. **Risk-based approval.** Routine plans need one approval; higher-risk ones need a second person (production).

## 6. Build

**Goal:** turn the approved plan into code in small phases, each checked before it leaves the machine.

1. **Agent:** builds one phase at a time with tests, on one branch per session (rule 15).
2. **Self-check:** runs the changed app's tests, lint and type checks locally before every push (rules 8 to 10).
3. **Review:** a fresh subagent checks the diff against `code-standards.md`, the threat model's top risks and the mockup; the agent fixes what it blocks.
4. **Pre-push scan:** Gitleaks and Trivy block secrets, vulnerable packages and bad IaC (guardrails 3).
5. **Agent limits:** `.claude/settings.json` denies force-pushes, `--no-verify`, `terraform apply`, approving PRs, ruleset edits and `.env` reads (guardrails 5).
6. **Never:** change cloud resources, read secrets in production, skip a hook or weaken a check (rules 25, 26).
7. **Gate:** none. Production commits and pushes only when I ask.
8. **Record:** one commit per finished piece; `features.md` and `TODO.md` updated in the same change.

From the playbook:

1. **The context file stays short.** `AGENTS.md` is my `CLAUDE.md`, held to 1,750 words by CI.
2. **Same mistake twice, write it down.** That's `known-mistakes.md` (rule 31); better, turn it into a check.
3. **Parallel sessions need separate worktrees** and separate files; review capacity is the real limit.
4. **Hooks over habits.** A Claude Code `PreToolUse` hook that blocks edits to `infra/`, workflows or test files during a fix *(planned)*.

## 7. Test

**Goal:** prove the change works and is safe on every push, not once at the end.

1. **Tests and coverage:** pytest, ruff and pyright in CI; 80% coverage and abuse cases for production, 50% and main paths for a prototype (guardrails 9).
2. **Secrets, SCA and IaC:** Gitleaks, Trivy and Checkov on every PR, `main` and weekly (guardrails 6).
3. **SAST:** Semgrep and CodeQL (guardrails 7).
4. **Supply chain:** actions pinned by SHA, images by digest, packages a week old, an SBOM on `main` (guardrails 8).
5. **Agent loop:** the agent reads each failure, fixes the cause and pushes again; three failures of one check and production stops (rule 21).
6. **Gate:** none for a person. A failed required check blocks the merge.
7. **Record:** check runs and the security summary comment on the PR.

From the playbook:

1. **Give the agent a feedback loop.** One command per check, documented with what healthy output looks like.
2. **Bug fixes start with a failing test.** Commit it, confirm it fails for the right reason, then fix the code without touching the test.
3. **Evals guard the agent's config.** 20 to 50 real tasks rerun whenever `AGENTS.md`, settings or hooks change, and each incident becomes one. Not in the template yet (trade-offs 8) *(planned)*.
4. **Tamper resistance.** Checks run from a copy the agent can't edit, and a run that changes files outside its allowed paths fails.

Not in Test yet: DAST with OWASP ZAP after each apply to `dev`, unauthenticated then signed in (guardrails 10, 11) *(planned)*.

## 8. Deploy

**Goal:** get a checked change to `main`, then to AWS, with a person approving each step that can hurt.

**Merge (G2):**

1. **Agent:** opens the PR with a Security line, lists findings with `bash scripts/pr-findings.sh <pr>`, fixes critical and high at their cause, and answers the rest (rule 16).
2. **Ruleset:** every change goes through a PR with required checks; `main` can't be force-pushed or deleted (guardrails 12).
3. **Cost:** Infracost comments the monthly change on PRs touching `infra/aws/` (guardrails 14).
4. **Gate G2:** a prototype merges once checks pass; production needs a second reviewer after the last push (guardrails 13).

**Apply (G3, G4):**

1. **Pipeline only:** GitHub OIDC, no stored keys; a read-only role plans, a bounded deploy role applies the saved plan (guardrails 16).
2. **Gate G3:** the first apply to `dev`. A prototype applies unattended; production waits for the reviewer on `aws-dev-apply` (guardrails 17).
3. **Gate G4:** `prod`, production only, after the checklist's production rows and a second reviewer.
4. **Smoke test:** the main path on `dev` after the first apply (rule 18).
5. **Record:** PR, approvals, Terraform plan and apply logs, SBOM. Export what an audit needs, as GitHub drops logs after 90 days.

From the playbook:

1. **AI review on every PR.** The same passes on every PR (bugs, security, spec compliance), with severity ranked and nits capped. Findings inform; a person approves.
2. **A review policy file.** `REVIEW.md` says what counts as important and what to skip *(planned)*.
3. **Autonomy tiers by environment.** `dev` open, `prod` behind a named approver: the same split as my profiles.
4. **The agent acts up to the production gate but never passes it.** Here the agent can't deploy at all.
5. **Its own identity.** Agent actions logged under its own account, separate from mine (production, guardrails 5).
6. **Fail closed.** If the approval check errors, the release is denied.
7. **Rollback is the most rehearsed path.** One command, tested in `dev` *(planned)*.

## 9. Maintain

**Goal:** keep watching what shipped, and turn every finding into the next change.

1. **Rescans:** weekly `security` and `codeql` runs on `main`, and Dependabot alerts and PRs (guardrails 4, 20).
2. **Cost:** the AWS budget alert (guardrails 21); the day after a deploy, Cost Explorer against `costs.md`, where a 2x gap is a finding (rule 19).
3. **Logs:** API access logs and throttling, 30 days (guardrails 22).
4. **Gate G5:** I check the cost, and in production the alarms.
5. **The loop:** each finding becomes a TODO item, a known mistake, or a decision to accept the risk.
6. **Record:** workflow runs, alerts, `known-mistakes.md` and `decisions.md`.

From the playbook:

1. **Control bands.** A normal range around a metric (30-day mean and σ): 1σ logs, 2σ diagnoses read-only, 3σ acts only through a PR or a pre-approved runbook *(planned)*.
2. **No model in detection.** Tested code decides a breach; the agent only diagnoses.
3. **Each incident becomes an eval** once the fix ships, so it can't come back unnoticed.
4. **A confidence gate between stages.** A deterministic check or an adversarial reviewer decides whether work continues or escalates.

Not in Maintain yet: CloudTrail, GuardDuty and alarms (guardrails 23, 24), and posture management such as Prowler *(planned)*.

## 10. What to measure

Outcomes, not lines of code. If throughput and the change failure rate rise together, tighten the checks first.

| Stage | Leading | Lagging |
|---|---|---|
| Plan | Time from idea to accepted item | Items dropped after design |
| Design | Time from item to approved plan | Spec changes after code starts |
| Build | Merged on the first pass | Repeat entries in `known-mistakes.md` |
| Test | First-pass CI success | Findings after merge versus before |
| Deploy | Time to first review, time waiting at each gate | DORA: lead time, deploy frequency, change failure rate, time to restore |
| Maintain | Time from alert to TODO item | Repeat incidents of the same class |

## 11. Next, in order

1. **The agent's own GitHub identity**, so the record separates its actions from mine and no one approves their own change.
2. **Claude Code hooks** for protected paths and test files, as the deterministic layer under `AGENTS.md`.
3. **Evals in CI** for changes to `AGENTS.md`, settings and hooks, plus one per incident.
4. **DAST** with ZAP after each `dev` apply.
5. **`REVIEW.md`** and AI review on every PR.
6. **Signed images and provenance** ([SLSA](https://slsa.dev)), so what runs is provably what was checked.
7. **Monitoring:** CloudTrail, GuardDuty and alarms, then control bands that write the next TODO item.
