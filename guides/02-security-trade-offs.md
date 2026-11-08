# Security trade-offs

The risks the template accepts, each with why it's a risk and the fix for production. Numbered so reviews can cite them (trade-offs 1). An accepted risk is a decision: change it here, never by weakening a check.

1. **The agent works as you on GitHub.** *Why it's a risk:* it runs `gh` with your token, so it could approve its own deploy, edit the apply environments or delete the ruleset; only `AGENTS.md` rules 20 and 21 ask it not to. *Production fix:* give the agent its own fine-grained token without Administration, Deployments or Environments permissions, so GitHub refuses those calls, and add deny rules in `.claude/settings.json` as a second layer.
