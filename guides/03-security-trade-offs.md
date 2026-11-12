# Security trade-offs

The risks the template accepts for speed, each with its production fix. Numbered so reviews can cite them (trade-offs 1). An accepted risk is a decision: change it here, never by weakening a check.

The profile decides what happens to them ([AGENTS.md](../AGENTS.md) rules 11 to 13). A `prototype` accepts them all. `production` applies each fix, or records in `decisions.md` who accepts the risk; 12 and 13 never apply to it.

| # | Risk | Why it's a risk | Production fix |
|:-:|------|-----------------|----------------|
| 1 | The agent shares the developer's GitHub identity | With the developer's token it could merge its own PR, approve its own deploy or delete the ruleset; only `AGENTS.md` rules 16 and 25 ask it not to | A second reviewer: `bash scripts/protect-main.sh production`, and *Prevent self-review* on the apply environments |
| 2 | Nothing enforces the agent's rules on the machine | Only `AGENTS.md` rules 25 and 26 stop it reading `.env` and secrets, skipping a hook or changing cloud resources | Deny rules in `.claude/settings.json` or a sandbox for `.env*`, `*.tfvars`, `--no-verify`, `terraform apply` and `aws`; secrets in a vault |
| 3 | Pinned tools go stale | Dependabot doesn't update digest-pinned images, `TF_VERSION` or local tools, so they miss newer checks | Renovate with the same 7-day wait; until then, update by hand when changing a workflow |
| 4 | The deploy role is broad in two places | `apigateway:*` covers every API in the region, and log delivery needs `*`, so in a shared account it reaches other workloads | A dedicated AWS account per project and environment |
| 5 | Plans run unreviewed code and are kept as files | A PR's plan runs before review and can read state; the saved plan holds state in plain text for a day | A private repo, a reviewer on the plan environments, and encrypted plans |
| 6 | A failing Terraform plan can merge | `aws` runs only on some paths, so `plan` can't be required; `terraform validate` catches all but AWS-only errors | An always-run job that fails when a plan failed, as a required check |
| 7 | A PR's checks cover only what it changes | Scans and app jobs run only on what changed, so a new rule matching old code fails only non-blocking runs on `main` and weekly | Alerts on failed `main` and weekly runs, fixed like a failed PR; review the `changes` job's paths when the layout changes |
| 8 | Some checks are missing | Workflows aren't linted though agents edit them (`AGENTS.md` rule 10); the report scripts are untested; Terraform isn't linted; no evals job | actionlint or zizmor and tflint as required checks; tests for the scripts; an evals job once an app calls a model |
| 9 | CodeQL needs a paid plan on private repos | On a private repo without Code Security, Semgrep is the only SAST | Buy Code Security, or accept Semgrep alone in `decisions.md` |
| 10 | Cost is a warning, not a gate | The cost comment doesn't block and prices only resources; the budget emails late and stops nothing | A required cost check, Cost Anomaly Detection, and a budget per project through cost tags |
| 11 | Nothing checks kickoff was finished | A leftover *(to fill in)* is a decision nobody made; only the kickoff gate (`AGENTS.md` rule 13) catches it | A CI check that fails on *(to fill in)* in `docs/` once `PROJECT_NAME` is set |
| 12 | A prototype runs without human gates | Nobody approves its plan, merges or `dev` deploys, and the agent settles unclear points (`AGENTS.md` rules 12 and 21) | The `production` profile, with the reviewer in 1 |
| 13 | A prototype is lightly tested | Main paths only, one review per branch and no threat model unless asked (`AGENTS.md` rule 15), so edge cases surface late | Before `production`: a threat model, abuse-case tests, 80% coverage and a review per phase |
