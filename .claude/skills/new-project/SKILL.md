---
name: new-project
description: Starts a new project from this template, gate G0: interviews the developer one question at a time (name, intent, profile, parts, limits), builds the repo with only the files those answers need, drafts the spec, docs and backlog, publishes and protects the repo, and hands over to the agent's long run. Use when the user says "new project", "start a project", "kick off" or "create a repo from the template".
---

# New project

The one time the developer is asked anything: after this, a prototype's agent works on its own (its AGENTS.md rule 7). So ask everything the build needs now, one question at a time, each with your recommendation and why, and say what you'll assume if they skip it. Probe a vague answer ("for everyone", "fast") until a person could check it.

Runs in a clone of the template on the developer's machine, with `gh` signed in: a cloud session can't create a repo, so there, say so and give the steps as commands.

## Ask

1. **Ready:** `git switch main && git pull` here, then `gh auth status`. Fix either before going on.
2. **Name:** lowercase with hyphens. Check it's free (`gh repo view <owner>/<name>` should fail). It goes in `../<name>`, beside this clone, unless they say otherwise.
3. **Intent,** `docs/intent.md`'s headings in order: problem, outcome (the few things the first version must do, by screen), users and systems, constraints, success criteria, open questions. Then what's out there to borrow from: products, libraries, APIs.
4. **Read it back** in a few short lines, in their words, and ask what's wrong or missing. Repeat until they say it's right.
5. **Profile:** `prototype` builds, merges and ships to `dev` on its own for hours; `production` stops for the developer and a second reviewer at each gate. Recommend `production` if the intent has real users, customer data or payments.
6. **Visibility:** `public` for personal or portfolio, `private` for work (the `main` ruleset needs a paid plan).
7. **Parts,** each recommended from the intent: AWS (deploys there now or later) and screens (has a UI). What's not picked isn't copied; adding it later means copying from the template.
8. **Limits:** the monthly spend limit, which the agent never passes without stopping (spec 6). A prototype also gets its run's time budget: recommend 8 hours.
9. **Production only:** the spec's Business section, one line at a time: the business, its size, regulators, where data must stay, risk appetite, systems it fits with, who owns the rules, tone.
10. **Confirm:** one short table of every answer, what the repo gets and what it doesn't. Wait for their yes: the next steps create a repo on GitHub.

## Build

11. `uv run --no-project python scripts/new-project.py ../<name> --name <name> --profile <profile> --visibility <visibility>`, with `--aws` and `--ui` as picked. It writes only the files those answers need, records the profile, repo and name, and lists each line still naming a file the project doesn't have. Work in `../<name>` from here on.
12. **Tidy:** fix each listed line, rewording or deleting it; `uv lock`, as the project's name changed; `uv run --no-project python scripts/check-refs.py` must say ok.
13. **Docs,** replacing every *(to fill in)* line in `docs/` (CI's `kickoff` check fails while one is left); a prototype writes "none" where a line doesn't apply:
    - `intent.md`: their answers, in their words, with Owner, `Status: Building` and today's date.
    - `spec.md`: drafted from the intent: AWS accounts and region if picked, the Stack, Done when, Rules (spec 6 holds the spend limit and the ASVS level: 1 for a prototype, 2 for production), and Not for now; production's Business section too.
    - `decisions.md` 1: the profile and why, who owns the code, and the trade-offs (production: from `guides/03-security-trade-offs.md`, each fixed or accepted by a named person; a prototype accepts them all).
    - With screens: `docs/web/design-system.md` for the project, and the MVP's main screens mocked up in `docs/web/mockups/mvp.html`.
    - Production: `threat-model.md` and, with AWS, `docs/aws/costs.md`, extended for the intent. A prototype keeps the starter costs.
    - A prototype deletes the `.env` deny rules from `.claude/settings.json` (its rule 4 lets it read `.env`).
    - Then `bash scripts/check.sh all` must pass.
14. **Publish:** `bash scripts/setup.sh` first, so the first push is scanned; then `git add -A`, `git commit -m "Start <name> from sdlc-template"` and `gh repo create <name> --<visibility> --source . --push`; then `bash scripts/protect-main.sh`, adding `production` for production. Pass on anything it lists to do by hand.
15. **Backlog:** `gh label create blocked --description "Failed three times; needs a person"`, then the build as GitHub issues in order, oldest first: each a small, shippable slice with the intent's headings and its own checkable success, the walking skeleton first. A prototype's agent builds them in this order.

## Hand over

16. Production stops here at G0: the developer approves the spec, its Business section, the threat model, costs, design system and mockup before any issue is built.
17. Tell the developer to open `../<name>` in VS Code and start Claude Code there, as its rules and hooks load only in a session started in it. A prototype then says *"Go"*: its agent turns on the autopilot and builds the backlog until it's done or the time budget is spent. For a long run without permission prompts, start Claude Code in auto mode.

End with the repo's URL and folder, the profile and parts, the issues in order, what's left to do by hand, and the next step.
