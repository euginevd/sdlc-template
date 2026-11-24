# Checklist

Stages: Plan → Design → Build → Test → Deploy → Maintain, the six of Anthropic's AI-native SDLC; Plan has no controls of its own.

The guardrails by stage of the [secure agentic SDLC](../guides/06-secure-agentic-sdlc.md). Clear it before real users, customer data, payments or a `prod` deploy. How each one works: [guides/04-the-guardrails.md](../guides/04-the-guardrails.md); risks accepted instead: [guides/03-security-trade-offs.md](../guides/03-security-trade-offs.md).

| # | Stage | Control | Tool | Profile |
|---|---|---|---|---|
| 1 | Design | Threat modelling, requirements | `docs/threat-model.md`, and the spec's Rules with an OWASP ASVS level | Production; a prototype only if asked |
| 2 | Design | Cost estimate | `docs/aws/costs.md` | Production; a prototype keeps the starter's |
| 3 | Build, IDE | Secrets, SCA, IaC scanning | Gitleaks and Trivy, in `.lefthook/pre-push-scan.sh` | Both |
| 4 | Build, repo | Push protection, SCA | GitHub push protection and Dependabot, turned on by `bash scripts/protect-main.sh` | Both |
| 5 | Build, agent | Agent guardrails | `AGENTS.md`, the agent tool's permission settings and Stop hook, and for production the agent's own GitHub account | Both |
| 6 | Test | Secrets, SCA, IaC scanning | Gitleaks, Trivy and Checkov, in `.github/workflows/security.yml` | Both |
| 7 | Test | SAST | Semgrep (`security.yml`), CodeQL (`codeql.yml`), and GitHub AI Scan, set by hand | Both |
| 8 | Test | Supply chain security | Pins in the workflows, `exclude-newer` in `pyproject.toml`, `cooldown` in `dependabot.yml`, and the `sbom` job | Both |
| 9 | Test | Unit tests and coverage; abuse cases in production | `bash scripts/check.sh`: pytest, ruff and pyright, also in `.github/workflows/ci.yml` | Both; the bar differs |
| 10 | Test | DAST, unauthenticated | OWASP ZAP's baseline scan, in the `aws` workflow after each `dev` apply | Both |
| 11 | Test | DAST, authenticated | OWASP ZAP with a test login, per project | Production |
| 12 | Deploy | Branch protection | The `main` ruleset, set by `bash scripts/protect-main.sh` | Both |
| 13 | Deploy | Peer review | A second reviewer, set by `bash scripts/protect-main.sh production` | Production |
| 14 | Deploy | Cost review | Infracost, the `cost-report` job in `aws.yml` | Both |
| 15 | Deploy | AWS account baseline | Root MFA and IAM Identity Center, set by you | Both; production adds separate accounts |
| 16 | Deploy | Least privilege | GitHub OIDC, a read-only plan role and applies from `main` only, set in `infra/aws/bootstrap/bootstrap.yaml` | Both |
| 17 | Deploy | Deploy approval | A required reviewer on each `aws-<env>-apply` environment | Production |
| 18 | Deploy | Runtime secrets | Secrets Manager or SSM `SecureString`, per project | Both |
| 19 | Deploy | API protection | An API Gateway authoriser, AWS WAF, CORS and security headers, per project | Production |
| 20 | Maintain | Weekly re-scans | Weekly `security` and `codeql` runs, and Dependabot | Both |
| 21 | Maintain | Budget alert | The AWS budget in `bootstrap.yaml` | Both |
| 22 | Maintain | Access logs, throttling | The HTTP API's access logs and throttling, and Lambda logs, from `infra/aws/api/` | Both |
| 23 | Maintain | Audit logging | AWS CloudTrail, per account *(planned)* | Both |
| 24 | Maintain | Threat detection, alarms | Amazon GuardDuty and CloudWatch alarms, per account | Production |
