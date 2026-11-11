# Status

What's built, how to run it, what's missing and what's next. The agent keeps it current in the same commit as each change; each feature's status is in [features.md](features.md).

## Built

1. `api`: a Lambda behind a throttled HTTP API with access logs; its features are in `features.md`.
2. Pipeline: app checks, security scans, and a Terraform plan and apply through the `aws` workflow.

## Running it

3. Set up each clone once: `bash scripts/setup.sh`.
4. Run the tests: `uv run pytest`.
5. Check: `AGENTS.md` → Commands.
6. Deploy: a merge to `main` applies to `dev` after approval; `prod` is a manual run of the `aws` workflow.

## Known gaps

7. Kickoff hasn't happened: the lines marked *(to fill in)* in `docs/` are placeholders.
8. Nothing is deployed: the `aws` workflow skips itself until the AWS account is bootstrapped.

## Next

9. Kick off: [guides/01-using-the-template.md](../guides/01-using-the-template.md), section 3.
