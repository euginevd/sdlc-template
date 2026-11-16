<!-- Skeleton for docs/plan-<name>.md (AGENTS.md rule 9): copy it, keep it to two pages at most, and delete this line and any section that doesn't apply. -->
# Plan: <name>

Spec items: <numbers>. Features: <numbers>. Threat-model risks: <IDs>. Profile: <prototype or production>.

## Design

What changes and how, in a few lines, and what it leaves alone.

Files: <each file added or changed>.

## Security risks

Each risk with its control and its threat-model ID, or "None: touches no users, data, auth or endpoints".

## Constraints

Each Security line in the brief and each Rule in the spec this change touches, and what meets it.

| Constraint | Met by |
|---|---|
| <brief Security line or spec rule> | <the design choice, control or test> |

## Open questions and concerns

Each question still open, and each conflict between rules or docs, with who decides it; a prototype takes the simpler option and says so here.

## Phases

### 1. <what this phase delivers> (<the spec, feature and risk IDs it meets>)

- [ ] <a result someone can check>
- [ ] New cloud service: a walking skeleton applied to `dev` and called once ([deploy.md](deploy.md))
- [ ] Tests cover it (prototype: the main path; production: abuse cases too)
- [ ] `bash scripts/check.sh` passes; the review skills and the verifier are clean (prototype: once, after the last phase)

## Proof

Each spec item, feature and risk above, with the test, screenshot or command output that shows it's done.

## Ask first

New AWS services, costs, packages or rule changes, each with why: production needs a yes before building; a prototype lists what it decided (AGENTS.md rule 4).
