# Security trade-offs

The risks the template accepts, why it's built the way it is, and what to change before production. The same for every project, numbered so reviews can cite them (trade-offs 7). An accepted risk is a decision: change it here, never by weakening a check.

## Layers

What stops a bad change, from weakest to strongest. Layers 3 to 6 hold even if the agent ignores 1 and 2.

1. **Prompt rules:** `AGENTS.md` and `docs/code-standards.md`. The agent can ignore them.
2. **Harness:** Claude Code deny rules in `.claude/settings.json` *(planned)*. They match command patterns, so a workaround can slip past.
3. **Token scope:** the agent's own fine-grained token *(planned)*, which can't approve a deploy or edit environments or the ruleset.
4. **Repo:** the `main` ruleset requires every check to pass, allows squash merges only, and blocks force pushes and deletion.
5. **Deploy gate:** the `aws-<target>-apply` environment needs your approval and deploys only from `main`.
6. **Cloud:** the deploy role trusts only the apply environment, so a workflow edited to skip the gate can't deploy. The permissions boundary caps every role Terraform creates.

## Known risks

Each risk gives why it's accepted, what limits it, and what to change for production.

7. **The agent uses your GitHub token.** It could approve its own deploy, or edit the environment or ruleset. *Why:* one identity is simplest for a solo developer. *Limited by:* `AGENTS.md` rules 20 and 21. *Production:* layers 2 and 3.
8. **Merges need no human approval.** The ruleset requires 0 approvals. *Why:* the agent merges once checks pass, so work keeps moving. *Limited by:* required checks and the deploy gate (layer 5). *Production:* once the agent has its own identity, require 1 approval and add CODEOWNERS for `.github/`, `aws/bootstrap/`, `scripts/` and `AGENTS.md`.
9. **A failing Terraform plan can merge.** The plan runs only when `aws/` or `apps/` changes, so it can't be a required check. *Limited by:* the apply hits the same error and needs approval anyway. *Production:* a required job that always runs and passes only when the plan does.
10. **Branches needn't be up to date to merge.** *Why:* no rebasing every PR. *Limited by:* `ci` and `security` run again on `main`. *Production:* turn on strict status checks, or use a merge queue.
11. **PR plans run branch code with AWS read access.** `terraform plan` can run code, such as an external data source. *Why:* a plan on the PR catches errors before review. *Limited by:* the plan role can only read, plus write the state lock; on a public repo, outside contributors' runs wait for your approval. *Production:* keep the plan role read-only as services are added.
12. **Vulnerabilities with no fix pass.** Trivy blocks HIGH and CRITICAL only, with `--ignore-unfixed`. *Why:* a finding with no fix can't be acted on and would block every PR. *Limited by:* the weekly re-scan fails once a fix ships. *Production:* review unfixed CRITICAL findings each week.
13. **Pinned images go stale.** Dependabot updates actions, `uv` and Terraform, but not the image digests in `docker run` and `container:` lines. *Limited by:* Trivy downloads its vulnerability database on each run. *Production:* Renovate, or a monthly digest update.
14. **Local tools aren't pinned.** `scripts/setup.sh` installs the latest gitleaks and Trivy. *Limited by:* CI runs the same scans from pinned images.
15. **Semgrep rules can change between runs.** `p/default` comes from the registry on each run. *Production:* acceptable, or pin a local ruleset.
16. **The deploy role is broad in places.** It has `apigateway:*` in the region and `logs:PutResourcePolicy` on `*`. *Why:* API Gateway has no name-based ARNs. *Limited by:* one AWS account per environment. *Production:* never share an account with another workload.
17. **AWS-managed encryption.** The state bucket uses SSE-S3, and log groups have no customer key. *Why:* a customer key adds a key policy to run and a cost. *Limited by:* the bucket is private, TLS-only and versioned. *Production:* KMS keys for every store that holds personal data.
18. **The sample Lambda keeps the defaults.** No VPC, X-Ray, dead-letter queue, reserved concurrency or code signing; each skip's reason is next to it in `aws/api/main.tf`. *Production:* add each one when the app needs it, and code signing if policy requires it.
19. **Logs are kept 30 days.** *Why:* cost. *Production:* the retention that audits and the regulator require.
20. **Deleting the bootstrap stack deletes the state bucket.** *Why:* cleanup in one step. *Limited by:* the delete fails unless the bucket is empty. *Production:* `DeletionPolicy: Retain` on the bucket and termination protection on the stack.
21. **The SBOM isn't signed.** *Production:* build provenance attestations with `actions/attest-build-provenance`, which is GitHub-owned, so the allow-list already permits it.

## Why we do what we do

22. **Actions pinned by commit SHA, from an allow-list:** a moved tag can't change what the pipeline runs.
23. **Scanners run from digest-pinned images:** no third-party action code runs in the pipeline.
24. **Read-only tokens, and no credentials kept after checkout:** a step can't push with the job's token.
25. **Packages at least 7 days old:** most malicious releases are pulled within days.
26. **OIDC, no access keys:** nothing long-lived to leak.
27. **Separate plan and deploy roles:** a PR only ever gets read access.
28. **The apply uses the saved plan:** what deploys is exactly what you approved, zip included.
29. **A pre-push scan and the same scans in CI:** a hook can be skipped; CI can't.
30. **Gitleaks over full history and unpushed commits:** a secret added then removed is still caught.

## Before production

31. The agent's own token (layer 3): Contents, Pull requests and Workflows write; Actions read; no Administration, Deployments, Environments, Secrets or Variables.
32. Deny rules in `.claude/settings.json` (layer 2).
33. The apply environments, with you as required reviewer and `main` only.
34. A dedicated AWS account per environment (16).
35. The production steps in 8 to 10, 12, 13 and 17 to 21.
