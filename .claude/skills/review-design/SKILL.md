---
name: review-design
description: Design review of a changed screen against its mockup, this repo's design system and its web UI standards (AGENTS.md rule 10). Use when a phase changes a page or component, or when asked for a design or accessibility review. Reports findings; never edits code.
model: sonnet  # A different model from the session that wrote the code, for a second opinion; haiku if that session runs Sonnet.
---

# Design review

Review the screens this branch changes, as a user would see them. You report; the agent that wrote the code fixes as the `pull-request` skill 1 says, then runs this review again until nothing critical or high is left. Run in a fresh context, not the author's.

## Scope

1. The changed screens: from `git diff origin/main...HEAD`, the pages and components touched.
2. The standards, read first: the screen's mockup in `docs/web/mockups/` (or `mvp.html`), `docs/web/design-system.md` (tokens, motion, imagery, components, "Not this" and "This project") and `docs/standards.md` 25 to 29.
3. The Web apps section of `docs/lessons.md`.

## Look

Run the app locally and screenshot each changed screen, light and dark:

1. At the developer's window size and at 1440×900; on a phone at 500px wide (headless Chrome won't go narrower).
2. In each state: loading, empty, error with a retry, and full (standards 28).
3. With reduced motion on, so animations are settled (standards 26).

## Check

1. **Mockup:** layout, hierarchy and content match it; any difference is deliberate and noted.
2. **Tokens:** colours, type, spacing, radius and shadow come from the design system's tokens as CSS variables, never raw values (standards 27).
3. **Accessibility:** contrast 4.5:1 for text and 3:1 for controls and focus; a visible focus ring; targets at least 24×24px; every control has a name; status is a word plus an icon, never colour alone (25, 26). Run axe where the app has it.
4. **Motion and imagery:** as the design system says: purposeful, `transform` and `opacity` only, nothing looping; real imagery, no illustrations.
5. **AI output:** labelled, with its reasons, sources and how to ask for a person (29).
6. **Words:** plain, specific and in sentence case; buttons say what happens; errors say what to do next.
7. **Not this:** nothing from the design system's "Not this" list.

## Report

A list, most severe first; "No findings" if clean; at most five low findings, the ones most worth fixing. Each finding:

- **Severity:** high (blocks a user or fails WCAG AA), medium (off the mockup or tokens), low (polish).
- **Where:** the screen, state and size, with the `path:line` that causes it.
- **What and why:** one line, citing the standard or design-system number.
- **Fix:** one line.

Attach the screenshots you took, and list any state you couldn't reach and why.
