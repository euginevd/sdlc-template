# Features

What each app does today, one row per feature, added in the PR that builds it ([AGENTS.md](../AGENTS.md) rule 10). Planned work is the open GitHub issues; the rules every feature keeps are in [spec.md](spec.md). Numbered across the file so reviews can cite them (features 2).

| App | For | Link |
|---|---|---|
| [`api`](#api) | *(to fill in)* who uses it | *(to fill in)* its local or deployed address |

## `api`

One section per app, in the table's order, each listing what it offers its audience.

| # | Feature | Status | Issue | PR |
|---|---|---|---|---|
| 1 | Health check, `GET /health` (spec 3) | Done | | Starter |

## Behind every app

What no single app owns, such as an agent, a check every request goes through, or a deployment.

| # | Feature | Status | Issue | PR |
|---|---|---|---|---|
| 2 | Pipeline: app checks, security scans, and a Terraform plan and apply through the `aws` workflow: a merge to `main` applies to `dev` (production: once a second reviewer approves), `prod` is a manual run | Done | | Starter |

Status: Done, or Removed with the reason; a removed feature keeps its number.
