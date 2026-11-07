# Tech stack

| Part | Choice |
|------|--------|
| IaC | Terraform |
| State | S3, one key per root, `use_lockfile = true` |
| Pipeline | GitHub Actions |
| Auth | GitHub OIDC to a read-only plan role and a deploy role, per environment |
| Region | |

## Checks

## Deployment
