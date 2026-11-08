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
4. Use the system's Button, Badge, Card, Eyebrow, Input and Logo. Build anything new from the tokens only, and add it back to the system once it's settled.
5. Icons: Lucide outline, stroke 2, `currentColor`.
6. Contrast: text 4.5:1, controls and focus rings 3:1 in both themes (code-standards 16).
7. Status is a word plus an icon, never colour alone. Motion is 0.2s at most, and none under `prefers-reduced-motion`.
8. Words: Australian English and sentence case; buttons say what happens ("Approve claim"); errors say what to do next.

## This project

9. Premium and quiet: a `bg-ink` header band with the logo, generous space on paper, and key numbers set large in Geist.
10. Queue: a strip of four figures (waiting, decided today, median time to decision, paid this week) with mono labels and a 7-day sparkline each, then the claims table.
11. Claim page: on the left, the claimant's story, receipt thumbnails that open full size, and a timeline of every step (submitted, screened, decided, paid); on the right, a sticky decision card with the outcome, the payout and the policy clauses it quotes.
12. Payout bar: one horizontal bar from claimed to paid, with the deductible and anything over the limit in `bg-3`, the paid amount in `accent`, and every segment labelled.
13. Charts: a line for trends, a bar for comparisons; `ink-3` axes, `accent` for the series in focus, and a table view of the same numbers.
14. Claimants: a single-column form that works at 360px wide, with numbered steps and a receipt drop zone that shows previews.
15. Every screen has loading skeletons in its own layout, an empty state that says what to do, and an error state with a retry.
16. Status chips: Approved, Declined, Referred and Paid; `warn` only for a payment held over the limit. Money as `$1,234.50` AUD, dates as `8 Nov 2026`.
