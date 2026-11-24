# Spec

The requirements and design agreed from [intent.md](intent.md) at the start, and changed as each issue is approved ([AGENTS.md](../AGENTS.md) rules 4 and 8): the intent says what and why, this says what gets built. It starts out describing the template's sample, a health-check API. What each feature does is its row in [features.md](features.md), not a line here.

## Business

Who the business is, unnumbered so the spec's numbers stay put. The same for every project for this business: change it only when the business changes, and copy it into the next project's spec.

- Business: *(to fill in)* its name, what it does and where.
- Size: *(to fill in)* staff, the team this is for, and the volume it handles.
- Regulators and laws: *(to fill in)* the ones that apply to its data and decisions, or none.
- Data: *(to fill in)* where customer data must stay.
- Risk appetite: *(to fill in)* what it won't risk, and how changes reach `prod`.
- Systems: *(to fill in)* the systems of record, sign-in and payments this must fit with.
- People: *(to fill in)* who owns the rules the software applies, and who approves new data flows.
- Tone: *(to fill in)* how it speaks to its customers.

## Project

Profile: *(to fill in)* `prototype` or `production`.

Repo: *(to fill in)* `personal` (public) or `work` (private).

Name: `starter`.

1. AWS: *(to fill in)* the accounts, region and environments. The pipeline deploys `dev` on merge and `prod` by hand.

## Stack

Template defaults: GitHub Actions, Terraform on AWS, the pre-push scan and the PR security checks.

Each app with its language, how to run it locally, what it may and may never call, and each outside service's limits.

2. `api`: Python on Lambda behind an HTTP API, the template's sample. Keep it, build on it or replace it.
   - Run: no local server; its tests exercise the handler, and on `dev` it's `GET <api url>/health`.
   - Talks to: nothing; only the HTTP API calls it.
   - Outside limits: none.

## Done when

3. `GET /health` returns `{"status": "ok"}`.
4. *(to fill in)* what done means for the MVP as a whole, from `intent.md`'s success criteria as agreed; each feature's own result is its row in `features.md`.

## Rules

5. `/health` is public and returns nothing from the request.
6. *(to fill in)* the limits that hold whatever else changes: data, money, monthly spend and the security baseline, as an OWASP ASVS level (1 for a prototype, 2 for production).

## Not for now

7. *(to fill in)* what's deliberately left out.
