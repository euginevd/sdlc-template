# File notes

One line per repo file: what it is, why we need it.

## 1. uv (Python packages)

1. **pyproject.toml**: you edit it: packages, Python version, tool settings (ruff, pyright, pytest).
2. **apps/api/pyproject.toml**: the api app's own settings; shares the root lock and .venv.
3. **.python-version**: pins Python 3.13.
4. **uv.lock**: auto-generated exact versions + hashes, so every install is identical. Never edit.
5. **.venv/**: installed packages; git-ignored, rebuild with `uv sync`.

## 2. Docs (.md files)

1. **README.md**: the GitHub front page: what the project is and what's in it.
2. **CONTRIBUTING.md**: how anyone (person or agent) sets up and makes a change: plan, checks, PR.
3. **AGENTS.md**: rules every coding agent follows; a standard name most AI tools read.
4. **docs/**: project context agents read and keep current, as AGENTS.md lists: spec, decisions, status.
5. **SECURITY.md**: how to report a vulnerability privately; shown in GitHub's Security tab.
6. **LICENSE**: MIT: anyone may use, copy or change the code, keeping the notice; no warranty.

## 3. Git basics

1. **.git/**: git's own database (history, config, hooks); hidden in VS Code, never edit by hand.
2. **.gitignore**: files git never tracks: secrets (.env, *.tfvars), Terraform state, build output, caches.
3. **.gitattributes**: line-ending rules; forces LF on .sh so bash scripts work on Windows clones.
4. **.dockerignore**: keeps secrets, .git, caches and docs out of Docker images; smaller and safer.

## 4. Local checks (hooks + editor)

How they fit: setup.sh → `lefthook install` writes .git/hooks/pre-push → on `git push`, git runs it → lefthook reads lefthook.yml → runs pre-push-scan.sh → scan.sh passes or blocks the push.

1. **scripts/setup.sh**: run by hand once per clone: installs the tools, the hooks, then `uv sync`.
2. **lefthook.yml**: says which script runs on which git event; here, a scan before every push.
3. **.git/hooks/pre-push**: hidden; the only place git looks; per clone, written by `lefthook install`.
4. **.lefthook/pre-push-scan.sh**: collects the pushed commits' files and diffs, then calls scan.sh.
5. **scripts/scan.sh**: gitleaks (secrets) + Trivy (packages, IaC); a finding blocks the push.
6. **.vscode/extensions.json**: VS Code suggests the Trivy + Semgrep extensions; flags issues as you type.

Other scripts/ (run by hand or by CI, not hooks):

7. **scripts/protect-main.sh**: by hand once: locks main, squash-only merges, GitHub security features.
8. **scripts/pr-findings.sh**: lists a PR's open review threads and alerts; replies and resolves them.
9. **scripts/security-report.py**: CI: turns scanner results into PR annotations + one summary comment.
10. **scripts/cost-report.py**: CI: turns Infracost results into PR annotations + one cost comment.

## 5. App code

Typical: one folder per app in apps/; Python = pyproject.toml + `src/<name>/` + tests/; Node = package.json + src/ + tests/.

How they fit: `apps/<name>/` is one app; src/ holds the code, tests/ checks it; settings in 1.2.

1. **apps/api/src/api/handler.py**: the app's code: the function AWS Lambda calls for each request.
2. **apps/api/src/api/\_\_init\_\_.py**: empty; marks the folder as a Python package so it can be imported.
3. **apps/api/src/api/py.typed**: empty; tells type checkers the package ships its type hints.
4. **apps/api/tests/test_handler.py**: pytest checks: one that it works, one that it's safe.
5. **.coverage**: git-ignored; pytest-cov's record of tested lines; under 80% fails the run.

How tests run: `uv run pytest` (or CI on every PR) → finds tests in apps/ → runs them → writes .coverage → fails if any test fails or coverage < 80%.

## 6. CI/CD (.github/)

How they fit: open a PR → ci + security + codeql run → aws plans → review → merge → aws deploys dev.

1. **pull_request_template.md**: pre-fills every PR: what changed, security impact, checks ticked. Fixed name.
2. **dependabot.yml**: weekly update PRs for actions, Python, Terraform; also waits 7 days. Fixed name.
3. **workflows/ci.yml**: every PR: lint, type-check and test only the apps the PR changed.
4. **workflows/security.yml**: the pre-push scan again (hooks can be skipped) + Checkov, Semgrep; weekly.
5. **workflows/codeql.yml**: GitHub's code scanning for bugs and vulnerabilities; PRs, main, weekly.
6. **workflows/aws.yml**: Terraform plan + cost on PRs; deploys dev on merge, prod by hand after approval.

## 7. Cloud (infra/)

How they fit: bootstrap once by hand → aws.yml plans each `infra/aws/<unit>/` on PRs → applies after approval.

1. **bootstrap/bootstrap.yaml**: CloudFormation, by hand once per account: GitHub login, roles, state bucket.
2. **`<unit>/`**: one Terraform folder per deployable unit (e.g. api/), each with its own state.
   1. **versions.tf**: pins the Terraform and provider versions.
   2. **variables.tf**: inputs (project, environment, region), set by the pipeline.
   3. **main.tf**: the unit's resources, e.g. Lambda, API Gateway, roles, logs.
   4. **outputs.tf**: values printed after deploy, e.g. a URL.
   5. **.terraform.lock.hcl**: like uv.lock for Terraform: exact provider versions + hashes. Never edit.
