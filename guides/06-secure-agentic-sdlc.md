# The secure agentic SDLC

The template's lifecycle on one page: six stages, the security controls in each and the gate that ends it. Agile fixed waterfall's late feedback, DevOps automated slow releases and DevSecOps put security in every stage; this is the next step: agents plan, write, test and fix the code, every DevSecOps control stays, and people make the calls that matter. The stages follow Anthropic's [AI-native SDLC playbook](https://academy.claude.com/courses/ai-native-sdlc-playbook/introduction); the rules are in [AGENTS.md](../AGENTS.md) and each control in [04-the-guardrails.md](04-the-guardrails.md).

| Stage | What happens | Security controls | Gate |
|---|---|---|---|
| 1. Plan | The top line of `TODO.md`, from the project brief, becomes a feature; the agent asks the questions that change the build | Data classified; new AWS services and cost flagged | I accept the item |
| 2. Design | The agent drafts the spec, plan, threat model and mockup | STRIDE threat model, ASVS level, cost estimate | **G1**: I approve before any code |
| 3. Build | The agent codes each phase with tests on one branch; a fresh subagent reviews it with the review skills and the verifier runs it | Pre-push scan (Gitleaks, Trivy), agent deny rules, no secrets or cloud access | None: the checks decide |
| 4. Test | Every push runs the checks; the agent fixes each failure at its cause | Tests and coverage, Semgrep, CodeQL, Trivy, Checkov, pinned supply chain | None: a failed check blocks the merge |
| 5. Deploy | The agent opens the PR; the pipeline plans and applies Terraform | Protected `main`, security summary, cost comment, OIDC roles, read-only plan | **G2** merge, **G3** `dev`, **G4** `prod` |
| 6. Maintain | Rescans and alerts find what changed; each finding becomes a new TODO line | Weekly rescans, Dependabot, budget alert, access logs | **G5**: I check cost and alarms the day after |

G0, kickoff, comes once before all six ([docs/kickoff.md](../docs/kickoff.md)). Who approves each gate in each profile is the table in AGENTS.md rule 5.

## The rules behind the gates

1. **The agent works, a control checks, a person decides.** A stage missing one of the three is a gap.
2. **Gate by blast radius.** Checks handle the routine, a merge needs review, and a deploy needs an approval GitHub enforces.
3. **Approve before, not after.** A gate seen once the change is live is only a report.
4. **The agent never deploys or approves its own work.** The pipeline holds the AWS roles, and the second reviewer is never the agent's account.
5. **Enforce what matters.** A rule in `AGENTS.md` can be ignored; a required check, a ruleset or a missing permission can't.

## Next

Not in the template yet, in order: the agent's own GitHub identity, Claude Code hooks for protected paths, evals for the agent's config, DAST on `dev`, signed images, and monitoring with CloudTrail, GuardDuty and alarms.
