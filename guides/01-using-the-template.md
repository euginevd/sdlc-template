# Using the template

How to take a project from an empty repo to a deployed app with your coding agent: what you say, what the agent does, and what you decide, for a fast `prototype` or a gated `production` project. For developers; the agent works from [AGENTS.md](../AGENTS.md), not from this guide, so the prompts in italics are suggestions and your own words do the same job. A tour of every file is in [02-the-files.md](02-the-files.md), the risks the template accepts are in [03-security-trade-offs.md](03-security-trade-offs.md), and how each guardrail works is in [04-the-guardrails.md](04-the-guardrails.md).

## 1. Pick a profile

The agent asks for this first ([AGENTS.md](../AGENTS.md) rules 15 and 24). Section 4 is the prototype's path and section 5 is production's.

| | `prototype`: a working MVP, fast | `production`: secure and gated |
|---|---|---|
| For | No real users, customer data or payments | Anything that has them |
| Approvals | Kickoff only; after that the agent plans, builds, merges and deploys to `dev` on its own | You approve the plan; a second reviewer approves each PR and each deploy, and GitHub enforces it |
| Tests | Main paths and anything sensitive, 50% coverage | Every change, abuse cases included, 80% coverage |
| When unsure | The agent takes the simpler option, says so in its report and keeps going | The agent asks you |
| Trade-offs | All accepted | Each fixed, or accepted by a named person |

Both keep the pre-push scan, the PR security checks, no pushes to `main`, no reading of secrets, and deploys only through the pipeline. In both, the agent asks before a new AWS service, anything that adds cost or a change to its rules, and before a prototype takes real users, customer data, payments or a `prod` deploy (section 7).

## 2. Set up the repo

Once per project, by you. Steps 1 and 2 need the GitHub CLI, signed in with `gh auth login`.

1. **Create it:** `gh repo create <name> --template euginevd/sdlc-template --private --clone`. Keep a repo that deploys to AWS private: on a public repo, anyone signed in to GitHub can download its Terraform plans (trade-offs 5).
2. **Tools and hooks:** `bash scripts/setup.sh`, on every fresh clone: it installs the scanners, uv and Terraform if they're missing, then the push hook, and lists what the machine has. Until it has run, pushes from that clone aren't scanned. `bash scripts/setup.sh --check` lists the same and changes nothing.
3. **Protect `main`:** `bash scripts/protect-main.sh` sets the Actions limits, squash-only merges, GitHub's security features and the `main` ruleset; rerun it after changing it. A private repo needs a paid GitHub plan for the ruleset and the approval environments. On a public repo, also turn on everything under Settings → Advanced Security, which has no API for the script; the AI scans and Agentic autofix use AI credits ([guide 04](04-the-guardrails.md), sections 4 and 7).
4. **AWS, when the project first needs it:** the steps at the top of [bootstrap.yaml](../infra/aws/bootstrap/bootstrap.yaml), once per account: `dev` now, and `prod` (`Target=prod`) before the first `prod` deploy. Until then the `aws` workflow skips itself, so a project can start without an account. Two extras, each off until you set it: `BudgetEmail` emails you as the account's spend nears its monthly budget, and an Infracost API key in the `INFRACOST_API_KEY` secret puts a cost comment on each PR. Then, in Settings → Environments, set Deployment branches to `main` only on each `aws-<env>-apply` environment ([guide 04](04-the-guardrails.md), section 16).
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
| | Builds each phase: code, tests, the checks, `features.md` and `TODO.md`, a local commit | |
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
| 3 | Code | *"Implement the plan"* | Builds each phase: code, tests, the checks, a fresh subagent review, `features.md` and `TODO.md`, a local commit. After the last one, reviews the whole branch, updates `decisions.md` and deletes the plan and its mockups, and `mvp.html` once all its screens are built | |
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
