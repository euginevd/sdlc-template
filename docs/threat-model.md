# Threat model

A worked example: `travel-claims`. STRIDE on the data flow below; each risk maps to the OWASP lists that fit the app: Top 10:2025 (A), API Security Top 10:2023 (API), LLM Top 10:2025 (LLM) and Agentic Top 10:2026 (ASI). Optional: delete it if the project has no users, data or secrets to protect.

## Data flow

```mermaid
flowchart LR
  subgraph internet ["Internet: untrusted"]
    claimant[Claimant]
    handler[Handler]
  end
  subgraph aws ["AWS account, ap-southeast-2"]
    web((web))
    api((api))
    db[(Claims database)]
    bucket[(Receipt bucket)]
    subgraph agentzone ["Agent: output untrusted"]
      agent((agent))
    end
  end
  subgraph third ["External services"]
    entra[Entra ID]
    bedrock[Bedrock, AU profile]
    bank[Bank API]
  end
  claimant -- "4: claim, receipts" --> web
  handler -- "6: sign-in" --> entra
  handler -- "review, sign-off" --> web
  web -- "HTTPS, token" --> api
  api --> db
  api --> bucket
  api -- "claim as data" --> agent
  agent -- prompt --> bedrock
  agent -- "5: decision, schema-checked" --> api
  api -- "6: payment under the limit" --> bank
  classDef boundary fill:none,stroke:#d33,stroke-width:2px,stroke-dasharray:6 4
  class internet,aws,agentzone,third boundary
```

Rectangles are external entities, circles processes, cylinders data stores, red dashed boxes trust boundaries; numbers are the boundaries below.

| # | Data | Class | Where |
|:-:|------|-------|-------|
| 1 | Passports, bank details, medical records | Highly sensitive | Claims database and receipt bucket, in Australia (business 4) |
| 2 | Claim decisions and their reasons | Confidential | Claims database |
| 3 | Policy wording and the claims manual | Internal | Read by the agent |

## Trust boundaries

4. Internet to AWS: everything claimants and handlers send is untrusted, receipts included.
5. Agent to the `api`: model output is untrusted; code checks the decision before it can drive a payment.
6. AWS to external services: handlers sign in through Microsoft Entra ID (business 6), payments go to the bank API, and model calls stay in Australia.

## Top risks

STRIDE: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege.

| # | Risk | STRIDE | OWASP | Rating | Controls | Enforced at |
|:-:|------|:------:|-------|:------:|----------|-------------|
| 7 | Prompt injection in a receipt makes the agent approve a bad claim | T, E | LLM01, ASI01 | High | Content kept apart from instructions (code-standards 18), limits in code (spec 15), injection tests | Test, Monitor |
| 8 | The agent pays more than the policy allows | T, E | LLM06, ASI02 | High | Payment code checks every limit (spec 13) and fails closed (code-standards 7) | Code, Test |
| 9 | One claimant sees another's claim | I | A01, API1 | High | Authorisation on every request (code-standards 10), abuse-case tests (code-standards 11) | Code, Test |
| 10 | Personal data leaks into logs | I | A09, LLM02 | Medium | Redaction at the source (code-standards 8), a test against real receipts (status 10) | Code, Test |
| 11 | Claim data leaves Australia through model calls | I | LLM02 | Medium | The Australian inference profile (spec 16) | Deploy |
| 12 | Runaway model calls run up the bill | D | LLM10, API4 | Medium | Model call limits (code-standards 19), the `dev` budget (spec 19) | Code, Operate |
| 13 | A compromised package or image | T | A03, LLM03 | Medium | Pinned versions, Trivy on every push and PR | Code, Build |
| 14 | A secret is committed | I | A07 | Medium | The pre-push scan, OIDC with no long-lived keys | Code, Deploy |

## Compliance

15. Privacy Act and the Notifiable Data Breaches scheme: a privacy impact assessment before go-live; suspected breaches assessed within 30 days.
16. APRA CPS 234: controls tested yearly; APRA told within 72 hours of a material security incident.
