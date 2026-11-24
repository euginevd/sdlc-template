# The secure agentic SDLC

The template's lifecycle on one page: six stages, the security controls in each and the gate that ends it. Agile fixed waterfall's late feedback, DevOps automated slow releases and DevSecOps put security in every stage; this is the next step: agents plan, write, test and fix the code, every DevSecOps control stays, and people make the calls that matter. The stages follow Anthropic's [AI-native SDLC playbook](https://academy.claude.com/courses/ai-native-sdlc-playbook/introduction); the rules are in [AGENTS.md](../AGENTS.md) and each control in [04-the-guardrails.md](04-the-guardrails.md).

| Stage | What happens | Security controls | Gate |
|---|---|---|---|
| 1. Plan | The oldest open GitHub issue, an intent like `intent.md`, becomes a feature; the agent asks the questions that change the build | Data classified; new AWS services and cost flagged | I accept the item |
| 2. Design | The agent drafts the spec, plan, threat model and mockup | STRIDE threat model, ASVS level, cost estimate | **G1**: I approve before any code |
| 3. Build | The agent codes each phase with tests on one branch; a fresh subagent reviews it with the review skills and the verifier runs it | Pre-push scan (Gitleaks, Trivy), agent deny rules and the Stop hook's checks, no secrets or cloud access | None: the checks decide |
| 4. Test | Every push runs the checks; the agent fixes each failure at its cause | Tests and coverage, Semgrep, CodeQL, Trivy, Checkov, pinned supply chain | None: a failed check blocks the merge |
| 5. Deploy | The agent opens the PR; the pipeline plans and applies Terraform | Protected `main`, security summary, cost comment, OIDC roles, read-only plan | **G2** merge, **G3** `dev`, **G4** `prod` |
| 6. Maintain | Rescans and alerts find what changed; each finding becomes a new issue | Weekly rescans, Dependabot, budget alert, access logs | **G5**: I check cost and alarms the day after |

G0, kickoff, comes once before all six (the [`kickoff`](../.claude/skills/kickoff/SKILL.md) skill). Who approves each gate in each profile is the table in AGENTS.md rule 5.

## Where each doc fits

[AGENTS.md](../AGENTS.md) runs every stage; the rest belong to one.

| Stage | Docs | Checklist controls |
|---|---|---|
| Plan | [intent](../docs/intent.md), GitHub issues; the `kickoff` skill once | None |
| Design | [spec](../docs/spec.md), [threat-model](../docs/threat-model.md), [costs](../docs/aws/costs.md), [design-system](../docs/web/design-system.md), [plan template](../docs/templates/plan.md), [decisions](../docs/decisions.md), [trade-offs](03-security-trade-offs.md) | 1–2 |
| Build | [standards](../docs/standards.md), [lessons](../docs/lessons.md) | 3–5 |
| Test | [`scripts/check.sh`](../scripts/check.sh) and the CI workflows | 6–11 |
| Deploy | the `pull-request` and `deploy` skills, [checklist](../docs/checklist.md) before `prod` | 12–19 |
| Maintain | [features](../docs/features.md), what's built; [AWS cleanup](05-aws-cleanup.md) when a project ends | 20–24 |

For auditors: the eight DevSecOps stages map onto these six. Plan stays Plan (its threat model and cost here sit in Design), Code joins Build, the CI scans join Test, Release joins Deploy, and Operate and Monitor become Maintain.

## The rules behind the gates

1. **The agent works, a control checks, a person decides.** A stage missing one of the three is a gap.
2. **Gate by blast radius.** Checks handle the routine, a merge needs review, and a deploy needs an approval GitHub enforces.
3. **Approve before, not after.** A gate seen once the change is live is only a report.
4. **The agent never deploys or approves its own work.** The pipeline holds the AWS roles, and the second reviewer is never the agent's account.
5. **Enforce what matters.** A rule in `AGENTS.md` can be ignored; a required check, a ruleset or a missing permission can't.

## Next

Not in the template yet: the template's [issues labelled `template`](https://github.com/euginevd/sdlc-template/issues?q=is%3Aissue+is%3Aopen+label%3Atemplate), in priority order. Among them: hooks that stop an agent weakening checks, tests or `.env`, the agent's own GitHub identity, evals, DAST on `dev`, signed images, and monitoring with CloudTrail, GuardDuty and alarms.
