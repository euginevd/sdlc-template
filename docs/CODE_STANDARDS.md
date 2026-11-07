# Code standards

## General

1. Keep it simple. Build only what's asked, for cases that exist now.
2. Correct and clear before clever or fast. Measure before optimising.
3. Names say what; comments say why, in one line.
4. No dead code, commented-out code, unused imports or compat shims.
5. Handle an error only where you can do something useful with it.
6. Match the surrounding code. Bring code up to standard before extending it.

## Structure

7. One way to do each thing: each service is reached through one module, the only place with its address and settings.
8. One job per module and per function. Shared helpers get their own module; never borrow another's.
9. Write a literal once, where it belongs.
10. Use the framework's own way before your own, checked against the installed version's docs.

## Security

11. No secrets in code, config or logs.
12. OIDC from CI to cloud; least privilege for every role, token and job.
13. Pin dependencies exactly; pin CI actions to a commit SHA with the version in a comment.

## Tests

14. Add tests with each change, using stubs for models, cloud and paid services.
15. Never weaken or skip a check to get a green run. Fix the cause.

## Terraform

16. One root per deployable unit, with its own remote state, locked and encrypted. Never commit state.
17. `main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`; pin Terraform and providers; commit the lock file.
18. No hardcoded IDs, regions or ARNs. Tag once, in the provider's `default_tags`.
19. snake_case; `fmt`, `validate`, `tflint` and a security scanner clean. Skip intentional findings inline, with the reason.
20. Plan on the PR; apply only the reviewed plan, after approval. `ignore_changes` only what other systems change on purpose.

## Languages

21. Python: always `uv run`; `ruff`, type hints, current stable Python.
22. TypeScript: strict mode, never `any`.

## LLMs and agents

23. Pass an explicit model ID, never a "latest" alias.
24. Instructions give the goal, the inputs and what done looks like, not the steps. What must always happen is code.
