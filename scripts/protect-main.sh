#!/usr/bin/env bash
# Hardens the repo: Actions settings, squash-only merges, GitHub's free security features, and a main ruleset.
# Safe to rerun. The ruleset needs a public repo or a paid plan. Usage: bash scripts/protect-main.sh
set -uo pipefail

repo=$(gh repo view --json nameWithOwner --jq .nameWithOwner) || exit 1
public=$(gh repo view --json visibility --jq '.visibility == "PUBLIC"')

# Squash merges only, and merged branches are deleted.
gh api -X PATCH "repos/$repo" -F allow_squash_merge=true -F allow_merge_commit=false -F allow_rebase_merge=false -F delete_branch_on_merge=true >/dev/null
# Workflow tokens are read-only unless a workflow asks for more, and can't approve PRs.
gh api -X PUT "repos/$repo/actions/permissions/workflow" -f default_workflow_permissions=read -F can_approve_pull_request_reviews=false
# Only GitHub's actions and the two the deploy uses, each pinned to a full commit SHA.
gh api -X PUT "repos/$repo/actions/permissions" -F enabled=true -f allowed_actions=selected -F sha_pinning_required=true
gh api -X PUT "repos/$repo/actions/permissions/selected-actions" -F github_owned_allowed=true -F verified_allowed=false   -f 'patterns_allowed[]=hashicorp/setup-terraform@*' -f 'patterns_allowed[]=aws-actions/configure-aws-credentials@*'
# Dependabot alerts and security-update PRs.
gh api -X PUT "repos/$repo/vulnerability-alerts" && gh api -X PUT "repos/$repo/automated-security-fixes" >/dev/null

if [ "$public" = true ]; then
  # Free on public repos: secret scanning with push protection, private reporting (SECURITY.md) and CodeQL.
  gh api -X PATCH "repos/$repo" --input - >/dev/null <<'JSON'
{"security_and_analysis": {"secret_scanning": {"status": "enabled"}, "secret_scanning_push_protection": {"status": "enabled"}}}
JSON
  gh api -X PUT "repos/$repo/private-vulnerability-reporting"
  gh api -X PATCH "repos/$repo/code-scanning/default-setup" -f state=configured >/dev/null
  # Anyone can open a PR on a public repo: their workflow runs wait for your approval.
  gh api -X PUT "repos/$repo/actions/permissions/fork-pr-contributor-approval" -f approval_policy=all_external_contributors
fi

if gh api "repos/$repo/rulesets" --jq '.[].name' 2>/dev/null | grep -qx main; then
  echo "Settings applied; ruleset 'main' already exists on $repo."
  exit 0
fi

gh api "repos/$repo/rulesets" -X POST --input - >/dev/null <<'JSON' || { echo "Could not add the ruleset: a private repo needs a paid GitHub plan."; exit 1; }
{
  "name": "main",
  "target": "branch",
  "enforcement": "active",
  "conditions": { "ref_name": { "include": ["~DEFAULT_BRANCH"], "exclude": [] } },
  "rules": [
    { "type": "deletion" },
    { "type": "non_fast_forward" },
    {
      "type": "required_status_checks",
      "parameters": {
        "strict_required_status_checks_policy": false,
        "required_status_checks": [
          { "context": "python" }, { "context": "web" }, { "context": "secrets" },
          { "context": "packages-and-iac" }, { "context": "terraform" }, { "context": "code" }
        ]
      }
    },
    {
      "type": "pull_request",
      "parameters": {
        "required_approving_review_count": 0,
        "dismiss_stale_reviews_on_push": false,
        "require_code_owner_review": false,
        "require_last_push_approval": false,
        "required_review_thread_resolution": false,
        "allowed_merge_methods": ["squash"]
      }
    }
  ]
}
JSON

echo "Settings applied and ruleset 'main' added to $repo."
