# Terraform rules

Applies to everything under `aws/`, on top of the root `AGENTS.md`.

- One Terraform root and state per unit, in `aws/<unit>/`. To start one, copy `aws/api` and change `Unit` in `versions.tf`.
- Each unit has `main.tf`, `variables.tf`, `outputs.tf`, `versions.tf` and its `.terraform.lock.hcl`. Pin Terraform and every provider.
- Don't write the project name, environment, account ID, state bucket or state key in the code. The pipeline passes them: `TF_VAR_project`, `TF_VAR_environment` and `-backend-config` at `terraform init`.
- Names: `${var.project}-<unit>-<what>-${var.environment}`. Tags come from the provider's `default_tags`.
- Every IAM role sets `permissions_boundary` to the `${var.project}-boundary` policy, or the deploy role can't create it.
- A new AWS service needs deploy and plan permissions in `bootstrap/bootstrap.yaml` first, scoped to `${ProjectName}-*` names. Ask the user to update the stack before the unit can deploy.
- `bootstrap/` is CloudFormation that only the user deploys. The pipeline never touches it.
- Check locally with `terraform fmt -recursive && terraform init -backend=false && terraform validate`. Never run `plan` or `apply` against the account; the `aws` workflow does.
