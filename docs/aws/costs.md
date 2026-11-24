# Costs

A starter: what the sample the template ships costs in `dev`, for the start to extend; part of the AWS module, which a project not on AWS doesn't get. Costs are approximate monthly figures. The day after each deploy, actual cost is compared with this file (the `deploy` skill 6).

## Resources

1. Lambda (`api`): under $1 at `dev` traffic, driven by requests, nothing when idle. Cut it by right-sizing memory.
2. HTTP API: under $1 at `dev` traffic, driven by requests. Throttling keeps floods from running up the bill.
3. CloudWatch logs: under $1 at `dev` traffic, driven by log volume. Cut it with 30-day retention and no debug logs in `prod`.
4. *(to fill in)* each resource the project adds, and each paid outside service such as a model API, written like the three above: its rough monthly cost, what drives it and how to cut it. An outside service's key gets its own credit limit, since no budget sees it.

## Budget and alerts

5. `dev` budget: the monthly limit in spec 6, set as `MonthlyBudgetUsd` (default $50) on the bootstrap, which emails as spend nears it ([guide 04](../../guides/04-the-guardrails.md) section 21).
6. `prod` budget, production only: set here after the first full month of real use.
7. Each PR that changes `infra/aws/` gets a cost comment once `INFRACOST_API_KEY` is set; it prices resources, not usage such as model tokens ([guide 04](../../guides/04-the-guardrails.md) section 14).
