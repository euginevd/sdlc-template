# Process

Work follows the DevSecOps stages in the README: Plan, Code, Build, Test, Release, Deploy, Operate, Monitor. Security is part of every stage, not a step at the end.

## Plan

When asked to plan, write the plan to `docs/PLAN_<NAME>.md` and write no code.

- Start with the design: the parts, what each is for, and why. Check it against `docs/CODE_STANDARDS.md`.
- Name the security risks the work adds (users, data, secrets, public endpoints) and how each is handled. Once there are any, keep `docs/SECURITY.md` up to date.
- Split the work into phases, each building on the last.
- Give each phase success criteria you can verify yourself, as checkboxes.
- Then stop and wait to be asked to build it.

## Code, Build and Test

For each change, or each phase of a plan:

1. Build it, with tests where the project has them.
2. Run the checks in `docs/TECH_STACK.md` and fix what fails.
3. Review it (below) and fix what the review finds.
4. Update the docs it affects, `docs/STATUS.md` always. Tick off the plan's criteria.
5. Commit with a one-line message.

## Review

The checks show the code works, not that it's fit to merge. Every change gets a review before it's committed.

- The reviewer is a fresh subagent that didn't write the code. Give it `docs/CODE_STANDARDS.md` and the diff, and ask it to review as a strict senior engineer deciding whether to merge, security included.
- Fix everything it would block on. If you disagree with a finding, say so in your report instead of skipping it.

## Release and Deploy

1. Push the branch. The pre-push scan runs; fix what it finds and push again.
2. Open a PR. The workflows run the checks and the Terraform plan.
3. Merge once every check passes, then delete the branch.
4. The apply runs after the user approves it in the `-apply` environment.

## Operate and Monitor

When a plan's last phase is done, review the whole branch against `main` the same way, then report what was built, what the reviews found and what you changed. Then update `docs/STATUS.md` and `docs/DECISIONS.md`, and delete the plan and its line in `AGENTS.md`; git history keeps it.

Anything unexpected from the account, the pipeline or the tools goes in `guides/03-findings.md`. Cost-bearing resources go in `docs/FINOPS.md` once there are several.

## Rules

- Never use `git commit --no-verify` or `git push --no-verify`.
- Never lower a threshold, turn off a rule or exclude a file to get a green run. If a rule looks wrong, stop and ask.
- Report results faithfully: what passed, what failed and what you skipped.
