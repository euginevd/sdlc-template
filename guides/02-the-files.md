# The files

Every file in the template and what it's for, one line each. Running a project: [guide 01](01-using-the-template.md). Which stage each doc serves: [guide 06](06-secure-agentic-sdlc.md).

```
my-project/
├── pyproject.toml   uv.lock   .python-version     1. Python packages
├── README.md   AGENTS.md   CONTRIBUTING.md  …      2. docs for people and agents
├── docs/   guides/
├── .gitignore   .gitattributes                     3. git and local tools
├── lefthook.yml   .lefthook/   scripts/
├── .vscode/   .editorconfig   .claude/
├── apps/                                           4. app code, one folder per app
├── .github/                                        5. CI/CD
└── infra/aws/                                      6. cloud
```

## 1. uv (Python packages)

### 1.1 Tooling (core, always kept)

Runs the template's own scripts and hooks, so keep it even without a Python app.

1. **pyproject.toml**: packages, Python version and tool settings (ruff, pyright, pytest).
2. **.python-version**: pins Python 3.13.
3. **uv.lock**: exact versions and hashes, so every install is identical. Never edit.
4. **.venv/**: installed packages; git-ignored, rebuilt with `uv sync`.

### 1.2 Python app (a module)

The starter's `api`; the tooling above doesn't need it.

1. **apps/api/pyproject.toml**: the api's own settings; shares the root lock and `.venv`. Its code is in section 4.

## 2. Docs (.md files)

### 2.1 Root files (core)

1. **README.md**: the GitHub front page.
2. **AGENTS.md**: the rules every coding agent follows, with the gates for each profile; changes rarely. Kept short, as every session reads it.
3. **CONTRIBUTING.md**: how a person or agent sets up and makes a change.
4. **SECURITY.md**: how to report a vulnerability privately.
5. **LICENSE**: MIT; replace it per project.

### 2.2 Project docs (core)

The project context in `docs/` that agents read and keep current.

1. **intent.md**: what you want built and why, in your own words, with research: Problem, Proposed outcome, Affected users and systems, Constraints, Success criteria and Open questions; you write it, or answer in chat at kickoff and the agent writes it for you to check.
2. **spec.md**: the requirements and design agreed from `intent.md`: the business, stack, done-when, rules and what's left out; you approve (production).
3. **features.md**: what each app does today, one row per feature, with its issue and PR; planned work is the open issues.
4. **decisions.md**: the project's decision log (ADRs), one line each: the decisions in force, why, and what they replaced.
5. **standards.md**: numbered coding rules, most of which the pipeline can't check.
6. **lessons.md**: mistakes an agent has made, each with its fix, by area; the agent reads an area's before working in it.
7. **threat-model.md**: the data, its flows and the top risks, each with its controls.
8. **checklist.md**: the guardrails by stage and profile, to clear before go-live.
9. **templates/plan.md**: the template each plan is copied from: Files that change, Order of work, Risks and Proof, as in Anthropic's plan.md.
10. **plan-\<name\>.md**: the plan being built; deleted when done.

### 2.3 Module docs

1. **web/**: `design-system.md` and `mockups/`, the UI's look and each screen's mockup, `mvp.html` from kickoff among them; for a project with screens.
2. **aws/**: `costs.md` and `lessons.md`, spend and AWS's lessons; for a project on AWS.

### 2.4 Guides (for people)

`guides/`: 01 using the template, 02 this tour, 03 accepted risks, 04 each guardrail, 05 removing a project from AWS, 06 the six lifecycle stages and their gates, 07 decisions on the template, 08 the incident runbook. `assets/` holds the README's images, `flow.html` that renders them, and `social.png`.

### 2.5 Work queue

**GitHub issues** (not a file): the agent takes the oldest open one, and the PR that builds it closes it ([guide 07](07-template-decisions.md) finding 4).

## 3. Git and local tools

### 3.1 Git (core)

1. **.git/**: git's own database; never edit by hand.
2. **.gitignore**: what git never tracks: secrets (`.env*`, `*.tfvars`), Terraform state, build output and caches.
3. **.gitattributes**: normalizes line endings, keeps LF on `.sh` so bash works on Windows, and collapses lock files in PR diffs.
4. **local/**: your own notes and drafts; git-ignored, so never committed.

### 3.2 Hooks (core)

`setup.sh` runs `lefthook install`; each `git push` then runs the scan and the reference check, and each commit the attribution check, which pass or block.

1. **lefthook.yml**: which script runs on which git event.
2. **.lefthook/pre-push-scan.sh**: scans the pushed commits with gitleaks (secrets) and Trivy (packages, IaC); a finding blocks the push.
3. **.git/hooks/pre-push** and **commit-msg**: hidden and per clone, written by `lefthook install`.

### 3.3 Scripts

All core, except `cost-report.py`, which only an AWS project needs.

1. **scripts/setup.sh**: once per clone, on Windows, macOS or Linux: installs the tools and hooks, then `uv sync`; `--check` only reports.
2. **scripts/check.sh**: runs what CI runs, for what changed, plus `itest` and `e2e` (Playwright, in `e2e/` once a project has screens) on request; CI's app jobs call it too, and the agent pastes its result when reporting done.
3. **scripts/protect-main.sh**: once, by hand: locks `main`, squash-only merges, security features, apply environments that take `main` only; `production` adds a second reviewer.
4. **scripts/agent-guard.sh**: the PreToolUse hook: before each edit or command, production denies touching `.env`, no agent calls an MCP server named for `prod`, and editing an existing test or a check's own settings asks first.
5. **scripts/agent-stop-check.sh**: the Stop hook: runs `check.sh` and sends a failure back to the agent, once, so it can't loop.
6. **scripts/pr-findings.sh**: lists a PR's failed checks, security summary, open threads and alerts; replies and resolves threads.
7. **scripts/check-refs.py**: fails when a numbered list skips a number, a reference names an item that doesn't exist, or an item cited elsewhere moved.
8. **scripts/check-attribution.py**: fails on an AI co-author or "Generated with" line in a commit message or PR description (AGENTS.md rule 15).
9. **scripts/check-hooks.py**: fails when a Claude Code hook in `.claude/settings.json` no longer loads, runs a missing or broken script, or the guard stops denying a production `.env` edit, since a broken hook fails silently.
10. **scripts/agent-evals.py**: runs the agent evals in `.claude/evals/` through Claude Code in plan mode, which changes nothing; CI's `agent-evals` workflow calls it.
11. **scripts/security-report.py**: CI: scanner results as PR annotations and one summary comment.
12. **scripts/cost-report.py**: CI: Infracost results as PR annotations and one cost comment (AWS module).
13. **scripts/tests/**: tests for the scripts; they run with the apps' tests.

### 3.4 Agent setup (core)

1. **.claude/settings.json**: Claude Code's shared settings: no AI attribution on commits or PRs, asking before each `git push` (production), a guard before each edit or command, a Stop hook that runs the quick checks when the agent ends a turn with uncommitted edits, and deny rules for force-pushes, skipped hooks, Terraform applies and `.env` reads.
2. **.claude/skills/**: the steps the agent loads when it reaches them: `kickoff`, `pull-request` and `deploy` (AWS module), the `review-security` and `review-design` reviews AGENTS.md rule 10 runs, and `new-app` for adding an app.
3. **.claude/agents/verifier.md**: the subagent that runs the app to check a change. It and the two review skills run on Sonnet, a different model from the session that wrote the code, for a second opinion.
4. **.claude/evals/**: the agent evals' cases, each a prompt and the patterns its answer must and mustn't have, and the pinned Claude Code CLI that `scripts/agent-evals.py` runs them with.

Local settings and worktrees are git-ignored.

### 3.5 Editor (core)

1. **.vscode/extensions.json**: suggests the Trivy and Semgrep scanners, Ruff, Python and Terraform extensions.
2. **.editorconfig**: LF, UTF-8, indent size, a final newline and no trailing spaces.

## 4. App code (modules)

Each app is a module in its own folder in `apps/`, added with the `new-app` skill: Python has `pyproject.toml`, `src/<name>/` and `tests/`; Node has `package.json`, `src/` and `tests/`.

### 4.1 The starter api (Python)

A Lambda behind `/health`; its settings are in section 1.2 and its Terraform in section 6.

1. **apps/api/src/api/handler.py**: the function Lambda calls for each request.
2. **apps/api/src/api/\_\_init\_\_.py**: empty; marks the folder as a package.
3. **apps/api/src/api/py.typed**: empty; tells pyright the package has types, or strict mode fails its imports.
4. **apps/api/tests/test_handler.py**: two tests: one that it works, one that it's safe.

### 4.2 Tool output

**.coverage**, **.pytest_cache/**, **.ruff_cache/**, **\_\_pycache\_\_/**: git-ignored, rebuilt by the tools; safe to delete.

Tests fail on any failed test, or on coverage under `fail_under` (80%, or 50% for a prototype).

## 5. CI/CD (.github/)

A change ships like this: issue → PR → `ci`, `security`, `codeql` and `rules` run → `aws` plans → review → merge → `aws` deploys `dev`.

### 5.1 Workflows (core)

1. **workflows/ci.yml**: lint, types and tests for only the apps a PR changes; actionlint, zizmor and shellcheck when workflows or scripts change; and the `kickoff` check for leftover *(to fill in)* lines and docs over their length.
2. **workflows/security.yml**: the push scan again, plus Checkov, Semgrep, `terraform validate` and TFLint; weekly too.
3. **workflows/codeql.yml**: GitHub's code scanning on PRs, `main` and weekly.
4. **workflows/rules.yml**: the hooks' reference and attribution checks again on every PR, as the required `rules` check, so a skipped hook can't get through, and `check-hooks.py` for the agent's hooks.
5. **workflows/factory.yml**: an issue the owner labels `factory` becomes a draft PR, built by a cloud agent; off until an `ANTHROPIC_API_KEY` secret is set, and run as the agent's own GitHub App when there is one.
6. **workflows/agent-evals.yml**: on a PR that changes `AGENTS.md`, `.claude/` or the standards, checks the agent still follows the rules; off until an `ANTHROPIC_API_KEY` secret is set, and not required.

### 5.2 Workflows (AWS module)

1. **workflows/aws.yml**: Terraform plan and cost on PRs, with one `plan-result` check the ruleset requires; on merge, applies the changed units to `dev`, smoke-tests them and runs ZAP's passive scan, and `prod` by hand.
2. **workflows/images.yml**: builds, scans and pushes each app's image to ECR, with its SBOM and signed provenance and SBOM attestations; idle until an app has a Dockerfile.

### 5.3 GitHub settings (core)

1. **ISSUE_TEMPLATE/**: the forms for a new issue. `intent.yml` has `intent.md`'s headings, so each issue is one change's intent; `incident.yml` records an incident or finding and what stops a repeat, so Maintain feeds the next Plan.
2. **pull_request_template.md**: pre-fills each PR: what changed, security, checks, and `Closes #<issue>`.
3. **dependabot.yml**: weekly update PRs for actions, Python and Terraform, each release 7 days old; an app adds its own, such as npm or Docker.
4. **CODEOWNERS** *(not included)*: requests reviewers per path; add it once a team shares the repo.

## 6. Cloud (infra/aws/, AWS module)

Bootstrap once by hand; after that the units deploy only through `aws.yml` (section 5.2).

### 6.1 Bootstrap

1. **bootstrap/bootstrap.yaml**: CloudFormation you deploy by hand once per account: GitHub's sign-in (OIDC), a read-only plan role, a bounded deploy role, a read-only troubleshoot role with its CLI user, the state bucket, a budget alert and, with `Monitoring` on, GuardDuty and an alerts topic.

### 6.2 Terraform units

One folder per deployable unit (such as `api/`), each with its own state; TFLint's settings for every unit are in `infra/aws/.tflint.hcl`.

1. **versions.tf**: pins Terraform and the providers.
2. **variables.tf**: inputs (project, environment, region), set by the pipeline.
3. **main.tf**: the unit's resources, such as Lambda, API Gateway, roles and logs.
4. **outputs.tf**: values printed after a deploy, such as a URL.
5. **.terraform.lock.hcl**: exact provider versions and hashes. Never edit.
6. **.terraform/**: downloaded providers; git-ignored, rebuilt by `terraform init`.
