---
name: kickoff
description: Gate G0, once per project made from the template (AGENTS.md rule 7): checks the setup, turns intent.md into the spec and the first issue, and fills in docs/. Use when the user starts a new project from the template, or says "kick off".
---

# Kickoff

CI's `kickoff` check fails while a to-fill-in line is left once a profile is set. A repo made with the `new-project` skill already has its intent, profile, repo type and parts: skip what's answered.

1. Check the one-time setup in guide 01 section 2 (`guides/01-using-the-template.md`) is done: run `bash scripts/setup.sh --check`, and ask whether `protect-main.sh` has run and, once AWS is wanted, the bootstrap. Walk the developer through any step that's missing before going on. Read `docs/intent.md`; ask the profile and the repo type (personal or portfolio: public; work: private) unless it gives them, and record both in `docs/spec.md`.
2. If `intent.md` still has lines to fill in, offer two ways: the user edits it, or the agent interviews them in chat. The interview goes heading by heading (problem, outcome, users, constraints, success), one question at a time, each with a recommendation, and probes vague answers ("for everyone", "fast") until a person could check them; the agent writes the answers in, in the user's words, for them to check.
3. Draft `spec.md` from `intent.md`, ask about gaps that change the build (a prototype fills small ones itself and says so), and open the first item as a GitHub issue.
4. Replace every other line marked to fill in, in `docs/`, fixing numbered references that move, or delete a doc that doesn't apply. A prototype writes "none" for a line that doesn't apply yet, such as regulators or tone, rather than asking. A prototype keeps the starter `threat-model.md` and `costs.md`, deleting only their to-fill-in lines.
5. Production picks the deploy target by a short spike: what each managed service refuses or limits, in `decisions.md`. A prototype uses the starter's Lambda unless `intent.md` says otherwise.
6. With UI: `docs/web/design-system.md` and a mockup of the MVP's main screens in `docs/web/mockups/mvp.html`. A repo made without `new-project` that has no UI deletes `docs/web/`, and one without AWS `docs/aws/`.
7. Record a decision on the profile, who owns the code and the trade-offs in guide 03. A prototype accepts them all, deletes the `.env` deny rules from `.claude/settings.json` (rule 4 lets it read `.env`), and keeps building. Production fixes each trade-off or names who accepts it, and the user approves `spec.md` (Business section included), the design system and mockup, `threat-model.md` and `costs.md`.
8. Rename the project from `starter` in the README, `spec.md` and `pyproject.toml` (then `uv lock`); a prototype sets `fail_under = 50` there.
