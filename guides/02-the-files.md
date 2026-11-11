# The files

For learning your way around a project made from [euginevd/sdlc-template](https://github.com/euginevd/sdlc-template): the layout, then one line per file on what it is and why it's there, foundations first. For people; how to run a project is in [01-using-the-template.md](01-using-the-template.md).

```
my-project/
├── pyproject.toml   uv.lock   .python-version     1. Python packages
├── README.md   AGENTS.md   CONTRIBUTING.md  …      2. docs for people and agents
├── docs/   guides/
├── .gitignore   .gitattributes                     3. git and ignore files
├── lefthook.yml   .lefthook/   scripts/            4. local tools
├── .vscode/   .editorconfig
├── apps/                                           5. app code, one folder per app
├── .github/                                        6. CI/CD
└── infra/aws/                                      7. cloud
```

## 1. uv (Python packages)

1. **pyproject.toml**: the file you edit for packages, Python version and tool settings (ruff, pyright, pytest).
2. **apps/api/pyproject.toml**: the api app's own settings; shares the root lock and .venv.
3. **.python-version**: pins Python 3.13.
4. **uv.lock**: generated exact versions + hashes, so every install is identical. Never edit.
5. **.venv/**: the installed packages; git-ignored, rebuild with `uv sync`.

## 2. Docs (.md files)

1. **README.md**: the GitHub front page: what the project is and what's in it.
2. **CONTRIBUTING.md**: how anyone (person or agent) sets up and makes a change: plan, checks, PR.
3. **AGENTS.md**: rules every coding agent follows; a standard name most AI tools read; changes rarely.
4. **docs/**: project context agents read and keep current, as AGENTS.md lists:
   1. **business-context.md**: the business, regulators, data rules, risk appetite, systems; changes rarely.
   2. **spec.md**: problem, users, stack, what done means, rules; the agent drafts, you approve; often.
   3. **code-standards.md**: numbered coding rules the pipeline can't check; changes rarely.
   4. **status.md**: what's built, how to run it, known gaps, what's next; every change.
   5. **decisions.md**: key decisions, why, and what they replaced; never deleted; sometimes.
   6. **design-system.md**, **threat-model.md**, **costs.md**: UI, risks, spend; optional; sometimes.
   7. **skeleton-plan.md**: the outline each plan is copied from.
   8. **plan-\<name\>.md**, **mockups/\<name\>.html**: the plan being built and its screens; deleted when done.
   9. **mockups/mvp.html**: the MVP's screens, agreed at kickoff; deleted once they're all built.
5. **guides/**: for people: 01 how to use the template, 02 this tour, 03 the risks it accepts; assets/ holds the README's hero image and `social.png`, the repo's social preview.
6. **SECURITY.md**: how to report a vulnerability privately; shown in GitHub's Security tab.
7. **LICENSE**: MIT; anyone may use, copy or change the code, keeping the notice; replace it per project.

## 3. Git and ignore files

1. **.git/**: git's own database (history, config, hooks); hidden in VS Code, never edit by hand.
2. **.gitignore**: files git never tracks: secrets (.env*, *.tfvars), Terraform state, build output, caches.
3. **.gitattributes**: forces LF on .sh so bash works on Windows; collapses lock files in PR diffs.

## 4. Local tools (hooks, editor, scripts)

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

## 5. App code

One folder per app in apps/. Python: pyproject.toml (section 1) + `src/<name>/` + tests/; Node: package.json + src/ + tests/.

1. **apps/api/src/api/handler.py**: the function AWS Lambda calls for each request.
2. **apps/api/src/api/\_\_init\_\_.py**: empty; marks the folder as a Python package so it can be imported.
3. **apps/api/src/api/py.typed**: empty; tells pyright the package has type hints, or strict mode fails every import of it.
4. **apps/api/tests/test_handler.py**: two pytest tests: one that it works, one that it's safe.
5. **.coverage**: git-ignored; pytest-cov's record of tested lines.
6. **.pytest_cache/, .ruff_cache/, \_\_pycache\_\_/**: git-ignored tool caches for speed; safe to delete.

How tests run: `uv run pytest`, or CI on every PR → runs the tests in apps/ → writes .coverage → fails on any failed test, or coverage under `fail_under` in `pyproject.toml` (80%, or 50% for a prototype).

## 6. CI/CD (.github/)

How a change ships: open a PR → ci, security and codeql run → aws plans → review → merge → aws deploys dev.

1. **pull_request_template.md**: pre-fills every PR: what changed, security impact, checks. Fixed name.
2. **CODEOWNERS** *(not included)*: auto-requests reviewers per path; add it once a team shares the repo.
3. **dependabot.yml**: weekly update PRs for actions, Python, Terraform; waits 7 days too. Fixed name.
4. **workflows/ci.yml**: every PR: lint, type-check and test only the apps the PR changed.
5. **workflows/security.yml**: the pre-push scan again (hooks can be skipped) + Checkov, Semgrep, terraform validate; weekly.
6. **workflows/codeql.yml**: GitHub's code scanning for bugs and vulnerabilities; PRs, main, weekly.
7. **workflows/aws.yml**: Terraform plan + cost on PRs; on merge, plans every unit and deploys the changed ones to dev after approval; prod by hand.

## 7. Cloud (infra/aws/)

How it deploys: bootstrap once by hand → aws.yml plans the changed units on PRs → applies after approval.

1. **bootstrap/bootstrap.yaml**: CloudFormation, by hand once per account: GitHub login, roles, state bucket, budget emails.
2. **`<unit>/`**: one Terraform folder per deployable unit (e.g. api/), each with its own state.
   1. **versions.tf**: pins the Terraform and provider versions.
   2. **variables.tf**: inputs (project, environment, region), set by the pipeline.
   3. **main.tf**: the unit's resources, e.g. Lambda, API Gateway, roles, logs.
   4. **outputs.tf**: values printed after deploy, e.g. a URL.
   5. **.terraform.lock.hcl**: uv.lock for Terraform: exact provider versions + hashes. Never edit.
