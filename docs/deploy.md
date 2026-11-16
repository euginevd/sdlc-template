# Deploy

How the agent takes a change to AWS, gates G3 to G5 ([AGENTS.md](../AGENTS.md) rules 5 and 12). Build and test locally first, with stand-ins for cloud services, until the user bootstraps AWS.

1. Every bootstrap has an AWS Budgets alert (`BudgetEmail`) and a read-only troubleshoot role with a CLI user that can only assume it. How wide its permissions go, per profile: rule 4.
2. A new cloud service starts as a walking skeleton: phase 1 applies its smallest resource to `dev` and calls it once. Production adds one new AWS service per PR, once the last has applied; a prototype may batch skeletons.
3. Test against the target engine's limits, not just its local stand-in (known-mistakes 16 to 18).
4. Troubleshoot from the read-only role's logs before guessing.
5. First deploy (G3): every fix goes on the one branch until the apply is green, each adding its known mistake. Then smoke-test the main path on `dev`.
6. The day after a deploy (G5): compare Cost Explorer with `costs.md`. A gap of 2x or more is a finding: fix `costs.md` and report it.
7. A prototype's settings tear down cleanly, with no deletion protection. Teardown keeps the bootstrap until the agent confirms the account is empty ([guides/05-aws-cleanup.md](../guides/05-aws-cleanup.md)).
