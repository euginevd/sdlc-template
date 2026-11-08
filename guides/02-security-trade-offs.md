# Security trade-offs

The risks the template accepts, each with why it's a risk and the fix for production. Numbered so reviews can cite them (trade-offs 1). An accepted risk is a decision: change it here, never by weakening a check.

1. **The agent shares the developer's GitHub identity.**\
   **Why it's a risk:**\
   It runs `gh` with the developer's token, so it could approve its own deploy, edit the apply environments or delete the ruleset; only `AGENTS.md` rules 20 and 21 ask it not to.\
   **Production fix:**\
   Peer review. The `main` ruleset requires at least one approval from someone other than the author, and the apply environments turn on *Prevent self-review*. GitHub never lets an author approve their own PR or deploy, so the agent can't merge or deploy alone.
