<!-- Template for docs/plan-<name>.md (AGENTS.md rule 9), in the four sections of Anthropic's plan.md: copy it, keep it to two pages at most, enough for a fresh session (`/clear`) to build from alone, and delete this line and anything that doesn't apply. -->
# Plan: <name>

Issue: #<number>. Spec items: <numbers>. Features: <numbers>. Threat-model risks: <IDs>. Profile: <prototype or production>. Review level: <low, medium or high, by blast radius (the `review-security` skill)>.

Approach: what changes and how, in a few lines, and what it leaves alone. Decided against: the other options, and why not.

## Files that change

Each file added or changed, with what changes in it; a file not listed here is out of scope.

## Order of work

The phases in the order they're built, each one shippable on its own.

### 1. <what this phase delivers> (<the spec, feature and risk IDs it meets>)

- [ ] <a result someone can check>
- [ ] New cloud service: a walking skeleton applied to `dev` and called once (the `deploy` skill)
- [ ] Tests cover it (prototype: the main path; production: abuse cases too)
- [ ] `bash scripts/check.sh` passes; the review skills and the verifier are clean (prototype: once, after the last phase)

## Risks

What could go wrong, and how each is avoided; "None" where a kind doesn't apply.

- Security: each risk with its control and threat-model ID, or "None: touches no users, data, auth or endpoints".
- Constraints: each constraint in `intent.md` and Rule in the spec this change touches, and what meets it.
- Riskiest step: the one most likely to break something, and how it's tested first.
- Open questions: each still open, or a conflict between docs, with who decides; a prototype takes the simpler option and says so.
- Ask first: new AWS services, costs, packages or rule changes, each with why; production needs a yes before building, a prototype lists what it decided (AGENTS.md rule 4).

## Proof

Each spec item, feature and risk above, with the test, screenshot or command output that shows it's done.
