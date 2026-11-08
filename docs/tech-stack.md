# Tech stack

| Part | Choice |
|------|--------|
| Repo and pipeline | GitHub, GitHub Actions |
| IaC | Terraform `>= 1.17` (CI pins 1.17.1), AWS provider `6.72.0` |
| State | S3 `<project>-tfstate-<account>`, key `<project>/<unit>.tfstate`, `use_lockfile = true`; the bucket is passed at `init` from the `TF_STATE_BUCKET` variable |
| Bootstrap | CloudFormation stack `<project>-bootstrap`, from `aws/bootstrap/bootstrap.yaml`, changed in the AWS console by an admin |
| Auth | GitHub OIDC to `<project>-github-plan` (read-only, `aws-<target>-plan` environment) and `<project>-github-deploy` (`aws-<target>-apply` environment), scoped by the token's `sub` claim |
| Region | `ap-southeast-2` |
| Apps | *(Per app: language, framework, hosting)* |

## Checks

In each changed unit: `terraform fmt -recursive`, `terraform init -backend=false`, `terraform validate`. The PR's plan job is the last check.

*(Per app: the lint, type check and test commands.)*

On the developer workstation, a lefthook pre-push hook runs gitleaks and Trivy over the pushed commits and blocks on findings, for humans and coding agents alike. `scripts/setup.sh` installs them: `guides/02-git-hooks.md`.

## Deployment

- **PR:** plans each changed unit (every unit if the workflow changed) with the plan role, and writes the plan to the job summary.
- **Merge to `main`:** applies that exact plan with the deploy role after `aws-<target>-apply` approval.
- **Manual run:** one unit or `all`, `apply` or `destroy`, after `aws-<target>-apply` approval.
