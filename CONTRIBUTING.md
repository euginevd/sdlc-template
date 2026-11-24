<div align="center">

# Contributing

**Every change, by a person or a coding agent, goes through the same checks. The project's profile sets how much planning and approval it needs.**

</div>

1. **Setup:** `bash scripts/setup.sh` once per clone installs the tools and hooks; `--check` reports what's missing. Read [AGENTS.md](AGENTS.md) and [docs/standards.md](docs/standards.md): the rules for agents and people alike.
2. **Start from an issue:** each change answers one GitHub issue; one the spec doesn't cover starts with an update to [docs/spec.md](docs/spec.md).
3. **Follow the profile:** [guide 01](guides/01-using-the-template.md), section 4 for a `prototype`, section 5 for `production`.
4. **Check before pushing:** `bash scripts/check.sh` runs what CI runs. Never push to `main` or skip a hook.
5. **Pull request:** one per branch, from the template, with its **Security** line and `Closes #<issue>`. Every check passes and findings are fixed at their cause.
6. **Merge:** update the branch if `main` has moved, then squash-merge: once checks pass in a `prototype`, once a second reviewer approves in `production`.

Security issues go through [SECURITY.md](SECURITY.md), never a public issue or PR. [MIT licence](LICENSE).
