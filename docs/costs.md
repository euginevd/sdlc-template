# Costs

A starter: what the sample the template ships costs in `dev`, for kickoff to extend. Optional: delete it if the project has little that costs money. Costs are approximate monthly figures.

## Resources

1. Lambda (`api`): under $1 at `dev` traffic, driven by requests, nothing when idle. Cut it by right-sizing memory.
2. HTTP API: under $1 at `dev` traffic, driven by requests. Throttling keeps floods from running up the bill.
3. CloudWatch logs: under $1 at `dev` traffic, driven by log volume. Cut it with 30-day retention and no debug logs in `prod`.
4. *(to fill in)* each resource the project adds, written like the three above: its rough monthly cost, what drives it and how to cut it.

## Budget and alerts

5. `dev` budget: the monthly limit in spec 10, set as `MonthlyBudgetUsd` (default $50) on the bootstrap, which emails as spend nears it ([guide 04](../guides/04-the-guardrails.md) section 21).
6. `prod` budget, production only: set here after the first full month of real use.
7. Each PR that changes `infra/aws/` gets a cost comment once `INFRACOST_API_KEY` is set; it prices resources, not usage such as model tokens ([guide 04](../guides/04-the-guardrails.md) section 14).
