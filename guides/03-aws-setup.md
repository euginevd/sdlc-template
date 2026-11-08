# AWS setup

Bootstrap, deploy and clean up a project's AWS accounts. Done by a person, never the agent: the apply environment is the deploy gate (trade-offs 1). `<project>` is the project's name, as in `PROJECT_NAME`.

## Bootstrap

Once per AWS account (`dev`, then `prod`), as an admin:

1. **AWS Console:** CloudFormation → upload [bootstrap.yaml](../aws/bootstrap/bootstrap.yaml) as `<project>-bootstrap`, with `ProjectName` `<project>`, `GitHubOwner` and `GitHubRepo` as in the repo URL, and `Target` `dev` or `prod` (`CreateOidcProvider` false if the account already has GitHub's).
2. **GitHub:** Settings → Environments: `aws-<target>-plan`, and `aws-<target>-apply` with yourself as required reviewer and deployment branches limited to `main`.
3. **GitHub:** Settings → Variables: `PROJECT_NAME` for the repo. Then on each environment, from that account's stack outputs: `AWS_PLAN_ROLE_ARN` on `-plan`, `AWS_DEPLOY_ROLE_ARN` on `-apply`, and `TF_STATE_BUCKET` on both.

## Deploying

A merge to `main` applies to `dev` after your approval. To promote to `prod`: Actions → `aws` → Run workflow → target `prod`, `all`, `apply`, then approve.

## Cleanup

1. **GitHub:** Actions → `aws` → Run workflow → each target, `all`, `destroy`.
2. **AWS Console:** empty the state bucket, then delete the bootstrap stack.
3. **GitHub:** delete the plan and apply environments.
