---
name: new-project
description: Makes a new project's repo from this template and walks the developer through it, one question at a time: the name, the intent, the profile and the parts it needs, then creates the repo with only those parts, sets it up and hands over to kickoff. Use when the user says "new project", "start a project", or "create a repo from the template".
---

# New project

Runs in a clone of the template, on the developer's machine: it needs `gh`, signed in. A cloud session can't create a repo, so there, say so and give the steps as commands.

The developer is walked through everything. Ask one question at a time, each with your recommendation and why, and say what you'll assume if they skip it. Ask only what changes the new repo; the rest waits for kickoff.

1. **Ready:** `git switch main && git pull`, then `gh auth status`. Fix either before going on.
2. **Name:** the repo name, in lowercase with hyphens. Check it's free (`gh repo view <owner>/<name>` should fail) and say where it goes: `../<name>`, beside this clone, unless they want somewhere else.
3. **Intent:** go through `docs/intent.md`'s headings in order: problem, outcome, users and systems, constraints, success criteria, open questions. Probe a vague answer ("for everyone", "fast") until a person could check it. Ask what's out there to borrow from (its Research section), or note it for kickoff.
4. **Check it back:** read the intent back in a few short lines, in their words, and ask what's wrong or missing. Repeat until they say it's right.
5. **Profile** (`AGENTS.md` rule 4), explained in two lines: `prototype` builds and ships to `dev` on its own; `production` stops for approval and a second reviewer. Recommend `production` if the intent has real users, customer data or payments, and `prototype` otherwise.
6. **Visibility:** `public` for a personal or portfolio project, `private` for work. A private repo needs a paid GitHub plan for the `main` ruleset.
7. **Parts**, each recommended from the intent:
   - AWS: will it deploy to AWS, now or later? Without it, `--no-aws` drops `infra/`, the `aws` and `images` workflows, `docs/aws/`, the `deploy` skill and the cost report. Adding them back later means copying them from the template.
   - Screens: does it have a UI? Without one, `--no-ui` drops `docs/web/` and the `review-design` skill.
8. **Confirm:** one short table of the answers, what's kept and what's dropped. Wait for their yes: the next step creates a repo on GitHub.
9. **Make it:** `uv run --no-project python scripts/new-project.py ../<name> --name <name> --profile <profile> --visibility <visibility>`, plus `--no-aws` and `--no-ui` as answered. It copies only what's needed, records the profile and repo in `docs/spec.md`, and lists each line that still names a removed file.
10. **Tidy it,** in the new folder:
    - Write the intent into `docs/intent.md` in their words, with Owner, `Status: Idea` and today's date.
    - Fix each line the script listed: reword it or delete it, so nothing points at a removed file. Then `uv run --no-project python scripts/check-refs.py` must say ok.
11. **Publish it,** in the new folder: `bash scripts/setup.sh` first, so the first push is scanned. Then `git add -A`, `git commit -m "Start <name> from sdlc-template"` and `gh repo create <name> --<visibility> --source . --push`. Then `bash scripts/protect-main.sh`, adding `production` for production, and pass on anything it lists as left to do by hand.
12. **Hand over:** the new repo's rules and hooks load only in a session started there. Tell them to open the new folder in VS Code, start Claude Code there and say *"Kick off"*. Kickoff then skips what's already answered.

End with what was made (the repo's URL and folder, its profile and parts), what's left to do by hand, and the next step: kickoff in the new folder.
