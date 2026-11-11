# Spec

A starter: it describes the sample the template ships, a health-check API, and each *(to fill in)* line says what to write. Kickoff fills it in from your notes. The user approves every change (a prototype: [AGENTS.md](../AGENTS.md) rule 24).

## Project

Profile: *(to fill in)* `prototype` or `production`.

1. Name: `starter`
2. Problem: *(to fill in)* what's slow, costly or missing today, and for whom.
3. Goal: *(to fill in)* what's true once this works.
4. Users: *(to fill in)* who uses it, and what each of them does.
5. AWS: *(to fill in)* the accounts, region and environments. The pipeline deploys `dev` on merge and `prod` by hand.

## Stack

Template defaults: GitHub Actions, Terraform on AWS, the pre-push scan and the PR security checks.

6. `api`: Python on Lambda behind an HTTP API, the template's sample. Keep it, build on it or replace it.

## Done when

7. `GET /health` returns `{"status": "ok"}`.
8. *(to fill in)* one line for each result a user can see.

## Rules

9. `/health` is public and returns nothing from the request.
10. *(to fill in)* the limits that hold whatever else changes: data, money, monthly spend and the security baseline, as an OWASP ASVS level (1 for a prototype, 2 for production).

## Not for now

11. *(to fill in)* what's deliberately left out.
