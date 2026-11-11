# Using the template

How to take a project from an empty repo to a deployed app with your coding agent: what you say, what the agent does, and what you decide, for a fast `prototype` or a gated `production` project. For developers; the agent works from [AGENTS.md](../AGENTS.md), not from this guide, so the prompts in italics are suggestions and your own words do the same job. The risks the template accepts are in [02-security-trade-offs.md](02-security-trade-offs.md); a tour of every file is in the appendix.

## 1. Pick a profile

The agent asks for this first ([AGENTS.md](../AGENTS.md) rules 15 and 24). Section 4 is the prototype's path and section 5 is production's.

| | `prototype`: a working MVP, fast | `production`: secure and gated |
|---|---|---|
| For | No real users, customer data or payments | Anything that has them |
| Approvals | Kickoff only; after that the agent plans, builds, merges and deploys to `dev` on its own | You approve the plan; a second reviewer approves each PR and each deploy, and GitHub enforces it |
| Tests | Main paths and anything sensitive, 50% coverage | Every change, abuse cases included, 80% coverage |
| When unsure | The agent takes the simpler option, says so in its report and keeps going | The agent asks you |
| Trade-offs | All accepted, 14 and 15 included | Each fixed, or accepted by a named person |

Both keep the pre-push scan, the PR security checks, no pushes to `main`, no reading of secrets, and deploys only through the pipeline. In both, the agent asks before a new AWS service, anything that adds cost or a change to its rules, and before a prototype takes real users, customer data, payments or a `prod` deploy (section 7).

## 2. Set up the repo

Once per project, by you. Steps 1 and 2 need the GitHub CLI, signed in with `gh auth login`.

1. **Create it:** `gh repo create <name> --template euginevd/sdlc-template --private --clone`. Keep a repo that deploys to AWS private: on a public repo, anyone signed in to GitHub can download its Terraform plans (trade-offs 9).
2. **Tools and hooks:** `bash scripts/setup.sh`, on every fresh clone: it installs the scanners, uv and Terraform if they're missing, then the push hook, and lists what the machine has. Until it has run, pushes from that clone aren't scanned. `bash scripts/setup.sh --check` lists the same and changes nothing.
3. **Protect `main`:** `bash scripts/protect-main.sh` sets the Actions limits, squash-only merges, GitHub's security features and the `main` ruleset; rerun it after changing it. A private repo needs a paid GitHub plan for the ruleset and the approval environments. On a public repo, also turn on everything under Settings → Advanced Security except **Agentic autofix**, which uses AI credits; the script can't set Automatic dependency submission, Malware alerts, the AI scans or Copilot Autofix, as they have no API.
4. **AWS, when the project first needs it:** the steps at the top of [bootstrap.yaml](../infra/aws/bootstrap/bootstrap.yaml), once per account: `dev` now, and `prod` (`Target=prod`) before the first `prod` deploy. Until then the `aws` workflow skips itself, so a project can start without an account. Two extras, each off until you set it: `BudgetEmail` emails you as the account's spend nears its monthly budget, and an Infracost API key in the `INFRACOST_API_KEY` secret puts a cost comment on each PR.
5. **Reviewers**, the one step that differs by profile:
   - `prototype`: none. Leave the required reviewer off the `aws-dev-apply` environment, so a merge deploys to `dev` unattended.
   - `production`: give a second reviewer write access, run `bash scripts/protect-main.sh production` so a PR needs their approval after its last push, and make them the required reviewer on each apply environment, with *Prevent self-review* on.
6. Keep `AGENTS.md`, `code-standards.md`, the workflows and the scripts as they are.

## 3. Kick off

Once per project. The repo arrives as a starter: `docs/` describes the health-check API it ships, with a line marked *(to fill in)* for everything that's yours to decide. Kickoff fills those in, and nothing is planned until you've approved the result.

| You say | The agent | You |
|---------|-----------|-----|
| *"Kick off `<name>`: `<your notes on the business, the problem, the users and the stack>`"* | Checks the machine, asks for the profile, then drafts `business-context.md` and `spec.md` from your notes | Answer, then correct each draft until it says what you want |
| | If there's UI: drafts `design-system.md`, keeping the house style, swapping its tokens for your brand or replacing it, then mocks up the MVP's main screens from it in `docs/mockups/mvp.html` | Open the mockup in a browser; ask for changes until both are what you want, then approve |
| | Extends `threat-model.md` and `costs.md` from the starter's to the project's, or deletes one that doesn't apply; a prototype keeps the starter's as they are unless you ask | `production`: approve each |
| | Starts `decisions.md` with the profile, the trade-offs you accept and who owns the code, then the big architecture choices | Say which trade-offs you accept; a prototype accepts them all |
| *"Rename the project"* | Renames the README, `Name` in `spec.md` and the root `pyproject.toml` (then `uv lock`); for a prototype sets `fail_under = 50` | Replace `LICENSE` to match the owner, or delete it; replace the images in `guides/assets/`. In a private project, delete `CONTRIBUTING.md` and `social.png`, which serve a public repo |
| | Opens one PR with all of it | Approve it, and the agent merges |

`business-context.md` and `design-system.md` describe the business, so its next project reuses them. Check they hold no coding standards that override `code-standards.md`.

## 4. Build a prototype

One prompt takes a piece of work from idea to `dev`, with nothing waiting for you.

| You say | The agent | You |
|---------|-----------|-----|
| *"Build `<the work>`"* | Adds the work to the spec if it's new, writes a short plan and starts building | Interrupt if the direction is wrong |
| | Builds each phase: code, tests, the checks, `status.md`, a local commit | |
| | Has a fresh subagent review the whole branch, fixes what it blocks, updates `decisions.md`, deletes the plan, and `mvp.html` once all its screens are built, and pushes; the pre-push scan runs | |
| | Opens a PR, fixes the findings from the checks and the security summary, and squash-merges once they pass | |
| | The pipeline deploys to `dev` and checks `/health`; the agent reports what was built, what passed and what was skipped | Try it in `dev`; say what to change next |

Ask for more whenever you want it: *"review the plan with me first"*, *"add a threat model"*, *"wait for me before merging"*.

## 5. Build for production

The same loop with a person at each gate, and every finding fed back to the agent (↺) until the work is clean.

| # | Stage | You say | The agent | You |
|:-:|-------|---------|-----------|-----|
| 1 | Plan | *"Update spec: `<what's changing>`"* | Edits `spec.md` and shows the change | ↺ Correct it, then approve |
| 2 | Plan | *"Plan `<the work>`"* | Writes the plan, updates the threat model and mocks up any screens; no code, then stops | ↺ Ask for changes, then approve |
| 3 | Code | *"Implement the plan"* | Builds each phase: code, tests, the checks, a fresh subagent review, `status.md`, a local commit. After the last one, reviews the whole branch, updates `decisions.md` and deletes the plan and its mockups, and `mvp.html` once all its screens are built | |
| 4 | Code | | Pushes; the pre-push scan runs. ↺ Fixes findings, then opens a PR with its Security line | |
| 5 | Build and test | | ↺ Fixes what the PR checks find: the security summary, code scanning, the Terraform plan and the cost comment; asks for review once they pass | |
| 6 | Release | *"Merge it"*, once it's approved | Updates the branch if `main` moved, squash-merges and deletes the branch | The second reviewer reads the diff and the security summary, then approves the PR |
| 7 | Deploy | | The pipeline plans every unit and, if one has changes, waits | The second reviewer approves the `dev` deploy on the run's page in GitHub; it applies and checks `/health` |
| 8 | Deploy | | | After sign-off, deploy `prod`: `gh workflow run aws.yml -f target=prod`; the second reviewer approves it |
| 9 | Operate | | Reports what was built and what the reviews found | Read the report; anything it raises starts at step 1 |

## 6. Other changes

| When | You say | What happens |
|------|---------|--------------|
| A small fix: a few dozen lines, touching no users, data, auth, endpoints, infrastructure or screens | *"Fix `<the problem>`"* | No plan doc: straight to a PR, with the same checks |
| Dependabot's weekly update PRs | *"Check the Dependabot PRs"* | The agent fixes what the checks find; they merge like any other PR |
| A scan on `main` or the weekly scan fails | *"Fix the failed scan on main"* | The agent lists the findings and fixes each at its cause in a PR |
| The work needs a new AWS service | Answer when the agent asks | The agent adds its permissions to `bootstrap.yaml` in the PR; you redeploy the stack before the merge, as the agent never touches AWS |
| The agent got something wrong | Tell it | It fixes it and adds a line to Known mistakes in `AGENTS.md`, which every later session reads |

## 7. From prototype to production

Say *"Make this project production"*, and the agent works through steps 1 to 3 in a PR:

1. `Profile` in `spec.md` becomes `production`, with a new decision in `decisions.md`.
2. It extends the threat model and costs for you to approve.
3. `fail_under` goes back to 80, and it adds the tests that were skipped, abuse cases included.
4. You go through the trade-offs: each gets its production fix, or a named person accepts it.
5. You set up the reviewers (section 2, step 5) and bootstrap the `prod` account.

## Appendix. The files

For learning your way around a project made from [euginevd/sdlc-template](https://github.com/euginevd/sdlc-template): the layout, then one line per file on what it is and why it's there, foundations first.

```
my-project/
├── pyproject.toml   uv.lock   .python-version     A.1 Python packages
├── README.md   AGENTS.md   CONTRIBUTING.md  …      A.2 docs for people and agents
├── docs/   guides/
├── .gitignore   .gitattributes                     A.3 git and ignore files
├── lefthook.yml   .lefthook/   scripts/            A.4 local tools
├── .vscode/   .editorconfig
├── apps/                                           A.5 app code, one folder per app
├── .github/                                        A.6 CI/CD
└── infra/aws/                                      A.7 cloud
```

### A.1 uv (Python packages)

1. **pyproject.toml**: the file you edit for packages, Python version and tool settings (ruff, pyright, pytest).
2. **apps/api/pyproject.toml**: the api app's own settings; shares the root lock and .venv.
3. **.python-version**: pins Python 3.13.
4. **uv.lock**: generated exact versions + hashes, so every install is identical. Never edit.
5. **.venv/**: the installed packages; git-ignored, rebuild with `uv sync`.

### A.2 Docs (.md files)

1. **README.md**: the GitHub front page: what the project is and what's in it.
2. **CONTRIBUTING.md**: how anyone (person or agent) sets up and makes a change: plan, checks, PR.
3. **AGENTS.md**: rules every coding agent follows; a standard name most AI tools read; changes rarely.
4. **docs/**: project context agents read and keep current, as AGENTS.md lists:
   1. **business-context.md**: the business, regulators, data rules, risk appetite, systems; changes rarely.
   2. **spec.md**: problem, users, stack, what done means, rules; the agent drafts, you approve; often.
   3. **code-standards.md**: numbered coding rules the pipeline can't check; changes rarely.
   4. **status.md**: what's built, how to run it, known gaps, what's next; every change.
   5. **decisions.md**: key decisions, why, and what they replaced; never deleted; sometimes.
   6. **plan-\<name\>.md**, **mockups/\<name\>.html**: the plan being built (design, risks, phases, PR groups) and its screens; deleted when done. **mockups/mvp.html**: the MVP's screens, agreed at kickoff; deleted once they're all built. **skeleton-plan.md**: the outline each plan is copied from.
   7. **design-system.md**, **threat-model.md**, **costs.md**: UI, risks, spend; optional; sometimes.
5. **guides/**: for people: 01 this template, 02 the risks it accepts; assets/ holds the README's hero image and `social.png`, the repo's social preview.
6. **SECURITY.md**: how to report a vulnerability privately; shown in GitHub's Security tab.
7. **LICENSE**: MIT; anyone may use, copy or change the code, keeping the notice; replace it per project.

### A.3 Git and ignore files

1. **.git/**: git's own database (history, config, hooks); hidden in VS Code, never edit by hand.
2. **.gitignore**: files git never tracks: secrets (.env*, *.tfvars), Terraform state, build output, caches.
3. **.gitattributes**: forces LF on .sh so bash works on Windows; collapses lock files in PR diffs.

### A.4 Local tools (hooks, editor, scripts)

How the push scan works: setup.sh → `lefthook install` writes .git/hooks/pre-push → `git push` runs it → lefthook reads lefthook.yml → pre-push-scan.sh passes or blocks.

1. **scripts/setup.sh**: run by hand once per clone: installs the tools, the hooks, then `uv sync`; `--check` only reports what the machine has.
2. **lefthook.yml**: says which script runs on which git event; here, a scan before every push.
3. **.git/hooks/pre-push**: hidden; the only place git looks; per clone, written by `lefthook install`.
4. **.lefthook/pre-push-scan.sh**: collects the pushed commits' files and diffs, then scans them with gitleaks (secrets) + Trivy (packages, IaC); a finding blocks the push.
5. **.vscode/extensions.json**: suggests the scanner, Ruff, Python and Terraform extensions.
6. **.editorconfig**: editor defaults for people and agents: LF, UTF-8, indent size, final newline.
7. **.claude/**: Claude Code's folder; local settings and worktrees git-ignored; rules live in AGENTS.md.

Other scripts, run by hand or by CI:

8. **scripts/protect-main.sh**: by hand once, rerun after changes: locks main, squash-only merges, security features; `production` adds a required second reviewer.
9. **scripts/pr-findings.sh**: lists a PR's failed checks, security summary, open review threads and alerts; replies and resolves threads.
10. **scripts/security-report.py**: CI: turns scanner results into PR annotations + one summary comment.
11. **scripts/cost-report.py**: CI: turns Infracost results into PR annotations + one cost comment.

### A.5 App code

One folder per app in apps/. Python: pyproject.toml (A.1) + `src/<name>/` + tests/; Node: package.json + src/ + tests/.

1. **apps/api/src/api/handler.py**: the function AWS Lambda calls for each request.
2. **apps/api/src/api/\_\_init\_\_.py**: empty; marks the folder as a Python package so it can be imported.
3. **apps/api/src/api/py.typed**: empty; tells pyright the package has type hints, or strict mode fails every import of it.
4. **apps/api/tests/test_handler.py**: two pytest tests: one that it works, one that it's safe.
5. **.coverage**: git-ignored; pytest-cov's record of tested lines.
6. **.pytest_cache/, .ruff_cache/, \_\_pycache\_\_/**: git-ignored tool caches for speed; safe to delete.

How tests run: `uv run pytest`, or CI on every PR → runs the tests in apps/ → writes .coverage → fails on any failed test or coverage under 80%.

### A.6 CI/CD (.github/)

How a change ships: open a PR → ci, security and codeql run → aws plans → review → merge → aws deploys dev.

1. **pull_request_template.md**: pre-fills every PR: what changed, security impact, checks. Fixed name.
2. **CODEOWNERS** *(not included)*: auto-requests reviewers per path; add it once a team shares the repo.
3. **dependabot.yml**: weekly update PRs for actions, Python, Terraform; waits 7 days too. Fixed name.
4. **workflows/ci.yml**: every PR: lint, type-check and test only the apps the PR changed.
5. **workflows/security.yml**: the pre-push scan again (hooks can be skipped) + Checkov, Semgrep, terraform validate; weekly.
6. **workflows/codeql.yml**: GitHub's code scanning for bugs and vulnerabilities; PRs, main, weekly.
7. **workflows/aws.yml**: Terraform plan + cost on PRs; on merge, plans every unit and deploys the changed ones to dev after approval; prod by hand.

### A.7 Cloud (infra/aws/)

How it deploys: bootstrap once by hand → aws.yml plans the changed units on PRs → applies after approval.

1. **bootstrap/bootstrap.yaml**: CloudFormation, by hand once per account: GitHub login, roles, state bucket, budget emails.
2. **`<unit>/`**: one Terraform folder per deployable unit (e.g. api/), each with its own state.
   1. **versions.tf**: pins the Terraform and provider versions.
   2. **variables.tf**: inputs (project, environment, region), set by the pipeline.
   3. **main.tf**: the unit's resources, e.g. Lambda, API Gateway, roles, logs.
   4. **outputs.tf**: values printed after deploy, e.g. a URL.
   5. **.terraform.lock.hcl**: uv.lock for Terraform: exact provider versions + hashes. Never edit.
