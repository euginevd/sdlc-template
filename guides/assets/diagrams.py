"""Builds the guide diagrams as HTML and renders each to a PNG beside this file.

Usage: python -I guides/assets/diagrams.py [name ...]
Each renders in light and dark (<name>.png, <name>-dark.png); social.png is the repo's
social preview, light only. Needs Google Chrome and a network connection for the fonts
(Geist, Geist Mono, Instrument Serif).
"""

import os
import subprocess
import sys
import tempfile
from collections.abc import Callable

HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = os.environ.get("CHROME", r"C:\Program Files\Google\Chrome\Application\chrome.exe")
WIDTH = 1200
FONTS = (
    "https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700"
    "&family=Geist+Mono:wght@400;500;700&family=Instrument+Serif&display=swap"
)
THEMES = ("light", "dark")

# Colours, type and spacing from docs/design-system.md, in light and dark.
CSS = """
:root {
  --bg: oklch(0.985 0.002 90); --bg-2: oklch(1 0 0); --bg-3: oklch(0.965 0.003 90);
  --bg-ink: oklch(0.21 0.006 90); --on-ink: oklch(0.97 0.003 90); --on-ink-2: oklch(0.78 0.004 90);
  --ink: oklch(0.21 0.006 90); --ink-2: oklch(0.45 0.006 90); --ink-3: oklch(0.62 0.005 90);
  --line: oklch(0.91 0.004 90); --line-2: oklch(0.86 0.004 90);
  --line-ink: oklch(1 0 0 / .14);
  --accent: oklch(0.50 0.17 262); --accent-2: oklch(0.78 0.10 262);
  --teal-deep: oklch(0.50 0.17 262); --warn-dark: oklch(0.80 0.13 75);
  --accent-weak: color-mix(in oklab, var(--accent) 24%, transparent);
  --mint-tint: color-mix(in oklab, var(--accent) 5%, var(--bg-2));
  --fs: 'Instrument Serif', Georgia, serif;
  --fd: 'Geist', system-ui, sans-serif;
  --fb: 'Geist', system-ui, sans-serif;
  --fm: 'Geist Mono', ui-monospace, monospace;
}
:root[data-theme="dark"] {
  --bg: oklch(0.16 0.004 90); --bg-2: oklch(0.20 0.004 90); --bg-3: oklch(0.13 0.004 90);
  --bg-ink: oklch(0.25 0.006 262); --on-ink: oklch(0.97 0.003 90); --on-ink-2: oklch(0.78 0.004 90);
  --ink: oklch(0.95 0.003 90); --ink-2: oklch(0.74 0.004 90); --ink-3: oklch(0.58 0.004 90);
  --line: oklch(0.28 0.004 90); --line-2: oklch(0.34 0.004 90);
  --line-ink: oklch(1 0 0 / .12);
  --accent: oklch(0.74 0.12 262); --accent-2: oklch(0.80 0.10 262);
  --teal-deep: oklch(0.74 0.12 262);
  --mint-tint: color-mix(in oklab, var(--accent) 6%, var(--bg-2));
}
* { box-sizing: border-box; }
html, body { margin: 0; background: var(--bg); }
.page {
  width: __W__px; padding: 56px 60px 44px; position: relative; overflow: hidden;
  background: var(--bg); color: var(--ink); font-family: var(--fb);
}
.eyebrow {
  font-family: var(--fm); font-size: 17px; letter-spacing: .16em; text-transform: uppercase;
  font-weight: 700; color: var(--accent); display: flex; align-items: center; gap: 12px;
}
.eyebrow::before { content: ""; width: 28px; height: 1px; background: var(--accent); }
h1 {
  font-family: var(--fs); font-weight: 400; font-size: 58px; letter-spacing: -.01em;
  line-height: 1.05; margin: 14px 0 0; max-width: 22ch;
}
.lead {
  color: var(--ink-2); font-size: 22px; line-height: 1.5; margin: 14px 0 0; max-width: 68ch;
}
.label {
  font-family: var(--fm); font-size: 16px; letter-spacing: .12em; text-transform: uppercase;
  font-weight: 700;
}
.tile {
  border: 1px solid var(--line); background: var(--bg-2); border-radius: 12px; padding: 26px;
}
.badge {
  display: grid; place-items: center; border-radius: 12px; flex: none;
  background: color-mix(in oklab, var(--accent) 12%, var(--bg-2)); color: var(--accent);
}
.ico { display: inline-block; vertical-align: middle; flex: none; }
.ico svg { width: 100%; height: 100%; display: block; }
.foot {
  margin-top: 28px; display: flex; justify-content: space-between; color: var(--ink-3);
  font-family: var(--fm); font-size: 15px; letter-spacing: .08em;
}
""".replace("__W__", str(WIDTH))

# Lucide icons: 24px grid, 2px round strokes, as the design system's iconography asks.
ICONS = {
    "bot": '<path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/>'
    '<path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6'
    "a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5"
    'a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "user": '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    "book": '<path d="M12 7v14"/><path d="M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4'
    ' 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3 3 3 0 0 0-3-3z"/>',
    "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77'
    "a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94"
    'l-3.76 3.76z"/>',
    "loop": '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/>'
    '<path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/>'
    '<path d="M8 16H3v5"/>',
    "lock": '<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/>'
    '<path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "cpu": '<rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9"'
    ' y="9" rx="1"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/>'
    '<path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/>'
    '<path d="M9 20v2"/>',
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "down": '<path d="M12 5v14"/><path d="m19 12-7 7-7-7"/>',
    "chevrons": '<path d="m7 6 5 5 5-5"/><path d="m7 13 5 5 5-5"/>',
    "infinity": '<path d="M6 16c5 0 7-8 12-8a4 4 0 0 1 0 8c-5 0-7-8-12-8a4 4 0 1 0 0 8"/>',
    "keyboard": '<path d="M10 8h.01"/><path d="M12 12h.01"/><path d="M14 8h.01"/>'
    '<path d="M16 12h.01"/><path d="M18 8h.01"/><path d="M6 8h.01"/><path d="M7 16h10"/>'
    '<path d="M8 12h.01"/><rect width="20" height="16" x="2" y="4" rx="2"/>',
    "file": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/>'
    '<path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/>'
    '<path d="M16 17H8"/>',
    "code": '<path d="m16 18 6-6-6-6"/><path d="m8 6-6 6 6 6"/>',
    "flask": '<path d="M10 2v7.527a2 2 0 0 1-.211.896L4.72 20.55a1 1 0 0 0 .9 1.45h12.76'
    'a1 1 0 0 0 .9-1.45l-5.069-10.127A2 2 0 0 1 14 9.527V2"/><path d="M8.5 2h7"/>'
    '<path d="M7 16h10"/>',
    "merge": '<circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/>'
    '<path d="M6 21V9a9 9 0 0 0 9 9"/>',
    "rocket": '<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91'
    'a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1'
    ' 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4'
    'c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>',
    "activity": '<path d="M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0'
    'L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.49 12H2"/>',
    "check": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    "eye": '<path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0'
    ' .696 10.75 10.75 0 0 1-19.876 0"/><circle cx="12" cy="12" r="3"/>',
    "terminal": '<path d="m4 17 6-6-6-6"/><path d="M12 19h8"/>',
    "package": '<path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2'
    ' 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/>'
    '<path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "message": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
}


def icon(name: str, color: str = "currentColor", size: int = 20) -> str:
    """An inline Lucide icon in the given colour and size."""
    style = f"width:{size}px;height:{size}px;color:{color}"
    svg = (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"'
        f' stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>'
    )
    return f'<span class="ico" style="{style}">{svg}</span>'


def page(css: str, body: str) -> str:
    """A whole HTML document: the shared styles, this diagram's styles and its body.

    The theme is filled in at render time, through the __THEME__ placeholder.
    """
    head = f'<meta charset="utf-8"><link rel="stylesheet" href="{FONTS}">'
    head += f"<style>{CSS}{css}</style>"
    content = f'<body><div class="page">{body}</div></body>'
    html = '<!doctype html><html lang="en" data-theme="__THEME__">'
    return f"{html}<head>{head}</head>{content}</html>"


def foot(number: str) -> str:
    return f'<div class="foot"><span>SDLC-TEMPLATE · GUIDES/02</span><span>{number}</span></div>'


def header(eyebrow: str, title: str, lead: str = "") -> str:
    lead_html = f'<p class="lead">{lead}</p>' if lead else ""
    return f'<div class="eyebrow">{eyebrow}</div><h1>{title}</h1>{lead_html}'


def badge(name: str, size: int = 60) -> str:
    """An icon on a tinted square, sized to stay legible when GitHub scales the image down."""
    inner = icon(name, "currentColor", size // 2)
    return f'<span class="badge" style="width:{size}px;height:{size}px">{inner}</span>'


# 1. Evolution ------------------------------------------------------------------------------------
EVOLUTION_CSS = """
.eras { margin-top: 44px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px 28px; }
.era { position: relative; }
.era:not(:nth-child(3n)):not(:last-child)::after {
  content: "\\2192"; position: absolute; right: -24px; top: 50%; transform: translateY(-50%);
  color: var(--ink-3); font-size: 22px;
}
.era .when { font-family: var(--fm); font-size: 17px; color: var(--ink-3); margin-top: 18px; }
.era .name { font-family: var(--fd); font-weight: 600; font-size: 30px; margin-top: 4px; }
.era .what { font-size: 21px; color: var(--ink-2); margin-top: 6px; line-height: 1.35; }
.era.now { background: var(--bg-ink); border-color: var(--bg-ink); }
.era.now .name { color: var(--on-ink); }
.era.now .what { color: var(--on-ink-2); }
.era.now .when { color: var(--accent-2); }
.era.now .badge { background: var(--accent); color: oklch(1 0 0); }
.flow { margin-top: 28px; display: flex; align-items: center; flex-wrap: wrap; gap: 6px; }
.flow .label { color: var(--ink-3); margin-right: 18px; }
.flow .step {
  display: inline-flex; align-items: center; gap: 10px; font-size: 21px; font-weight: 500;
}
.flow .sep { color: var(--ink-3); margin: 0 12px; font-size: 22px; }
"""

ERAS = [
    ("1970s", "Waterfall", "chevrons", "One long pass"),
    ("2001", "Agile", "loop", "Short sprints"),
    ("2009", "DevOps", "infinity", "One automated pipeline"),
    ("2010s", "DevSecOps", "shield", "Security in every stage"),
    ("2021", "AI-assisted", "keyboard", "AI suggests, people type"),
    ("Now", "Secure agentic", "bot", "Agents build, controls check, people decide"),
]


def evolution() -> str:
    tiles = "".join(
        f'<div class="tile era{" now" if when == "Now" else ""}">{badge(ic)}'
        f'<div class="when">{when}</div><div class="name">{name}</div>'
        f'<div class="what">{what}</div></div>'
        for when, name, ic, what in ERAS
    )
    sep = '<span class="sep">&rarr;</span>'
    flow = (
        '<div class="tile flow"><span class="label">Who writes the code</span>'
        f'<span class="step">{icon("user", "var(--accent)", 26)}People</span>{sep}'
        f'<span class="step">{icon("keyboard", "var(--accent)", 26)}People, with AI</span>{sep}'
        f'<span class="step">{icon("bot", "var(--accent)", 26)}Agents, inside guardrails</span>'
        "</div>"
    )
    body = (
        header("How we got here", "Each step fixed the last one&rsquo;s biggest gap.")
        + f'<div class="eras">{tiles}</div>'
        + flow
        + foot("1 / 3")
    )
    return page(EVOLUTION_CSS, body)


# 2. Harness --------------------------------------------------------------------------------------
HARNESS_CSS = """
.you {
  margin: 36px auto 0; width: fit-content; display: flex; align-items: center; gap: 14px;
  padding: 16px 28px; border: 1px solid var(--line-2); border-radius: 999px;
  background: var(--bg-2); font-size: 22px; color: var(--ink-2);
}
.you b { font-weight: 600; color: var(--ink); }
.down { text-align: center; color: var(--ink-3); margin: 8px 0; }
.trio { display: grid; grid-template-columns: 1fr 1.05fr 1fr; gap: 20px; }
.trio h3 { font-family: var(--fd); font-weight: 600; font-size: 28px; margin: 16px 0 2px; }
.trio .sub { font-size: 19px; color: var(--ink-2); margin-bottom: 12px; }
.item { display: flex; align-items: center; gap: 12px; font-size: 20px; padding: 10px 0; }
.item + .item { border-top: 1px solid var(--line); }
.agent {
  background: var(--bg-ink); color: var(--on-ink); border-color: var(--bg-ink);
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  text-align: center;
}
.agent .badge { background: var(--accent); color: oklch(1 0 0); }
.agent h3 { color: var(--on-ink); font-size: 32px; }
.agent .sub { color: var(--on-ink-2); }
.chip {
  display: inline-flex; align-items: center; gap: 10px; padding: 10px 20px; border-radius: 999px;
  border: 1px solid var(--line-ink); font-size: 20px; font-weight: 600; margin-top: 6px;
}
.rails { margin-top: 20px; }
.rails .top { display: flex; justify-content: space-between; align-items: center; }
.rails h3 {
  font-family: var(--fd); font-weight: 600; font-size: 28px; margin: 0;
  display: flex; align-items: center; gap: 12px;
}
.steps {
  margin-top: 22px; display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px;
  align-items: end;
}
.bar {
  border-radius: 8px 8px 4px 4px; background: var(--accent); display: grid;
  place-items: center; color: oklch(1 0 0);
}
.st { font-family: var(--fd); font-weight: 600; font-size: 22px; margin-top: 12px; }
.st span { font-family: var(--fm); color: var(--accent); margin-right: 8px; }
.sd { font-size: 18px; color: var(--ink-2); margin-top: 2px; line-height: 1.35; min-height: 48px; }
"""

CONTEXT = [
    ("file", "AGENTS.md rules"),
    ("file", "Spec and plan"),
    ("shield", "Threat model"),
    ("book", "Decisions and status"),
]
TOOLS = [
    ("terminal", "Git and gh"),
    ("package", "Package managers"),
    ("search", "Security scanners"),
    ("eye", "Review subagent"),
]
LAYERS = [
    ("Asked", "AGENTS.md rules", "message"),
    ("Checked", "Pre-push scan", "search"),
    ("Enforced", "Required PR checks", "shield"),
    ("Limited", "AWS only in the pipeline", "lock"),
    ("Approved", "You sign off", "user"),
]


def items(rows: list[tuple[str, str]]) -> str:
    return "".join(
        f'<div class="item">{icon(ic, "var(--accent)", 24)}{text}</div>' for ic, text in rows
    )


def harness() -> str:
    you = (
        f'<div class="you">{icon("user", "var(--ink)", 26)}<b>You</b>'
        "set the goal and approve each gate</div>"
        f'<div class="down">{icon("down", "var(--ink-3)", 26)}</div>'
    )
    trio = (
        '<div class="trio">'
        f'<div class="tile">{badge("book")}<h3>Context</h3><div class="sub">What it knows</div>'
        f"{items(CONTEXT)}</div>"
        f'<div class="tile agent">{badge("bot", 76)}<h3>Coding agent</h3>'
        '<div class="sub">plans · writes · tests · fixes</div>'
        f'<span class="chip">{icon("cpu", "var(--accent-2)", 24)}Model</span></div>'
        f'<div class="tile">{badge("wrench")}<h3>Tools</h3><div class="sub">What it can touch</div>'
        f"{items(TOOLS)}</div></div>"
    )
    steps = "".join(
        f'<div><div class="bar" style="height:{44 + i * 20}px;opacity:{0.4 + i * 0.15:.2f}">'
        f"{icon(ic, 'currentColor', 26)}</div>"
        f'<div class="st"><span>{i + 1}</span>{name}</div><div class="sd">{desc}</div></div>'
        for i, (name, desc, ic) in enumerate(LAYERS)
    )
    rails = (
        f'<div class="tile rails"><div class="top"><h3>{icon("lock", "var(--accent)", 28)}'
        'Guardrails: what stops it</h3><span class="label" style="color:var(--ink-3)">'
        f'Weakest &rarr; strongest</span></div><div class="steps">{steps}</div></div>'
    )
    body = (
        header("The harness", "An agent is a model inside a harness.")
        + you
        + trio
        + rails
        + foot("2 / 3")
    )
    return page(HARNESS_CSS, body)


# 3. Lifecycle ------------------------------------------------------------------------------------
LIFECYCLE_CSS = """
.grid { margin-top: 36px; display: grid; grid-template-columns: 260px 1fr 1fr 260px; }
.h { padding: 0 18px 14px; display: flex; align-items: center; gap: 10px; color: var(--ink-2); }
.h.p {
  background: var(--bg-ink); color: var(--on-ink); border-radius: 12px 12px 0 0;
  padding-top: 18px;
}
.c {
  padding: 18px; border-top: 1px solid var(--line); font-size: 20px; line-height: 1.35;
  display: flex; flex-direction: column; justify-content: center;
}
.c.s { flex-direction: row; align-items: center; justify-content: flex-start; gap: 14px; }
.st { font-family: var(--fd); font-weight: 600; font-size: 24px; line-height: 1.15; }
.role {
  font-family: var(--fm); font-size: 15px; color: var(--accent); margin-top: 4px;
  letter-spacing: .04em;
}
.c.k { background: var(--mint-tint); }
.c.p {
  background: var(--bg-ink); color: var(--on-ink); border-top-color: var(--line-ink);
  font-weight: 500; gap: 4px;
}
.c.p .who { font-size: 17px; color: var(--on-ink-2); font-weight: 400; }
.c.p.last { border-radius: 0 0 12px 12px; }
.tag {
  font-family: var(--fm); font-size: 15px; letter-spacing: .12em; font-weight: 700;
  color: var(--accent-2); display: inline-flex; gap: 8px; align-items: center;
}
.tag.hard { color: var(--warn-dark); }
.c.p.hard { box-shadow: inset 0 0 0 3px var(--warn-dark); border-radius: 6px; }
.c.p.auto { align-items: center; text-align: center; }
.none { color: var(--ink-3); font-style: italic; }
.notes { margin-top: 20px; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.note { display: flex; gap: 16px; align-items: center; font-size: 20px; padding: 20px 22px; }
.note b { display: block; font-family: var(--fd); font-size: 22px; font-weight: 600; }
.note span { color: var(--ink-2); }
"""

# Stage, icon, the agent's role, what it does, what the controls check, and the person's gate:
# (kind, text, who in a team), or None where the checks decide.
STAGES: list[tuple[str, str, str, str, str, tuple[str, str, str] | None]] = [
    (
        "Plan",
        "file",
        "Architect",
        "Writes the spec, plan and threat model",
        "No code before approval",
        ("gate", "Approve the plan", "Product owner, tech lead"),
    ),
    (
        "Code",
        "code",
        "Coder + reviewer",
        "Builds in phases with tests; a subagent reviews",
        "Pre-push scan",
        None,
    ),
    (
        "Build and test",
        "flask",
        "QA",
        "Opens the PR, fixes every finding",
        "Semgrep · CodeQL · Trivy · Checkov",
        None,
    ),
    (
        "Release",
        "merge",
        "Merges",
        "Answers review, merges once approved",
        "Protected main",
        ("gate", "Approve the PR", "Another engineer"),
    ),
    (
        "Deploy",
        "rocket",
        "No agent",
        '<span class="none">Can&rsquo;t deploy</span>',
        "Pipeline plans, then applies",
        ("hard", "Approve every apply", "Release manager"),
    ),
    (
        "Operate",
        "activity",
        "SRE · next",
        "Turns findings into the next change",
        "Weekly rescans · Dependabot",
        ("gate", "Own incidents", "On-call engineer"),
    ),
]


def person_cell(i: int, person: tuple[str, str, str] | None) -> str:
    last = " last" if i == len(STAGES) - 1 else ""
    if person is None:
        if i != 1:
            return ""  # The automatic cell spans this row and the one before it.
        return (
            '<div class="c p auto" style="grid-row:span 2">'
            f'{icon("loop", "var(--accent-2)", 44)}<div style="margin-top:8px">Auto-retry</div>'
            '<div class="who">until every check passes</div></div>'
        )
    kind, text, who = person
    if kind == "hard":
        tag = f'<span class="tag hard">{icon("lock", "currentColor", 18)}HARD GATE</span>'
        return f'<div class="c p hard{last}">{tag}{text}<span class="who">{who}</span></div>'
    tag = f'<span class="tag">{icon("check", "currentColor", 18)}GATE</span>'
    return f'<div class="c p{last}">{tag}{text}<span class="who">{who}</span></div>'


def column(icon_name: str, color: str, label: str, extra: str = "") -> str:
    ic = icon(icon_name, color, 24)
    return f'<div class="h{extra}">{ic}<span class="label">{label}</span></div>'


def lifecycle() -> str:
    cells = [
        '<div class="h"><span class="label">Stage</span></div>',
        column("bot", "var(--accent)", "Agent does"),
        column("shield", "var(--accent)", "Checks · automatic"),
        column("user", "var(--accent-2)", "People decide", " p"),
    ]
    for i, (stage, ic, role, agent, control, person) in enumerate(STAGES):
        cells.append(
            f'<div class="c s">{badge(ic, 52)}<div><div class="st">{stage}</div>'
            f'<div class="role">{role}</div></div></div>'
        )
        cells.append(f'<div class="c">{agent}</div>')
        cells.append(f'<div class="c k">{control}</div>')
        cells.append(person_cell(i, person))
    notes = (
        '<div class="notes">'
        f'<div class="tile note">{badge("loop")}<div><b>Outer loop</b>'
        "<span>Production findings become the next spec change</span></div></div>"
        f'<div class="tile note">{badge("lock")}<div><b>Guardrails everywhere</b>'
        "<span>Least privilege, no secrets, pinned packages</span></div></div></div>"
    )
    body = (
        header("The secure agentic SDLC", "Agents do the work. Controls check it. People decide.")
        + f'<div class="grid">{"".join(cells)}</div>'
        + notes
        + foot("3 / 3")
    )
    return page(LIFECYCLE_CSS, body)


# 4. Social preview -------------------------------------------------------------------------------
SOCIAL_CSS = """
.page { height: 640px; padding: 72px 80px; display: flex; flex-direction: column; }
.page h1 { font-size: 76px; max-width: 16ch; margin-top: 22px; }
.page .lead { font-size: 24px; max-width: 46ch; margin-top: 20px; }
.row { margin-top: auto; display: flex; gap: 10px; flex-wrap: wrap; }
.row span {
  font-family: var(--fm); font-size: 15px; padding: 7px 12px; border-radius: 4px;
  border: 1px solid var(--line-2); color: var(--ink-2); background: var(--bg-2);
}
.row span.on { color: var(--on-ink); background: var(--bg-ink); border-color: var(--bg-ink); }
"""


def social() -> str:
    stages = ["Plan", "Code", "Build and test", "Release", "Deploy", "Operate"]
    row = "".join(f"<span>{s}</span>" for s in stages)
    body = (
        header(
            "sdlc-template",
            "Agents do the work. Controls check it. People decide.",
            "A starter for the secure agentic SDLC: agent rules, spec-driven docs, "
            "security checks and Terraform on AWS.",
        )
        + f'<div class="row"><span class="on">AGENTS.md</span>{row}</div>'
    )
    return page(SOCIAL_CSS, body)


# Rendering ---------------------------------------------------------------------------------------
MEASURE = (
    "<script>document.fonts.ready.then(() => {document.title = "
    "Math.ceil(document.querySelector('.page').getBoundingClientRect().height)})</script>"
)


def chrome(args: list[str]) -> str:
    """Runs headless Chrome on local files this script wrote, and returns what it prints."""
    base = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars"]
    cmd = [*base, "--virtual-time-budget=10000", *args]
    # Fixed program, and arguments this script builds from its own temporary files.
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", check=True)  # noqa: S603
    return result.stdout


def file_url(path: str) -> str:
    return "file:///" + path.replace("\\", "/")


def render(name: str, html: str, tmp: str, width: int = WIDTH) -> None:
    """Measures the page once its fonts load, then screenshots it at that height, at 2x."""
    html = html.replace(f"width: {WIDTH}px", f"width: {width}px")
    src = os.path.join(tmp, name + ".html")
    probe = os.path.join(tmp, name + "-probe.html")
    with open(src, "w", encoding="utf-8") as f:
        f.write(html)
    with open(probe, "w", encoding="utf-8") as f:
        f.write(html.replace("</body>", MEASURE + "</body>"))
    dom = chrome([f"--window-size={width},3000", "--dump-dom", file_url(probe)])
    height = int(dom.split("<title>")[1].split("</title>")[0])
    out = os.path.join(HERE, name + ".png")
    size = f"--window-size={width},{height}"
    chrome([size, "--force-device-scale-factor=2", f"--screenshot={out}", file_url(src)])
    print(f"{name}.png  {width}x{height}")


DIAGRAMS: dict[str, Callable[[], str]] = {
    "evolution": evolution,
    "harness": harness,
    "lifecycle": lifecycle,
    "social": social,
}

if __name__ == "__main__":
    wanted = sys.argv[1:] or list(DIAGRAMS)
    with tempfile.TemporaryDirectory() as tmp:
        for name in wanted:
            html = DIAGRAMS[name]()
            if name == "social":
                render(name, html.replace("__THEME__", "light"), tmp, width=1280)
                continue
            for theme in THEMES:
                suffix = "" if theme == "light" else "-dark"
                render(name + suffix, html.replace("__THEME__", theme), tmp)
