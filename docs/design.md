# Design

A worked example: `travel-claims`. Every project follows the [ArcVault design system](https://claude.ai/artifact/SWnGNCZKAxQBhxJ68cv5ao); this page is the part an app uses, plus the project's own choices. Optional: delete it if the project has no UI.

## Feel

1. Calm, precise and credible: a tool for regulated work, not a marketing page. No hype, emoji, gradients, aura blobs or scroll reveals in the app.
2. Warm paper, not cold white: `bg` with `ink` text, and teal `accent` used sparingly.
3. Light theme first; dark theme through `data-theme="dark"`.

## Tokens

| Token | Light | Dark | Use |
|-------|-------|------|-----|
| `bg` | `#fbf7f0` | `#141009` | Page |
| `bg-2` | `#fffdfa` | `#1c160e` | Cards and panels |
| `bg-3` | `#f3ece0` | `#241d12` | Sunken zones, table headers |
| `bg-ink` / `on-ink` | `#17120c` / `#f6efe3` | `#0d0a05` / `#f6efe3` | Primary buttons and their labels |
| `ink` | `#1b1610` | `#f6efe3` | Headings and primary text |
| `ink-2` | `#6e6457` | `#b0a492` | Body and secondary text |
| `ink-3` | `#9a8e7e` | `#7e7464` | Input borders, large or non-essential text |
| `accent` | `oklch(0.58 0.155 196)` | same | Focus rings, active states, links at 19px bold or larger |
| `warn` | `#b0700f` | `oklch(0.80 0.13 74)` | Regulatory and deadline callouts only |

4. Type: Geist 600 for headings, Inter for body, Geist Mono uppercase for labels. App sizes are the system's smallest: `h1` 2rem, `h2` 1.5rem, `h3` 1.14rem, `body` 1rem, `body-sm` 0.92rem in tables.
5. Spacing on the 8px scale (`space-1` 4px to `space-7` 48px); radii `radius-xs` for tags, `radius-md` for cards, `radius-pill` for buttons.
6. Cards use a 1px `line`, not a shadow; `shadow` is for menus and dialogs only.

## Components

7. Use the system's Button, Badge, Card, Eyebrow, Input and Logo first.
8. Build anything new from the tokens, never new colours, and add it back to the design system once it's settled.
9. Icons: Lucide outline, 24px grid, stroke 2, `currentColor`. No emoji or filled icons.

## Accessibility

10. Text meets 4.5:1: body text is `ink` or `ink-2` only (code-standards 16).
11. Controls and focus meet 3:1: input borders `ink-3`, a 3px `accent` focus ring, visible on every interactive element.
12. Colour never carries meaning alone: every status is a word plus an icon.
13. Motion is 0.2s UI transitions at most, and none under `prefers-reduced-motion`.

## Words

14. Australian English, sentence case, "you" for the user; mono uppercase only for labels.
15. Buttons say what happens: "Approve claim", "Send back", never "Submit" or "OK".
16. Errors say what went wrong and what to do next, in plain words, with no codes.

## This project

17. Handlers: a dense, table-first queue, then one claim per page with its decision, reasons and sources side by side.
18. Claimants: a single-column claim form that works at 360px wide.
19. Claim status chips: Approved, Declined, Referred and Paid, each a word, an icon and a `Badge`; `warn` only for a payment held over the limit.
20. Money in AUD as `$1,234.50`; dates as `8 Nov 2026`.
