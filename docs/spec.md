# Spec

A worked example: `travel-claims`, in production. For a new project, replace it by hand or ask the agent to draft one from your notes. The user approves every change.

## Project

- Name: `travel-claims`
- Problem: claims handlers work through a queue of travel insurance claims by hand, so simple claims wait days to be paid.
- Goal: an AI agent decides routine claims in minutes, and handlers spend their time only on claims that need judgement.
- Users: claimants submit and track claims; handlers review and sign off; admins manage users and limits.
- AWS: accounts `travel-claims-dev` and `travel-claims-prod`, region `ap-southeast-2`, environments `dev` and `prod`.

## Stack

Template defaults: GitHub Actions, Terraform on AWS and the Gitleaks and Trivy pre-push scan.

- `web`: React, Vite and TypeScript, hosted on S3 and CloudFront. Checks: `npm run lint`, `npm run typecheck`, `npm test`.
- `api`: Python and FastAPI on Lambda behind an HTTP API. Checks: `uv run ruff check`, `uv run pyright`, `uv run pytest`.
- `agent`: Python and LangGraph on Lambda, calling Claude on Amazon Bedrock. Checks: `uv run ruff check`, `uv run pyright`, `uv run pytest`.

## Done when

1. A claimant can submit a claim with receipts and see its status.
2. The agent decides each claim and gives reasons that quote the policy wording.
3. Claims the agent approves under $1,000 are paid automatically; the rest wait for a handler.
4. A handler can approve, decline or send back a claim from the dashboard.
5. No payment exceeds the policy limit, whatever the agent decides.

## Rules

- Claims hold passport, bank and medical details, so the laws in `business-context.md` apply.
- The agent decides; deterministic code pays and enforces every limit.
- Bedrock calls use the Australian cross-region inference profile, so claim data stays in Australia.
- Receipts are untrusted input: text hidden in them must not change a decision.
- Every decision is logged with its reasons, with personal data redacted.
- AWS spend stays under $200 a month in `dev`.

## Not for now

- Quotes and policy sales: claims only.
- A mobile app.
- Claims in currencies other than AUD.
- Fraud detection beyond the payment checks.
