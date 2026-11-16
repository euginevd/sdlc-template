<!-- Skeleton for docs/plan-<name>.md (AGENTS.md rule 9): copy it, keep it to two pages at most, and delete this line and any section that doesn't apply. -->
# Plan: <name>

Spec items: <numbers>. Profile: <prototype or production>.

## Design

What changes and how, in a few lines: the apps, units and data it touches, and what it leaves alone.

## Security risks

Each risk with its control and its threat-model ID, or "None: touches no users, data, auth or endpoints".

## Phases

### 1. <what this phase delivers>

- [ ] <a result someone can check>
- [ ] New cloud service: a walking skeleton applied to `dev` and called once ([deploy.md](deploy.md))
- [ ] Tests cover it (prototype: the main path; production: abuse cases too)
- [ ] Checks pass and the subagent review is clean (prototype: one review, after the last phase)

## PR groups

1. Phases 1–2: <title>, one branch per work session (AGENTS.md, the box at the top)

## Ask first

New AWS services, costs or rule changes: production needs a yes before building (AGENTS.md rule 4); a prototype lists what it decided. New packages, each checked as rule 16 says.
