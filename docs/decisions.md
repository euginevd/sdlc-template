# Decisions

Key decisions, newest last. Never delete one; supersede it with a new entry.

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

**Why:** one set of docs, standards and pipeline; apps in `apps/` and infrastructure in `aws/` change together in one PR.
**Instead of:** a repo per app or per cloud. Split only when owners, access or release cycles differ.

## 4. DevSecOps stages for the lifecycle
2026-11-08 · Accepted

**Why:** security is part of every stage, from the plan to monitoring, and each stage has an owner and an output.
**Instead of:** a build-then-secure process.

## 5. Pre-push scan with gitleaks and Trivy through lefthook
2026-11-08 · Accepted

**Why:** catches secrets, IaC misconfigurations and vulnerable packages before they leave the workstation, for people and agents alike, with free tools that need no account. Pre-push, not pre-commit, so agents committing often aren't slowed down.
**Instead of:** Wiz (needs a licensed tenant), pre-commit (slow on every commit), or no workstation scan. `guides/02-git-hooks.md` compares them.

## 6. The state bucket passed at `terraform init`
2026-11-08 · Accepted

**Why:** keeps the AWS account ID out of the repo, so the code can be made public safely.
**Instead of:** the bucket name written in each unit's `versions.tf`.

## 7. `AGENTS.md` only, no `CLAUDE.md`
2026-11-08 · Accepted

**Why:** one set of agent instructions that Claude Code, Codex, OpenCode, Copilot and Cursor all read. Claude Code reads `AGENTS.md` natively from v2.1.277, and skips it when a `CLAUDE.md` exists.
**Instead of:** a `CLAUDE.md` alongside it. If Claude-only extras are ever needed, add a `CLAUDE.md` whose first line is `@AGENTS.md`.

## 8. Project details in `spec.md`; `AGENTS.md` stays generic
2026-11-08 · Accepted

**Why:** a new project fills in one file. Template improvements to `AGENTS.md` copy into existing projects without merge conflicts. The project name reaches Terraform from the `PROJECT_NAME` repository variable, so the code holds no placeholders.
**Instead of:** project context in `AGENTS.md` and the project name written into each unit.

## 9. Six docs: `tech-stack.md` into `spec.md`, `process.md` into `AGENTS.md`
2026-11-08 · Accepted

**Why:** the template's stack is the same for every project and already lives in `aws/AGENTS.md` and the workflow, so only the app stack is project-specific, and it belongs in the spec. `process.md` repeated `AGENTS.md`'s rules; one copy can't drift.
**Instead of:** eight docs, with the workflow written twice.
