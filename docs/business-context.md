# Business context

Who the business is. The same for every project for this business: change it only when the business changes. A worked example; replace it for a new business.

- Business: Wattle Travel Insurance (fictional), an Australian travel insurer.
- Size: about 200 staff, a claims team of 20 handlers, about 40,000 claims a year.
- Regulators and laws: APRA (CPS 234 information security, CPS 230 operational risk), ASIC, the Privacy Act and the Notifiable Data Breaches scheme.
- Data: customer data stays in Australia.
- Risk appetite: low for customer data and payments. Changes ship to `dev` first, and to `prod` after sign-off.
- Systems: the policy admin system is the source of truth for policies; payments go through the bank's API; staff sign in with Microsoft Entra ID.
- People: the claims operations lead owns the claims rules; the security team approves new data flows.
- Tone: plain, friendly Australian English for customers; no insurance jargon.
