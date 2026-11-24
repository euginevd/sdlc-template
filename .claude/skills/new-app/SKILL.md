---
name: new-app
description: Adds a new app to this repo with everything CI, Dependabot, deploys and the docs need (AGENTS.md rule 3). Use when an issue or plan adds an app in apps/, such as a web front end, a worker or a second API.
---

# New app

An app needs changes in several files beyond its own folder, and missing one fails quietly (CI skips it, Dependabot never updates it). Work through each step, skip only what doesn't apply, and say which you skipped and why.

1. **The app:** `apps/<app>/`, named in kebab-case. Python joins the uv workspace in the root `pyproject.toml`; TypeScript gets its own `package.json` and an `.npmrc` (`docs/standards.md` 15 and 16). Packages as `AGENTS.md` rule 16 says.
2. **Checks:** a `check_<app>` (or an extension of `check_python` or `check_web`) in `scripts/check.sh`, and a target for it.
3. **CI:** a job in `.github/workflows/ci.yml` that runs `bash scripts/check.sh <target>`, in a pinned container like the others, and the app's folder in the `changes` job so a PR touching it runs that job.
4. **Dependabot:** the app's ecosystem and folder in `.github/dependabot.yml`, in the same form and cooldown as the entries there.
5. **Container,** if it ships as one: `apps/<app>/Dockerfile` meeting `docs/standards.md` 22, and `.env.example` listing each setting.
6. **Infrastructure,** if it deploys: `infra/aws/<app>/`, copied from `infra/aws/api` and named as `docs/standards.md` 13 and 14 say. A new AWS service follows the `deploy` skill 2; production asks first (`AGENTS.md` rule 4).
7. **Docs:** its Stack line in `docs/spec.md` with Run, Talks to and Outside limits; its section and first row in `docs/features.md`; a threat-model data flow and risks if it has users, data, auth or endpoints.
8. **Browser tests,** if it has screens: its main path in `e2e/` (`docs/standards.md` 30).

Finish with `bash scripts/check.sh all` passing, then show that the `changes` job selects the new app: a one-line edit in `apps/<app>/` must make `git diff` match its pattern in `ci.yml`.
