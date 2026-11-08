# Decisions

Key decisions only, newest last. Never delete one; supersede it with a new entry.

## 1. GitHub and Terraform for every project
2026-11-08 · Accepted

**Why:** one pipeline, one IaC tool and one set of standards across projects; each change is a reviewed plan.
**Instead of:** a tool per project, or CloudFormation or CDK for the app infrastructure.

## 2. CloudFormation for the bootstrap
2026-11-08 · Accepted

**Why:** it creates the pipeline's roles and state bucket, so it must exist before the pipeline; deleting one stack removes it all.
**Instead of:** Terraform, which can't create its own state bucket and roles without a separate state.

## 3. One repo per product
2026-11-08 · Accepted

**Why:** one set of docs, rules and pipeline; apps in `apps/` and infrastructure in `aws/` change together in one PR.
**Instead of:** a repo per app or per cloud. Split only when owners, access or release cycles differ.

## 4. No account IDs or project names in the code
2026-11-08 · Accepted

**Why:** the pipeline passes them in: the project name is the repo name, and the state bucket and environment come from repository variables. The code can go public safely and needs no placeholders.
**Instead of:** writing them into each Terraform unit.

## 5. Pre-push scan with Gitleaks and Trivy through lefthook
2026-11-08 · Accepted

**Why:** catches secrets, IaC misconfigurations and vulnerable packages before they leave the machine, for people and agents alike, with free tools that need no account. Pre-push, so agents committing often aren't slowed down.
**Instead of:** Wiz (needs a licensed tenant), a pre-commit scan, or no workstation scan.

## 6. One generic `AGENTS.md`, no `CLAUDE.md`
2026-11-08 · Accepted

**Why:** every coding agent reads `AGENTS.md`, and Claude Code skips it when a `CLAUDE.md` exists. Project details live in `docs/spec.md`, so the rules are identical in every project and template updates copy across cleanly.
**Instead of:** tool-specific files, or project details in `AGENTS.md`.
