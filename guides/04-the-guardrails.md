# The guardrails

How each control in [docs/checklist.md](../docs/checklist.md) works, numbered to match; its tool and profile are in the checklist. The risks the template accepts instead are in [03-security-trade-offs.md](03-security-trade-offs.md).

Terms: SCA finds vulnerable packages; SAST finds flaws in your own code; DAST attacks the running app; IaC is Terraform and CloudFormation. The same scans run before a push and on the PR on purpose: the hook can be skipped, the required checks can't.

## 1. Design: threat modelling and security requirements

- **Does:** lists what a change touches, classifies the data and works through STRIDE, mapping each risk to OWASP. The spec sets ASVS level 1 for a prototype, 2 for production.
- **When:** at kickoff, and in each plan touching users, data, auth or endpoints.
- **On a finding:** each risk gets a control and a test; you approve before any code.
- **Limits:** only as good as the review. Each data class still needs its own encryption, backups and retention, set per project.

## 2. Design: cost estimate

- **Does:** estimates each environment's monthly cost by service, against a monthly limit.
- **When:** at kickoff, and whenever a plan adds a service or cost (AGENTS.md rule 4).
- **On a finding:** you approve the estimate or change the plan.
- **Limits:** an estimate, not a bill; data transfer and model tokens are hardest to predict.

## 3. Build, IDE: secrets, SCA and IaC scanning

- **Does:** Gitleaks finds secrets. Trivy finds vulnerable packages, insecure infrastructure settings and secrets.
- **When:** on every `git push`, over every pushed commit and its history; `setup.sh` installs the hook.
- **On a finding:** the push is blocked. Trivy blocks only fixable high and critical findings.
- **Limits:** it runs on your machine, so it can be skipped. Rotate any secret that gets past it.

## 4. Build, repo: push protection and SCA

- **Does:** GitHub rejects a push containing a known secret pattern, even when the hook was skipped. Dependabot alerts on vulnerable or malicious packages and opens grouped fix PRs.
- **When:** on every push; alerts as advisories publish, and weekly update PRs per ecosystem.
- **On a finding:** the push is rejected, or an alert appears with a fix PR.
- **Limits:** turn on malware alerts and grouped security updates by hand (Settings → Advanced Security). Generic passwords need paid Secret Protection; Gitleaks covers them. Turn on 2FA and personal push protection.

## 5. Build, agent: agent guardrails

- **Does:** `AGENTS.md` holds the rules every agent reads (rules 4 and 14: never touch secrets, cloud resources or hooks). `.claude/settings.json` enforces what Claude Code can: it denies force-pushes, `--no-verify`, `terraform apply` and `destroy`, and `.env` reads (a prototype drops the last at kickoff), and turns off AI attribution on commits and PRs (rule 15).
- **Hooks:** before each edit or command, `scripts/agent-guard.sh` denies touching `.env` in production, even through a shell command (a prototype may, by its profile), and asks you before an existing test or a check's own settings (ruff, ESLint, Prettier, tsconfig, TFLint, the hooks, the workflows, `check.sh`, `.claude/settings.json`) is edited, so the agent fixes the code rather than the test or the check.
- **When:** in every session; Claude Code's Stop hook also runs the quick checks whenever the agent ends a turn with uncommitted edits, and sends a failure back, once, for it to fix.
- **On a finding:** hooks and required checks catch a broken rule: the commit hook and the `rules` check fail on AI attribution, and on a numbered reference that points at the wrong item. Add a lesson to `docs/lessons.md`.
- **Limits:** deny rules match how a command starts, so a reworded command can slip past; other agents need their own settings (trade-offs 2). The only AWS key on the agent's machine is the read-only troubleshoot user's (trade-offs 14); while it works as you on GitHub, its actions look like yours (trade-offs 1).

## 6. Test: secrets, SCA and IaC scanning

- **Does:** the pre-push scans again, plus Checkov, `terraform fmt` and `validate`, and tflint for AWS mistakes `validate` can't see, such as an invalid instance type or a retired Lambda runtime.
- **When:** on every PR, on `main` and weekly, so a vulnerability published after a merge still fails a run.
- **On a finding:** a required check fails; findings are marked on the PR and listed by `bash scripts/pr-findings.sh <pr>`.
- **Limits:** scans files, not images; the `images` workflow scans each built image before it reaches ECR.

## 7. Test: SAST

- **Does:** Semgrep matches known bad patterns in seconds. CodeQL traces data across files to find injection and path traversal.
- **AI Scan and Copilot Autofix** (Settings → Advanced Security): AI Scan comments on PRs in languages CodeQL skips and looks for prompt injection in LLM code. Autofix suggests or opens a fix PR, which goes through the same checks; these use AI credits and don't block a merge.
- **When:** on every PR (Semgrep only new findings), on `main` and weekly; CodeQL skips docs-only PRs.
- **On a finding:** Semgrep fails a required check; CodeQL adds an alert on the PR's lines.
- **Limits:** CodeQL is free on public repos only (trade-offs 9).

## 8. Test: supply chain security

- **Does:** actions are pinned by commit and images by digest. Packages wait 7 days before use, unless a release fixes a named vulnerability (AGENTS.md rule 16). Trivy builds a CycloneDX SBOM from the lock files.
- **When:** pins and the wait on every install; the SBOM on every push to `main`.
- **On a finding:** nothing fails; these prevent. The SBOM is under the `main` run's Artifacts.
- **Limits:** the SBOM isn't signed and GitHub deletes it after 90 days; for production, keep it with a release or in S3. Signing, SLSA provenance and a licence policy aren't in the template yet.

## 9. Test: unit and abuse-case tests, coverage

- **Does:** production tests every change with abuse cases at 80% coverage. A prototype tests main paths and anything touching auth, money or personal data, at 50%.
- **When:** on every PR that changes an app, as a required check.
- **On a finding:** a failed test, or coverage under `fail_under`, blocks the merge.
- **Limits:** tests run the code, not the deployed app. AI evals aren't in CI yet (trade-offs 8).

## 10. Test: DAST, unauthenticated

- **Does:** passively scans the running app for missing headers, verbose errors, open redirects and bad CORS or TLS, in about a minute.
- **When:** after each apply to `dev`, in the `aws` workflow; ZAP's API scan once there's an OpenAPI spec.
- **On a finding:** high risks block the `prod` deploy; the rest go in the run summary.
- **Limits:** not in the template yet; add it before go-live. It sees only the public surface.

## 11. Test: DAST, authenticated

- **Does:** the same scan signed in, to find broken access control and session flaws.
- **When:** with 10, after each apply to `dev`.
- **On a finding:** as in 10.
- **Limits:** not in the template yet. Its test account lives in `dev` only, with credentials in an environment secret.

## 12. Deploy: branch protection

- **Does:** every change goes through a PR with required checks on an up-to-date branch, squash-only; `main` can't be force-pushed or deleted, even by an admin. The required checks include `plan-result`, so a failed Terraform plan blocks the merge; `kickoff`, so an unfinished kickoff does; and `workflows`, which lints workflows and scripts with actionlint, zizmor and shellcheck.
- **When:** on every push to `main` and every merge.
- **On a finding:** a direct push is rejected; merge stays disabled until checks pass.
- **Limits:** rulesets need a public repo or a paid plan.

## 13. Deploy: peer review

- **Does:** each PR needs one approval from someone other than its author, after the last push, with every thread resolved.
- **When:** on every PR to `main`.
- **On a finding:** the PR can't merge; a new push dismisses the approval.
- **Limits:** while the agent works as you, the reviewer must be another account. A prototype merges once checks pass.

## 14. Deploy: cost review

- **Does:** comments each PR's monthly estimate, its change and the top cost drivers.
- **When:** on every PR that changes `infra/aws/`.
- **On a finding:** warns above `MONTHLY_COST_LIMIT`, without blocking.
- **Limits:** needs the bootstrap and a free `INFRACOST_API_KEY`. It prices resources, not usage (trade-offs 10).

## 15. Deploy: AWS account baseline

- **Does:** root has MFA and no keys; people sign in through IAM Identity Center with short sessions. Production keeps `dev` and `prod` in separate accounts in one Organization.
- **When:** once per account, before the bootstrap.
- **On a finding:** IAM and Security Hub flag root without MFA or with keys.
- **Limits:** not in the template yet; the bootstrap assumes it.

## 16. Deploy: cloud identity and least privilege

- **Does:** only the pipeline touches AWS, through OIDC, with no stored keys. A read-only role plans; a deploy role held to a boundary applies. Each trusts only this repo and one environment; the state bucket is encrypted and private.
- **When:** on every `aws` workflow run.
- **On a finding:** a plan outside the roles fails in the pipeline.
- **Limits:** the deploy role trusts its `aws-<env>-apply` environment, so `protect-main.sh` creates each one taking `main` only, and fails on a rerun if one takes more; without that a PR editing `aws.yml` could deploy. The boundary caps grants, not every mistake.

## 17. Deploy: deploy approval

- **Does:** holds every apply until a second reviewer approves it, after the plan and cost comment (AGENTS.md rule 5, G3 and G4).
- **When:** on every apply, `dev` and `prod`.
- **On a finding:** the reviewer rejects the run and nothing applies.
- **Limits:** a prototype leaves the reviewer off, so `dev` applies unattended; it has no `prod` (AGENTS.md rule 4).

## 18. Deploy: runtime secrets

- **Does:** runtime secrets live encrypted in AWS; each function's role reads only its own, at runtime. `.env` is for your machine only.
- **When:** from the first secret the app needs.
- **On a finding:** Checkov flags secrets in Terraform or Lambda environment variables; Gitleaks in code.
- **Limits:** not in the template yet. Never put a value in Terraform state or a Lambda variable; rotate on a schedule and after a leak.

## 19. Deploy: API protection

- **Does:** non-public endpoints need a signed-in caller: a JWT authoriser for users, IAM for services (lessons 9). WAF blocks common attacks; CORS allows only your origins.
- **When:** on every request.
- **On a finding:** `401` unauthenticated, `403` blocked; DAST (10, 11) checks they hold.
- **Limits:** not in the template yet; `/health` is public by design. WAF costs monthly, so ask first (AGENTS.md rule 4).

## 20. Maintain: weekly re-scans

- **Does:** re-scans `main` so a newly published vulnerability or query still fails a run.
- **When:** early every Monday, Sydney time.
- **On a finding:** a failed run or an alert, blocking nothing until fixed (trade-offs 7).
- **Limits:** logs and artifacts go after 90 days, app logs after 30. Posture management (such as Prowler) isn't in the template yet.

## 21. Maintain: budget alert

- **Does:** emails at 80% and 100% of `MonthlyBudgetUsd` in actual spend, and when the forecast passes 100%.
- **When:** as spend accrues.
- **On a finding:** an email; find the cause in Cost Explorer.
- **Limits:** exists only if `BudgetEmail` is set; alerts but doesn't stop spending (trade-offs 10).

## 22. Maintain: access logs and throttling

- **Does:** logs every request and run for 30 days, and caps the request rate.
- **When:** on every request.
- **On a finding:** throttled calls get `429`; investigate in CloudWatch.
- **Limits:** nothing watches the logs (see 23, 24); raise retention if an audit needs it.

## 23. Maintain: audit logging

- **Does:** records every AWS API call: who, what, when and from where.
- **When:** on every AWS API call.
- **On a finding:** search the console, or Athena for a trail in S3.
- **Limits:** not in the template yet. Event history keeps 90 days free; a trail to S3 keeps longer for storage cost.

## 24. Maintain: threat detection and alarms

- **Does:** GuardDuty spots stolen credentials, mining and bad addresses. Alarms watch errors, `5xx`, throttling and latency.
- **When:** all the time.
- **On a finding:** follow the project's incident runbook: contain, rotate and restore.
- **Limits:** not in the template yet. GuardDuty costs after 30 days, so ask first (AGENTS.md rule 4).
