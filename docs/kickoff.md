# Kickoff

Gate G0, once per project made from the template ([AGENTS.md](../AGENTS.md) rule 13). CI's `kickoff` check fails while a to-fill-in line is left once a profile is set.

1. Ask the profile, unless the notes give it, and record it in `spec.md`. It's the one question a prototype's kickoff asks.
2. Replace every line marked to fill in, in `docs/`, fixing numbered references that move, or delete a doc that doesn't apply. A prototype keeps the starter `threat-model.md` and `costs.md`, deleting only their to-fill-in lines.
3. Pick the deploy target by a short spike: list what each managed service refuses or limits, in `decisions.md`.
4. With UI: `design-system.md` and a mockup of the MVP's main screens in `docs/mockups/mvp.html`.
5. Record a decision on the profile, who owns the code and the trade-offs in guide 03. A prototype accepts them all, deletes the `.env` deny rules from `.claude/settings.json` (rule 26 lets it read `.env`), and keeps building; the user reviews the docs when they like. Production fixes each trade-off or names who accepts it, and the user approves `spec.md` (Business section included), the design system and mockup, `threat-model.md` and `costs.md`.
