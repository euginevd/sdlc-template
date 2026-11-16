---
name: review-security
description: Security review of the branch's diff against this repo's threat model, code standards and rules, before a PR or after each phase (AGENTS.md rule 10). Use when asked for a security review, or when the build reaches its review step. Reports findings; never edits code.
allowed-tools: Read, Grep, Glob, Bash(git diff*), Bash(git log*), Bash(git show*), Bash(git status*)
---

# Security review

Review what this branch changes, against the repo's own standards. You report; the agent that wrote the code fixes as `docs/pull-requests.md` 3 says, then runs this review again until nothing critical or high is left. Run in a fresh context, not the author's.

## Scope

1. The diff: `git diff origin/main...HEAD`, plus any uncommitted changes. Read each changed file around the change, not just the hunk.
2. The standards, read first: `docs/threat-model.md` (its risks and controls), `docs/code-standards.md` 6 to 10 and 17 to 20, `docs/spec.md`'s Rules, and AGENTS.md rules 14, 16 and 17.
3. The plan, if there is one (`docs/plan-<name>.md`): its Security risks section is what the change promised to control.

## Check

1. **Threat model:** each risk the change touches still has its control, and a new route, data store, outside service or model call has a risk row. A missing row is a finding.
2. **Access:** every new endpoint checks authorisation on the server and denies by default (code-standards 10); nothing is open because only our code calls it.
3. **Input and output:** input validated against a schema at the boundary, unknown fields rejected (9); each state-changing action emits an audit event (8); model output and uploads treated as untrusted and validated (18); limits and payments enforced in code, not a prompt (17).
4. **Secrets and data:** no secret, key or token in code, Terraform, logs, error messages, URLs or test data; no real personal or financial data in a public repo (rule 17); logs redact at the source (8).
5. **Failure:** security and payment checks fail closed (7); model calls have an explicit model ID, timeout, token limit and retry cap (19).
6. **Supply chain:** each new package is real, maintained, pinned and at least 7 days old (rule 16); new actions pinned by SHA, images by digest.
7. **Infrastructure:** IAM roles carry the project boundary, no wildcards beyond what the profile allows (AGENTS.md rule 4), nothing public that the spec doesn't make public.
8. **Tests:** each risk the change touches has a test; production adds the abuse cases in the threat model (code-standards 11).
9. **Known mistakes:** the area's entries in `docs/known-mistakes.md` aren't repeated.
10. **Scope:** every changed file is in the plan's Files list; anything else is a finding.

## Report

A list, most severe first; "No findings" if clean. Each finding:

- **Severity:** critical (exploitable now, or a secret exposed), high (a missing control on a real risk), medium (a weak control or missing test), low (hardening).
- **Where:** `path:line`.
- **What and why:** one line, citing the rule, standard or threat-model ID it breaks.
- **Fix:** one line, at the cause.

End with the threat-model rows to add or change, if any, and anything you couldn't check and why.
