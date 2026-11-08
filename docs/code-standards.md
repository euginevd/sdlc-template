# Code standards

How to write the code, numbered so reviews can cite them. `AGENTS.md` covers what to build and the workflow; these cover how.

## General

1. Keep it simple: the smallest change that meets the spec or plan, for cases that exist now.
2. Correct and clear before clever or fast. Measure before optimising.
3. Names say what; comments say why, in one line.
4. No dead code, commented-out code, unused imports or compat shims.
5. Match the surrounding code. Bring code up to standard before extending it.
6. Use the framework's own way first, checked against the installed version's docs.

## Structure

7. One job per module and per function. Each external service is reached through one module, the only place with its address and settings.
8. Write a literal once, where it belongs. Settings come from environment variables, validated at startup.

## Errors and logs

9. Handle an error only where you can do something useful with it; otherwise let it surface.
10. Fail closed: when a security or payment check can't complete, deny.
11. Log structured JSON with a request ID. Never log secrets or personal data; redact at the source.

## Security

12. Validate every input at the boundary (API, files, queues) against a schema, and reject what doesn't match.
13. Check authorisation on every request, on the server, and deny by default.
14. Use parameterised queries and the framework's escaping; never build SQL, shell commands or HTML from strings.
15. TLS everywhere, and encryption at rest for every data store.
16. Keep personal data in the regions `business-context.md` allows, including model calls.
17. Least privilege for every role, token and job. OIDC from CI to cloud; no long-lived keys.
18. Pin dependencies and commit lock files. Pin CI actions to a commit SHA, with the version in a comment.

## Tests

19. Add tests with each change. Tests never call real models, cloud or paid services; use stubs.
20. Test the abuse cases from `threat-model.md`, such as one user reading another's data.
21. Keep test coverage at 80% or more for new code.

## Terraform

22. One root per unit in `aws/<unit>/`, with remote state, locked and encrypted; copy `aws/api` to start one. Never commit state.
23. `main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`; pin Terraform and providers; commit the lock file.
24. No hardcoded IDs, regions, ARNs, project names or environments; the pipeline passes them.
25. Name resources `${var.project}-<unit>-<what>-${var.environment}`. Every IAM role has the `${var.project}-boundary` permissions boundary. Tags come from the provider's `default_tags`.
26. `fmt`, `validate`, `tflint` and a security scanner clean; skip an intentional finding inline, with the reason. `ignore_changes` only for what other systems change on purpose.

## Languages

27. Python: current stable version, `uv run` for everything, `ruff` to lint and format, `pyright` in strict mode.
28. TypeScript: strict mode, never `any`; ESLint and Prettier.
29. Web: meet WCAG 2.2 AA.

## AI and agents

30. Pass an explicit model ID, never a "latest" alias.
31. Treat model output as untrusted: ask for structured output and validate it against a schema before using it.
32. Keep untrusted content, such as uploaded documents, apart from instructions. It never changes the agent's tools or limits.
33. The model decides; deterministic code acts. Limits, payments and permissions are enforced in code, never in a prompt.
34. Each tool does one thing, with the least privilege it needs.
35. Prompts and model settings live in the repo. Changing them is a code change, with evals in CI.
36. Every model call has a timeout, a token limit and a retry cap.
37. Instructions give the goal, the inputs and what done looks like, not the steps.

## Docs

38. Each fact lives in one place; everywhere else links to it.
39. Keep docs short: tables and one-line rules.
40. Write what's true now. Mark future work *(planned)*.
41. Root files are uppercase (`README.md`, `AGENTS.md`); everything in `docs/` and `guides/` is lowercase kebab-case.
