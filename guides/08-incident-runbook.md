# Incident runbook

What to do when something is compromised: a malicious package or action, a leaked token, or an alarm that shows someone else in the account. The steps run in order; speed matters most in the first three. You run them, by hand: the agent may help find the reach (step 3) from logs and lock files, but never changes cloud resources or rotates a secret ([AGENTS.md](../AGENTS.md) rule 14). Run the GitHub commands in Git Bash and the AWS ones in **AWS CloudShell**.

## 1. Stop deploys

Nothing new ships while you look. Turn off the deploy workflows and merge nothing:

```bash
gh workflow disable aws.yml && gh workflow disable images.yml
```

## 2. Keep evidence

Before anything is deleted or rotated, write down the package and version, or the token, and when it was first seen. Save the logs of each run that installed or used it, since GitHub deletes them after 90 days:

```bash
gh run list --limit 50 --json databaseId,workflowName,createdAt,headBranch
```

```bash
gh run view <run-id> --log > run-<run-id>.log
```

Keep these in `local/`, which git ignores, never in the repo.

## 3. Find the reach

List everything that ran the bad code or held the token, and every secret each could read:

- **Machines:** each one that ran `npm ci`, `uv sync` or the app during the window: its `~/.aws`, `gh` login, `.env` files and `~/.npmrc`.
- **CI:** each run in the window: the GitHub secrets it got, and the AWS role it could assume through OIDC.
- **Images:** each image built in the window, and where it was deployed.
- **AWS:** in CloudTrail's Event history, each call made with the affected identity.

## 4. Remove persistence

An attacker leaves a way back in. Remove each one you didn't add:

- **GitHub:** new workflows, deploy keys, webhooks, GitHub Apps, collaborators, personal access tokens, and ruleset changes (Settings, and your account's Settings → Developer settings).
- **AWS:** new IAM users, access keys, roles or trust policies, Lambda layers or functions, and resources in other regions.
- **Machines:** scripts in `.git/hooks/` the template didn't put there, edits to shell profiles (`~/.bashrc`, PowerShell's `$PROFILE`), and unknown scheduled tasks.

## 5. Rotate credentials

Rotate every secret in the reach, newest exposure first: the `gh` login (revoke GitHub CLI under your account's Settings → Applications, then log in again) and any personal access tokens, the troubleshoot user's AWS key, GitHub secrets, and keys in Secrets Manager. OIDC roles have no key to rotate, but check their trust policy still names only this repo and `main`.

```bash
gh auth login
```

## 6. Purge caches

A cache can hand the bad version back. Clear GitHub's and your own, then delete images built in the window from ECR:

```bash
gh cache delete --all
```

```bash
npm cache clean --force && uv cache clean
```

## 7. Reinstall clean

Pin the last good version (AGENTS.md rule 16) and reinstall with install scripts off; a machine that ran the bad code gets a fresh clone, or a rebuild if it ran with your login:

```bash
npm ci --ignore-scripts && uv sync --locked
```

## 8. Resume and record

Once `bash scripts/check.sh all` and CI pass on the pinned version, turn the deploys back on:

```bash
gh workflow enable aws.yml && gh workflow enable images.yml
```

Then open an issue from the **Incident or finding** form with what happened and the check, alarm or lesson that stops a repeat, so the fix is planned like any other change ([guide 06](06-secure-agentic-sdlc.md), Maintain).
