# Security trade-offs

The risks the template accepts, why it's built the way it is, and the fix for production. The same for every project, numbered so reviews can cite them (trade-offs 7). An accepted risk is a decision: change it here, never by weakening a check.

## Layers

What stops a bad change, from weakest to strongest. Layers 3 to 6 hold even if the agent ignores 1 and 2.

1. **Prompt rules:** `AGENTS.md` and `docs/code-standards.md`. The agent can ignore them.
2. **Harness:** Claude Code deny rules in `.claude/settings.json` *(planned)*. They match command patterns, so a workaround can slip past.
3. **Token scope:** the agent's own fine-grained token *(planned)*, which can't approve a deploy or edit environments or the ruleset.
4. **Repo:** the `main` ruleset requires every check to pass, allows squash merges only, and blocks force pushes and deletion.
5. **Deploy gate:** the `aws-<target>-apply` environment needs your approval and deploys only from `main`.
6. **Cloud:** the deploy role trusts only the apply environment, so a workflow edited to skip the gate can't deploy. The permissions boundary caps every role Terraform creates.

## Known risks

7. **The agent works as you on GitHub.** *Why it's a risk:* it runs `gh` with your token, so it could approve its own deploy, edit the apply environments or delete the ruleset; only `AGENTS.md` rules 20 and 21 ask it not to. *Production fix:* give the agent its own fine-grained token without Administration, Deployments or Environments permissions, so GitHub refuses those calls (layer 3), with deny rules as a second layer (layer 2).

## Why we do what we do

8. **Actions pinned by commit SHA, from an allow-list:** a moved tag can't change what the pipeline runs.
9. **Scanners run from digest-pinned images:** no third-party action code runs in the pipeline.
10. **Read-only tokens, and no credentials kept after checkout:** a step can't push with the job's token.
11. **Packages at least 7 days old:** most malicious releases are pulled within days.
12. **OIDC, no access keys:** nothing long-lived to leak.
13. **Separate plan and deploy roles:** a PR only ever gets read access.
14. **The apply uses the saved plan:** what deploys is exactly what you approved, zip included.
15. **A pre-push scan and the same scans in CI:** a hook can be skipped; CI can't.
16. **Gitleaks over full history and unpushed commits:** a secret added then removed is still caught.
