# Using the template

How to use this repo: start a project, run the workflow with your coding agent, and know what every file is for. For developers. The risks it accepts are in [02-security-trade-offs.md](02-security-trade-offs.md).

## 1. Workflow

**A new project starts at step 1; every later change, such as a feature or a fix, starts at step 2.** You write the spec, the agent plans and builds from it, and every gate feeds findings back to the agent (↺) until the work is clean. A small, low-risk change skips steps 3 and 4 ([AGENTS.md](../AGENTS.md) rule 11). The prompts are in italics.

| # | Stage | Who | Step |
|:-:|-------|-----|------|
| 1 | Plan | Developer, agent | **Create the repo and kick off:** once per project; you approve the kickoff docs before the first plan (section 2) |
| 2 | Plan | Developer, agent | **Update the spec:** *"Update spec"*. ↺ Correct it until it says what you want |
| 3 | Plan | Agent | **Plan:** *"Plan <the work>"*. The agent writes the plan, threat model and any UI mockups; no code |
| 4 | Plan | Developer | **Review the plan:** ↺ ask for changes to the plan, threat model and mockups, then approve |
| 5 | Code | Developer | **Implement:** *"Implement the plan"*. The agent works through the phases |
| 6 | Code | Agent | **Build each phase:** code, checks, subagent review, docs, then a local commit |
| 7 | Code | Agent | **Push:** the pre-push scan runs. ↺ The agent fixes findings, then opens a PR |
| 8 | Build and test | Pipeline, agent | **PR checks:** security scans with a summary comment and fixes, the Terraform plan and a cost comment. ↺ The agent fixes findings |
| 9 | Release | Developer, agent | **Merge:** you review the diff and security summary, then the agent squash-merges |
| 10 | Deploy | Developer, pipeline | **Apply:** you approve the plan; it deploys (`dev` on merge, `prod` by hand) and checks `/health` |
| 11 | Operate and monitor | Agent, developer | **Close the loop:** the agent updates status and decisions; findings feed step 2 |

## 2. Starting a project

Step 1 in full:

1. `gh repo create <name> --template euginevd/sdlc-template --private --clone`, then `bash scripts/setup.sh` and `bash scripts/protect-main.sh` (Actions limits, squash-only merges, GitHub's security features and the `main` ruleset; rerun it after changing it). A private repo needs a paid GitHub plan for the ruleset and the approval environments; a public repo gets them free. On a public repo, also turn on everything under Settings → Advanced Security except **Agentic autofix**, which uses AI credits; the script can't set Automatic dependency submission, Malware alerts, the AI scans or Copilot Autofix, as they have no API.
2. Kickoff: replace the worked example in `docs/`, keeping its structure. The agent drafts each doc from your notes and you approve it, in this order; nothing is planned until all are approved ([AGENTS.md](../AGENTS.md) rule 15).
   1. **Per business**, reused for its next project: `business-context.md` (who it is, regulators, data rules, risk appetite) and, if there's UI, `design-system.md` (its brand). Check it has no coding standards that override `code-standards.md`.
   2. **Per project:** `spec.md`, then `threat-model.md` and `costs.md`.
   3. **Decisions:** start `decisions.md` with which of the trade-offs in [02-security-trade-offs.md](02-security-trade-offs.md) you accept and who owns the code, then the big architecture choices. Replace `LICENSE` to match, or delete it.
3. Rename for the project: the README and its images in `guides/assets/`, `status.md` and the root `pyproject.toml` name (then `uv lock`).
4. Keep `AGENTS.md`, `code-standards.md`, the workflows and the scripts as they are.
5. Bootstrap AWS: the steps at the top of [bootstrap.yaml](../infra/aws/bootstrap/bootstrap.yaml).

## 3. The files

A project made from [euginevd/sdlc-template](https://github.com/euginevd/sdlc-template): the layout, then one line per file on what it is and why it's there, foundations first.

```
travel-claims/
├── pyproject.toml   uv.lock   .python-version     3.1 Python packages
├── README.md   AGENTS.md   CONTRIBUTING.md  …      3.2 docs for people and agents
├── docs/   guides/
├── .gitignore   .gitattributes   .dockerignore     3.3 git and ignore files
├── lefthook.yml   .lefthook/   scripts/            3.4 local tools
├── .vscode/   .editorconfig
├── apps/                                           3.5 app code, one folder per app
├── .github/                                        3.6 CI/CD
└── infra/aws/                                      3.7 cloud
```

### 3.1 uv (Python packages)

1. **pyproject.toml**: the file you edit for packages, Python version and tool settings (ruff, pyright, pytest).
2. **apps/api/pyproject.toml**: the api app's own settings; shares the root lock and .venv.
3. **.python-version**: pins Python 3.13.
4. **uv.lock**: generated exact versions + hashes, so every install is identical. Never edit.
5. **.venv/**: the installed packages; git-ignored, rebuild with `uv sync`.

### 3.2 Docs (.md files)

1. **README.md**: the GitHub front page: what the project is and what's in it.
2. **CONTRIBUTING.md**: how anyone (person or agent) sets up and makes a change: plan, checks, PR.
3. **AGENTS.md**: rules every coding agent follows; a standard name most AI tools read; changes rarely.
4. **docs/**: project context agents read and keep current, as AGENTS.md lists:
   1. **business-context.md**: the business, regulators, data rules, risk appetite, systems; changes rarely.
   2. **spec.md**: problem, users, stack, what done means, rules; the agent drafts, you approve; often.
   3. **code-standards.md**: numbered coding rules the pipeline can't check; changes rarely.
   4. **status.md**: what's built, how to run it, known gaps, what's next; every change.
   5. **decisions.md**: key decisions, why, and what they replaced; never deleted; sometimes.
   6. **plan-\<name\>.md**, **mockups/\<name\>.html**: the plan being built (design, risks, phases, PR groups) and its screens; deleted when done.
   7. **design-system.md**, **threat-model.md**, **costs.md**: UI, risks, spend; optional; sometimes.
5. **guides/**: for people: 01 this template, 02 the risks it accepts; assets/ holds the README's hero image and `social.png`, the repo's social preview.
6. **SECURITY.md**: how to report a vulnerability privately; shown in GitHub's Security tab.
7. **LICENSE**: MIT; anyone may use, copy or change the code, keeping the notice; replace it per project.

### 3.3 Git and ignore files

1. **.git/**: git's own database (history, config, hooks); hidden in VS Code, never edit by hand.
2. **.gitignore**: files git never tracks: secrets (.env*, *.tfvars), Terraform state, build output, caches.
3. **.gitattributes**: forces LF on .sh so bash works on Windows; collapses lock files in PR diffs.
4. **.dockerignore**: keeps secrets, .git, caches and docs out of Docker images; smaller and safer.

### 3.4 Local tools (hooks, editor, scripts)

How the push scan works: setup.sh → `lefthook install` writes .git/hooks/pre-push → `git push` runs it → lefthook reads lefthook.yml → pre-push-scan.sh → scan.sh passes or blocks.

1. **scripts/setup.sh**: run by hand once per clone: installs the tools, the hooks, then `uv sync`.
2. **lefthook.yml**: says which script runs on which git event; here, a scan before every push.
3. **.git/hooks/pre-push**: hidden; the only place git looks; per clone, written by `lefthook install`.
4. **.lefthook/pre-push-scan.sh**: collects the pushed commits' files and diffs, then calls scan.sh.
5. **scripts/scan.sh**: gitleaks (secrets) + Trivy (packages, IaC); a finding blocks the push.
6. **.vscode/extensions.json**: suggests the scanner, Ruff, Python and Terraform extensions.
7. **.editorconfig**: editor defaults for people and agents: LF, UTF-8, indent size, final newline.
8. **.claude/**: Claude Code's folder; local settings and worktrees git-ignored; rules live in AGENTS.md.

Other scripts, run by hand or by CI:

9. **scripts/protect-main.sh**: by hand once, rerun after changes: locks main, squash-only merges, security features.
10. **scripts/pr-findings.sh**: lists a PR's open review threads and alerts; replies and resolves them.
11. **scripts/security-report.py**: CI: turns scanner results into PR annotations + one summary comment.
12. **scripts/cost-report.py**: CI: turns Infracost results into PR annotations + one cost comment.

### 3.5 App code

One folder per app in apps/. Python: pyproject.toml (3.1) + `src/<name>/` + tests/; Node: package.json + src/ + tests/.

1. **apps/api/src/api/handler.py**: the function AWS Lambda calls for each request.
2. **apps/api/src/api/\_\_init\_\_.py**: empty; marks the folder as a Python package so it can be imported.
3. **apps/api/src/api/py.typed**: empty; tells type checkers the package ships its type hints.
4. **apps/api/tests/test_handler.py**: two pytest tests: one that it works, one that it's safe.
5. **.coverage**: git-ignored; pytest-cov's record of tested lines.
6. **.pytest_cache/, .ruff_cache/, \_\_pycache\_\_/**: git-ignored tool caches for speed; safe to delete.

How tests run: `uv run pytest`, or CI on every PR → runs the tests in apps/ → writes .coverage → fails on any failed test or coverage under 80%.

### 3.6 CI/CD (.github/)

How a change ships: open a PR → ci, security and codeql run → aws plans → review → merge → aws deploys dev.

1. **pull_request_template.md**: pre-fills every PR: what changed, security impact, checks. Fixed name.
2. **CODEOWNERS**: auto-requests reviewers per path; optional, worth it once a team shares the repo.
3. **dependabot.yml**: weekly update PRs for actions, Python, Terraform; waits 7 days too. Fixed name.
4. **workflows/ci.yml**: every PR: lint, type-check and test only the apps the PR changed.
5. **workflows/security.yml**: the pre-push scan again (hooks can be skipped) + Checkov, Semgrep; weekly.
6. **workflows/codeql.yml**: GitHub's code scanning for bugs and vulnerabilities; PRs, main, weekly.
7. **workflows/aws.yml**: Terraform plan + cost on PRs; deploys dev on merge, prod by hand after approval.

### 3.7 Cloud (infra/aws/)

How it deploys: bootstrap once by hand → aws.yml plans each unit on PRs → applies after approval.

1. **bootstrap/bootstrap.yaml**: CloudFormation, by hand once per account: GitHub login, roles, state bucket.
2. **`<unit>/`**: one Terraform folder per deployable unit (e.g. api/), each with its own state.
   1. **versions.tf**: pins the Terraform and provider versions.
   2. **variables.tf**: inputs (project, environment, region), set by the pipeline.
   3. **main.tf**: the unit's resources, e.g. Lambda, API Gateway, roles, logs.
   4. **outputs.tf**: values printed after deploy, e.g. a URL.
   5. **.terraform.lock.hcl**: uv.lock for Terraform: exact provider versions + hashes. Never edit.
