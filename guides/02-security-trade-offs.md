# Security trade-offs

The risks the template accepts, each with why it's a risk and the fix for production. Numbered so reviews can cite them (trade-offs 1). An accepted risk is a decision: change it here, never by weakening a check.

| # | Risk | Why it's a risk | Production fix |
|:-:|------|-----------------|----------------|
| 1 | The agent shares the developer's GitHub identity | It runs `gh` with the developer's token, so it could approve its own deploy, edit the apply environments or delete the ruleset; only `AGENTS.md` rules 20 and 21 ask it not to | Peer review: the `main` ruleset requires one approval from someone other than the author, and the apply environments turn on *Prevent self-review*, so the agent can't merge or deploy alone |
