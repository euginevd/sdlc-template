# Spec

The one file to fill in for each project, by hand or by asking the agent to draft it. Replace the examples, every `<…>` and every *(…)*. The user approves every change.

## Project

- Name: `travel-claims`
- Problem: *(what's wrong or missing today, and for whom)*
- Goal: *(what changes once it's built, in one sentence)*
- Users: *(each kind of user, and what they need from it)*
- AWS: account `<aws-account-name>`, region `ap-southeast-2`, environments `dev` *(add `prod` when it's needed)*.
- Developer machine: Windows, with PowerShell or Git Bash.

## Stack

Template defaults: GitHub Actions, Terraform on AWS and the Gitleaks and Trivy pre-push scan. Add one line per app:

- `<app>`: *(language and framework)*, hosted on *(service)*. Checks: `<lint>`, `<types>`, `<tests>`.

## Done when

1. *(A result anyone can verify, such as "a user can sign in and see their dashboard")*

## Rules

- *(Constraints that always hold: data, cost, access, compliance)*

## Not for now

- *(What's deliberately out, so nobody builds it early)*
