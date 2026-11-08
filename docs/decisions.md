# Decisions

A worked example: `travel-claims`. Key decisions only, newest last, each with why and what it replaced. Never delete one; add a new one that supersedes it.

1. **The agent decides; code pays** (2026-11-10). Why: a model can be talked into a wrong answer, so limits and payments must be enforced where no prompt can reach (spec 15). Instead of: letting the agent call the payment API.
2. **Lambda for the API and the agent** (2026-11-10). Why: claims arrive in bursts, there's nothing to run between them, and the team already deploys Lambda with Terraform. Instead of: EKS, which suits a larger platform team, or AgentCore Runtime.
3. **Claude on Bedrock, Australian inference profile** (2026-11-12). Why: claim data must stay in Australia, and Bedrock keeps the model inside the AWS account's controls (spec 16). Instead of: a model provider's own API, which sends data overseas.
4. **Automatic payment under $1,000** (2026-11-20). Why: most claims are small and clear-cut; the claims operations lead set the limit, and larger claims still need a handler (spec 11). Instead of: a handler signing off every claim.
