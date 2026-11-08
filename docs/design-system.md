# Design system

A worked example: `travel-claims`. Built on the [ArcVault design system](https://claude.ai/artifact/SWnGNCZKAxQBhxJ68cv5ao): the part an app uses, then the project's own choices. Optional: delete it if the project has no UI.

## Tokens

| Token | Light | Dark | Use |
|-------|-------|------|-----|
| `bg` | `#fbf7f0` | `#141009` | Page |
| `bg-2` | `#fffdfa` | `#1c160e` | Cards and panels |
| `bg-3` | `#f3ece0` | `#241d12` | Sunken zones, table headers, excluded amounts |
| `bg-ink` / `on-ink` | `#17120c` / `#f6efe3` | `#0d0a05` / `#f6efe3` | Header band, primary buttons |
| `ink` | `#1b1610` | `#f6efe3` | Headings, primary text, large numbers |
| `ink-2` | `#6e6457` | `#b0a492` | Body and secondary text |
| `ink-3` | `#9a8e7e` | `#7e7464` | Input borders, chart axes; never essential text |
| `accent` | `oklch(0.58 0.155 196)` | same | Focus rings, active states, the series in focus |
| `warn` | `#b0700f` | `oklch(0.80 0.13 74)` | Regulatory and deadline callouts, held payments |

1. Type: Geist 600 for headings and numbers, Inter for body, Geist Mono uppercase for labels. App sizes: `h1` 2rem, `h2` 1.5rem, `h3` 1.14rem, body 1rem, tables 0.92rem.
2. Spacing on the 8px scale (4–48px); radii 6px for tags, 14px for cards, pills for buttons. Cards take a 1px `line`; `shadow` is for menus and dialogs only.

## Rules

3. Calm and precise: no hype, emoji, gradients or scroll reveals; `accent` used sparingly.
4. Use the system's Button, Badge, Card, Eyebrow, Input and Logo. Code uses the tokens as CSS variables (`var(--ink)`), never raw values; anything new is built from them and added back to the system once settled.
5. Icons: Lucide outline, stroke 2, `currentColor`; decorative icons are `aria-hidden`, and icon-only buttons have a label.
6. Themes follow the device (`prefers-color-scheme`), with a toggle that sets `data-theme`; test both, and Windows contrast themes (`forced-colors`).
7. Fonts are self-hosted `woff2` files served with the app, so no request leaves for a font CDN.
8. WCAG 2.2 AA (code-standards 16): text 4.5:1, controls and focus rings 3:1; targets at least 24×24px; sticky parts never hide the focused element; a file picker beside every drop zone; sign-in allows paste and password managers.
9. Status is a word plus an icon, never colour alone. Motion is 0.2s at most, and none under `prefers-reduced-motion`.
10. Words: Australian English and sentence case; buttons say what happens ("Approve claim"); errors say what to do next.
11. AI output is labelled: show what the agent decided, its reasons and sources, and how to ask for a person to review it (the Privacy Act's automated decision rules, business 3).

## This project

12. Premium and quiet: a `bg-ink` header band with the logo, generous space on paper, and key numbers set large in Geist.
13. Queue: a strip of four figures (waiting, decided today, median time to decision, paid this week) with mono labels and a 7-day sparkline each, then the claims table.
14. Claim page: on the left, the claimant's story, receipt thumbnails that open full size, and a timeline of every step (submitted, screened, decided, paid); on the right, a sticky decision card with the outcome, the payout and the policy clauses it quotes.
15. Payout bar: one horizontal bar from claimed to paid, with the deductible and anything over the limit in `bg-3`, the paid amount in `accent`, and every segment labelled.
16. Charts: a line for trends, a bar for comparisons; `ink-3` axes, `accent` for the series in focus, and a table view of the same numbers.
17. Claimants: a single-column form that works at 360px wide, with numbered steps and a receipt drop zone that shows previews.
18. Every screen has loading skeletons in its own layout, an empty state that says what to do, and an error state with a retry.
19. Status chips: Approved, Declined, Referred and Paid; `warn` only for a payment held over the limit.
20. Numbers in tabular figures, rounded to at most 2 decimal places (`4.25 hours`, `92.5%`); money always shows 2 (`$1,234.50` AUD). Dates as `8 Nov 2026`.
