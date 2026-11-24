# Using the template

How to take a project from an empty repo to a deployed app with your coding agent: what you say, what the agent does, and what you decide. For developers; the agent works from [AGENTS.md](../AGENTS.md), and the prompts in italics are only suggestions. Every file: [02-the-files.md](02-the-files.md). Accepted risks: [03-security-trade-offs.md](03-security-trade-offs.md). Each guardrail: [04-the-guardrails.md](04-the-guardrails.md).

## 1. Pick a profile

The agent asks for this first ([AGENTS.md](../AGENTS.md) rules 4 to 7). Where each profile stops for you is the gate table in rule 5; section 4 is the prototype's path and section 5 is production's.

| | `prototype`: a working MVP, fast | `production`: gated |
|---|---|---|
| For | No real users, customer data or payments | Anything that has them |
| You approve | Nothing after the start's questions: checks and a fresh reviewer pass its gates | The start and every plan; a second reviewer approves each PR and each apply, `dev` and `prod` |
| Environments | `dev` only | `dev`, then `prod`, each in its own account |
| Tests | Main paths and anything sensitive, 50% coverage | Abuse cases too, 80% coverage |
| When unsure | The agent takes the simpler option and says so | The agent asks |
| Runs | For hours on its own, issue after issue, until the backlog or the time budget is done | One step at a time, as you ask |
| Trade-offs | All accepted | Each fixed, or accepted by a named person |

In both, one branch holds a session's work. A prototype's agent commits, pushes, opens the PR and merges on its own; in production it does each only when you ask. It runs local commands itself and gives you cloud commands as bash for AWS CloudShell; what it asks first and never does is in [AGENTS.md](../AGENTS.md) rules 4 and 14 to 17.

## 2. Set up the repo

The easy way: open Claude Code in a clone of this template (`gh repo clone euginevd/sdlc-template`) on your own machine and say *"New project"*. The template's `new-project` skill (in `.claude/skills/`, left out of the projects it makes) is the only time you're asked anything:

| Step | It asks or does |
|------|-----------------|
| 1 | Checks the template is up to date and `gh` is signed in |
| 2 | The repo name, and checks it's free |
| 3 | Your intent, heading by heading: problem, outcome, users, constraints, success, open questions, and what to borrow from |
| 4 | Reads it back to you until it's right |
| 5 to 7 | Prototype or production, public or private, and whether it needs AWS and screens, each with a recommendation |
| 8 | The monthly spend limit, and for a prototype how long its run may take (8 hours unless you say) |
| 9 | Production only: the business behind it, for the spec |
| 10 | Shows a summary and waits for your yes |
| 11 to 13 | Writes only the files your answers need ([`scripts/new-project.py`](../scripts/new-project.py)), then the spec, decisions, design system and mockup |
| 14 to 15 | Runs `setup.sh`, creates the repo on GitHub, runs `protect-main.sh`, and turns the intent into GitHub issues in build order |
| 16 to 17 | Production stops for your approval (gate G0). A prototype hands over: open the new folder, start Claude Code there and say *"Go"* |

What each project gets: a slim prototype is about 55 files (the rules, seven docs, three workflows, the scripts and an empty `guides/` for its own guides); production adds the threat model, checklist, security guides and the rest of the pipeline; AWS and screens add their own. It needs your machine, as a cloud session can't create repos. The manual way, which copies everything:

Once per project, by you. Steps 1 to 3 need the GitHub CLI, signed in with `gh auth login`.

1. **Create it:** `gh repo create <name> --template euginevd/sdlc-template --public --clone` for a personal or portfolio project, built in the open; `--private` for a work project. On a public repo anyone signed in can download `main`'s Terraform plans for a day, so nothing secret goes in code or Terraform (trade-offs 5). A private repo needs a paid GitHub plan (Pro or Team) for step 3.
2. **Tools and hooks:** `bash scripts/setup.sh` on every fresh clone installs the scanners, uv, Terraform and the push hook: with winget on Windows, Homebrew on macOS, and checked downloads on Linux, where an agent in a cloud container runs it itself. Until it runs, pushes aren't scanned; `bash scripts/setup.sh --check` only reports.
3. **Protect `main`:** `bash scripts/protect-main.sh` sets the Actions limits, squash-only merges, security features, the `main` ruleset and the `aws-dev-apply` environment, which deploys from `main` only. On a free plan a private repo gets neither the ruleset nor the environment, so nothing is enforced and the script says so; a public one also needs everything under Settings → Advanced Security turned on by hand ([guide 04](04-the-guardrails.md), sections 4 and 7).
4. **AWS, once the project works locally and you're happy with it:** follow the steps at the top of [bootstrap.yaml](../infra/aws/bootstrap/bootstrap.yaml), once per account: `dev`, and for production `prod` (`Target=prod`) before its first release. Set `BudgetEmail` for spend alerts, and for production `Monitoring=on` with the `MONITORING` repo variable for GuardDuty and alarms (charged after 30 days) and `INFRACOST_API_KEY` for a cost comment on each PR; `protect-main.sh` has already limited each `aws-<env>-apply` environment to `main`; run it again to check ([guide 04](04-the-guardrails.md), section 16).
5. **Reviewers**, the one step that differs by profile:
   - `prototype`: none. Leave the reviewer off `aws-dev-apply`, so a merge deploys to `dev` unattended.
   - `production`: give a second reviewer write access, run `bash scripts/protect-main.sh production`, and make them the required reviewer on each apply environment, with *Prevent self-review* on.
6. **Optional, the agent's own identity and the factory:** create a GitHub App (Settings → Developer settings → GitHub Apps) with Contents, Pull requests and Issues set to read and write and no webhook, and install it on this repo only. Save its Client ID as the `AGENT_APP_CLIENT_ID` variable and a private key as the `AGENT_APP_PRIVATE_KEY` secret; the factory's PRs then show as the agent and run CI (trade-offs 1). The factory itself turns on with an `ANTHROPIC_API_KEY` secret, and each run is charged to that key: label an issue `factory` and a cloud agent builds it into a draft PR. Only your label starts it.

   ```bash
   gh variable set AGENT_APP_CLIENT_ID --body <client-id>
   ```

   ```bash
   gh secret set AGENT_APP_PRIVATE_KEY < <downloaded-key>.pem
   ```

   ```bash
   gh secret set ANTHROPIC_API_KEY
   ```

7. Keep `AGENTS.md`, `standards.md`, the workflows and the scripts as they are.

## 3. Gate G0, production

The `new-project` skill drafts every doc a production project needs and stops. Before any issue is built, you approve `spec.md` with its Business section, `threat-model.md`, `docs/aws/costs.md` with AWS, the design system and the mockup with screens, and the trade-offs in `decisions.md`, each fixed or accepted by a named person. Then say *"Commit and push"* for its first PR. A prototype has no stop here: it goes straight to section 4.

## 4. Build a prototype

Say *"Go"* in the new project, and the agent turns on its autopilot ([`scripts/autopilot.sh`](../scripts/autopilot.sh)) and builds the backlog, oldest issue first, without asking you anything. Each issue passes every gate, with a check or a fresh reviewer in your place:

| Stage | What the agent does | What passes the gate |
|-------|---------------------|----------------------|
| Plan | Settles the issue's scope from the intent, recording each call in `decisions.md` | It traces to the intent's success criteria |
| Design (G1) | Writes the plan and any mockup | The `plan-reviewer` subagent, on a different model, finds nothing critical or high |
| Build | Codes each phase with main-path tests on the issue's branch | The Stop hook's checks, `review-security`, `review-design` for screens, and the verifier running the app |
| Test | Pushes (the pre-push scan runs) and opens the PR | The required CI checks; it fixes each failure at its cause |
| Deploy (G2, G3) | Squash-merges on green; with AWS, the pipeline applies to `dev` and it smoke-tests | Green checks and the apply |
| Maintain | Turns what went wrong into a check or a lesson, then takes the next issue | |

Each time it finishes, the Stop hook sends it back to the next open issue, until the backlog is empty, the time budget is spent, or two turns in a row change nothing. A check that fails three times becomes a `blocked` issue while it moves on. It stops early only before spending past the limit in spec 6, weakening its own floor, or taking real users, customer data or payments, and says why. For a long run without permission prompts, start Claude Code in auto mode. When it stops, it reports what shipped, what's blocked and what it decided. Stop it yourself any time with *"Stop"*, or `bash scripts/autopilot.sh stop "<why>"`.

## 5. Build for production

The same loop, stopping at gates G1 to G4 ([AGENTS.md](../AGENTS.md) rule 5). The ↺ marks a step the agent repeats until it's clean.

| # | Gate | You say | The agent | You |
|:-:|------|---------|-----------|-----|
| 1 | G1 Plan | *"Plan `<the work>`"* | Interviews you on what changes the build, updates the spec, writes the plan, the threat model and any mockups; no code, then stops | ↺ Ask for changes, then approve |
| 2 | Build | `/clear`, then *"Implement the plan"* | In a fresh session, from the plan alone, builds each phase on one branch: abuse-case tests, local checks, a fresh review per phase | |
| 3 | G2 PR | *"Commit and push"* | Asks you to approve the push, then pushes, opens a PR with its Security line, ↺ fixes what the checks find, then asks for review | The second reviewer approves |
| 4 | G3 `dev` | *"Merge it"* | Squash-merges; the pipeline plans `dev` and waits; once applied, the pipeline smoke-tests and scans `dev` with ZAP, and the agent reports | The second reviewer approves the apply |
| 5 | G4 Release | | Confirms the checklist's production rows are done | Run `gh workflow run aws.yml -f target=prod`; the second reviewer approves it |
| 6 | G5 After | | The next day, checks actual cost and the alarms | Anything raised becomes an Incident issue and starts at step 1 |

## 6. Other changes

| When | You say | What happens |
|------|---------|--------------|
| A small fix touching no users, data, auth, endpoints, infrastructure or screens | *"Fix `<the problem>`"* | No plan, the same checks; it waits on the branch for the next PR |
| Dependabot's weekly PRs | *"Check the Dependabot PRs"* | The agent fixes what the checks find |
| A scan on `main` or the weekly scan fails | *"Fix the failed scan on main"* | The agent fixes each finding at its cause |
| A new AWS service | Production: answer when the agent asks. A prototype's agent decides | It adds the permissions to `bootstrap.yaml`; you redeploy the stack before the merge |
| The agent got something wrong | Tell it | It adds a line, or better a check, to `docs/lessons.md` |

## 7. From prototype to production

Say *"Make this project production"*, and the agent does steps 1 to 3 on one branch:

1. From a clone of the template, `uv run --no-project python scripts/new-project.py ../<name> --upgrade --profile production` brings in what a prototype didn't get: the full `AGENTS.md`, `threat-model.md`, `checklist.md`, the security guides and the production workflows. It sets `Profile` to `production`, coverage back to 80 and the `.env` deny rules, keeps every file the project already has, and lists any the template now words differently for the agent to bring in line. The same with `--aws` or `--ui` adds a part later. Then a new decision records the move.
2. It extends the threat model and costs for you to approve.
3. `fail_under` goes back to 80, and it adds the skipped tests, abuse cases included.
4. You go through the trade-offs: each gets its fix, or a named person accepts it.
5. You set up the reviewers (section 2, step 5) and bootstrap the `prod` account.
