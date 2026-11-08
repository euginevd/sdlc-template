"""Builds the guide diagrams as HTML and renders each to a PNG beside this file.

Usage: python -I guides/assets/diagrams.py [name ...]
Needs Google Chrome and a network connection for the fonts (Geist, Inter, Geist Mono).
"""

import os
import subprocess
import sys
import tempfile
from collections.abc import Callable

HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = os.environ.get("CHROME", r"C:\Program Files\Google\Chrome\Application\chrome.exe")
WIDTH = 1600
FONTS = (
    "https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700"
    "&family=Geist+Mono:wght@400;500;700&family=Inter:wght@400;500;600&display=swap"
)

# Colours, type and spacing from the ArcVault design system.
CSS = """
:root {
  --bg: #fbf7f0; --bg-2: #fffdfa; --bg-3: #f3ece0; --bg-ink: #17120c;
  --on-ink: #f6efe3; --on-ink-2: #b0a492;
  --ink: #1b1610; --ink-2: #6e6457; --ink-3: #9a8e7e;
  --line: rgba(27, 22, 16, .10); --line-2: rgba(27, 22, 16, .16);
  --line-ink: rgba(246, 239, 227, .14);
  --accent: oklch(0.58 0.155 196); --accent-2: oklch(0.68 0.135 172);
  --teal-deep: #0c5c68; --warn-dark: oklch(0.80 0.13 74);
  --accent-weak: color-mix(in oklab, var(--accent) 28%, transparent);
  --mint-tint: color-mix(in oklab, var(--accent-2) 11%, var(--bg-2));
  --fd: 'Geist', system-ui, sans-serif;
  --fb: 'Inter', system-ui, sans-serif;
  --fm: 'Geist Mono', ui-monospace, monospace;
}
* { box-sizing: border-box; }
html, body { margin: 0; background: var(--bg); }
.page {
  width: __W__px; padding: 64px 72px 60px; position: relative; overflow: hidden;
  background: var(--bg); color: var(--ink); font-family: var(--fb);
}
.page::before {
  content: ""; position: absolute; inset: 0; pointer-events: none;
  background-image: radial-gradient(var(--line) 1px, transparent 1.2px);
  background-size: 26px 26px;
  -webkit-mask-image: radial-gradient(ellipse 70% 45% at 85% 0%, #000 0%, transparent 70%);
}
.eyebrow {
  font-family: var(--fm); font-size: 13px; letter-spacing: .18em; text-transform: uppercase;
  font-weight: 700; color: var(--accent); display: flex; align-items: center; gap: 12px;
}
.eyebrow::before { content: ""; width: 28px; height: 1px; background: var(--accent); }
h1 {
  font-family: var(--fd); font-weight: 600; font-size: 46px; letter-spacing: -.03em;
  line-height: 1.04; margin: 16px 0 0; max-width: 30ch;
}
.lead {
  color: var(--ink-2); font-size: 19px; line-height: 1.55; margin: 14px 0 0; max-width: 68ch;
}
.label {
  font-family: var(--fm); font-size: 12px; letter-spacing: .16em; text-transform: uppercase;
  font-weight: 700;
}
.ico { display: inline-block; vertical-align: middle; flex: none; }
.ico svg { width: 100%; height: 100%; display: block; }
.foot {
  margin-top: 28px; display: flex; justify-content: space-between; color: var(--ink-3);
  font-family: var(--fm); font-size: 12px; letter-spacing: .08em;
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
    """A whole HTML document: the shared styles, this diagram's styles and its body."""
    head = f'<meta charset="utf-8"><link rel="stylesheet" href="{FONTS}">'
    head += f"<style>{CSS}{css}</style>"
    content = f'<body><div class="page">{body}</div></body>'
    return f'<!doctype html><html lang="en"><head>{head}</head>{content}</html>'


def foot(number: str) -> str:
    return f'<div class="foot"><span>SDLC-TEMPLATE · GUIDES/03</span><span>{number}</span></div>'


def header(eyebrow: str, title: str, lead: str) -> str:
    return f'<div class="eyebrow">{eyebrow}</div><h1>{title}</h1><p class="lead">{lead}</p>'


# 1. Evolution ------------------------------------------------------------------------------------
EVOLUTION_CSS = """
.line {
  position: relative; margin-top: 52px; display: grid;
  grid-template-columns: repeat(5, 1fr) 1.15fr; gap: 26px;
}
.line::before {
  content: ""; position: absolute; left: 0; right: 0; top: 7px; height: 1px;
  background: var(--line-2);
}
.era { position: relative; padding-top: 34px; }
.dot {
  position: absolute; top: 0; left: 0; width: 15px; height: 15px; border-radius: 50%;
  background: var(--bg); border: 2px solid var(--ink-3);
}
.when {
  font-family: var(--fm); font-size: 12px; letter-spacing: .14em; font-weight: 700;
  color: var(--ink-3); text-transform: uppercase;
}
.name {
  font-family: var(--fd); font-weight: 600; font-size: 24px; letter-spacing: -.02em;
  margin: 6px 0 10px;
}
.did { font-size: 16px; line-height: 1.5; color: var(--ink); min-height: 72px; }
.gap { margin-top: 16px; padding-top: 14px; border-top: 1px solid var(--line); }
.gap .label { color: var(--ink-3); font-size: 11px; }
.gap p { margin: 6px 0 0; font-size: 15px; line-height: 1.45; color: var(--ink-2); }
.era.now { padding-top: 0; }
.era.now .card {
  background: var(--bg-ink); color: var(--on-ink); border-radius: 18px;
  padding: 30px 20px 22px; margin-top: 4px;
}
.era.now .dot {
  left: 20px; z-index: 1; background: var(--accent); border-color: var(--accent);
  box-shadow: 0 0 0 6px var(--accent-weak);
}
.era.now .when { color: var(--accent); }
.era.now .did { color: var(--on-ink); }
.era.now .gap { border-color: var(--line-ink); }
.era.now .gap .label { color: var(--accent-2); }
.era.now .gap p { color: var(--on-ink-2); }
.who {
  margin-top: 40px; display: flex; align-items: center; gap: 14px; flex-wrap: wrap;
  padding: 18px 22px; border: 1px solid var(--line); border-radius: 14px;
  background: var(--bg-2); font-size: 16px; color: var(--ink-2);
}
.who b { color: var(--ink); font-weight: 600; }
"""

# When, name, what it did, and what it left open (or, for the last, what it keeps).
ERAS = [
    (
        "1970s",
        "Waterfall",
        "One pass, from requirements to release.",
        "Feedback arrives at the end.",
    ),
    (
        "2001",
        "Agile",
        "Short sprints with customer feedback.",
        "Shipping is still slow and manual.",
    ),
    (
        "2009",
        "DevOps",
        "Dev and ops share one automated pipeline.",
        "Security is checked last.",
    ),
    (
        "2010s",
        "DevSecOps",
        "Security shifts left, into every stage.",
        "People still write every line.",
    ),
    (
        "2021",
        "AI-assisted",
        "Copilots suggest code while a person drives.",
        "Helps with coding, not delivery.",
    ),
    (
        "Now",
        "Secure agentic",
        "Agents plan, build and test. Controls check. People decide.",
        "Every DevSecOps control, plus agents.",
    ),
]


def evolution() -> str:
    cols: list[str] = []
    for i, (when, name, did, gap) in enumerate(ERAS):
        now = i == len(ERAS) - 1
        label = "What it keeps" if now else "What it left open"
        cols.append(
            f'<div class="era{" now" if now else ""}"><span class="dot"></span>'
            f'<div class="card"><div class="when">{when}</div><div class="name">{name}</div>'
            f'<div class="did">{did}</div><div class="gap"><span class="label">{label}</span>'
            f"<p>{gap}</p></div></div></div>"
        )
    arrow = icon("arrow", "var(--ink-3)", 18)
    who = (
        '<div class="who"><span class="label" style="color:var(--ink-3)">'
        f"Who writes the code</span><b>People</b>{arrow}<b>People, with AI suggestions</b>"
        f"{arrow}<b>Agents, inside rules people set and checks they can&rsquo;t skip</b></div>"
    )
    body = (
        header(
            "How we got here",
            "Each step fixed the last one&rsquo;s biggest gap.",
            "Nothing earlier is thrown away. Agents are new workers on the same pipeline, "
            "with the same controls.",
        )
        + f'<div class="line">{"".join(cols)}</div>'
        + who
        + foot("1 / 3")
    )
    return page(EVOLUTION_CSS, body)


# 2. Harness --------------------------------------------------------------------------------------
HARNESS_CSS = """
.you {
  margin: 44px auto 0; width: 420px; text-align: center; padding: 16px 20px;
  border-radius: 100px; border: 1px solid var(--line-2); background: var(--bg-2);
}
.you b {
  font-family: var(--fd); font-size: 20px; font-weight: 600; letter-spacing: -.02em;
  display: inline-flex; align-items: center; gap: 10px;
}
.you span { display: block; color: var(--ink-2); font-size: 15px; margin-top: 2px; }
.down { display: flex; justify-content: center; margin: 10px 0; }
.row {
  display: grid; grid-template-columns: 1fr 1.05fr 1fr; gap: 22px; align-items: stretch;
}
.card {
  border: 1px solid var(--line); background: var(--bg-2); border-radius: 18px;
  padding: 26px 26px 24px;
}
.card h3 {
  font-family: var(--fd); font-weight: 600; font-size: 22px; letter-spacing: -.02em;
  margin: 12px 0 4px;
}
.card .sub { color: var(--ink-2); font-size: 15px; margin: 0 0 14px; }
.chips { display: flex; flex-wrap: wrap; gap: 8px; }
.chip {
  font-family: var(--fm); font-size: 13px; padding: 6px 10px; border-radius: 6px;
  border: 1px solid var(--line-2); color: var(--ink); background: var(--bg);
}
.agent {
  background: var(--bg-ink); color: var(--on-ink); border: 0; text-align: center;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.agent .label { color: var(--accent); }
.agent h3 { font-size: 26px; margin: 8px 0 18px; }
.model {
  display: inline-flex; align-items: center; gap: 10px; padding: 12px 22px;
  border-radius: 100px; border: 1px solid var(--line-ink);
  background: rgba(246, 239, 227, .06);
  font-family: var(--fd); font-weight: 600; font-size: 18px;
}
.agent p { color: var(--on-ink-2); font-size: 15px; margin: 16px 0 0; }
.rails {
  margin-top: 22px; border: 1px solid var(--line); background: var(--bg-2);
  border-radius: 18px; padding: 26px 26px 28px;
}
.rails .top { display: flex; align-items: baseline; justify-content: space-between; }
.rails h3 {
  font-family: var(--fd); font-weight: 600; font-size: 22px; letter-spacing: -.02em;
  margin: 0; display: flex; gap: 10px; align-items: center;
}
.rails .top span {
  color: var(--ink-3); font-family: var(--fm); font-size: 12px; letter-spacing: .14em;
  text-transform: uppercase; font-weight: 700;
}
.steps {
  margin-top: 22px; display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px;
  align-items: start;
}
.barwrap { height: 86px; display: flex; align-items: flex-end; margin-bottom: 14px; }
.bar { width: 100%; border-radius: 10px 10px 4px 4px; background: var(--accent); }
.step .label { color: var(--teal-deep); }
.step p { margin: 6px 0 0; font-size: 15px; line-height: 1.45; color: var(--ink-2); }
"""

GUARDRAILS = [
    ("1 · Asked", "AGENTS.md rules"),
    ("2 · Checked", "Pre-push scan"),
    ("3 · Enforced", "Required PR checks, protected main"),
    ("4 · Limited", "AWS only in the pipeline, read-only plan role"),
    ("5 · Approved", "You sign off the merge and every deploy"),
]
CONTEXT = [
    "AGENTS.md",
    "business context",
    "spec",
    "plan",
    "threat model",
    "code standards",
    "status",
    "decisions",
]
TOOLS = ["git", "gh", "uv", "npm", "terraform validate", "local scanners", "review subagents"]


def chips(items: list[str]) -> str:
    inner = "".join(f'<span class="chip">{c}</span>' for c in items)
    return f'<div class="chips">{inner}</div>'


def card(icon_name: str, title: str, sub: str, items: list[str]) -> str:
    return (
        f'<div class="card">{icon(icon_name, "var(--teal-deep)", 24)}<h3>{title}</h3>'
        f'<p class="sub">{sub}</p>{chips(items)}</div>'
    )


def step(i: int, name: str, what: str) -> str:
    bar = f'<div class="bar" style="height:{18 + i * 16}px;opacity:{0.28 + i * 0.18:.2f}"></div>'
    return (
        f'<div class="step"><div class="barwrap">{bar}</div>'
        f'<span class="label">{name}</span><p>{what}</p></div>'
    )


def harness() -> str:
    steps = "".join(step(i, name, what) for i, (name, what) in enumerate(GUARDRAILS))
    you = (
        f'<div class="you"><b>{icon("user", "var(--ink)", 20)}You</b>'
        "<span>set the goal and approve each gate</span></div>"
        f'<div class="down">{icon("down", "var(--ink-3)", 22)}</div>'
    )
    agent = (
        '<div class="card agent"><span class="label">The agent</span><h3>Coding agent</h3>'
        f'<span class="model">{icon("cpu", "var(--accent)", 20)}Model</span>'
        "<p>plans, writes, tests, fixes</p></div>"
    )
    context = card("book", "Context", "What it knows", CONTEXT)
    tools = card("wrench", "Tools", "What it can touch", TOOLS)
    rails = (
        f'<div class="rails"><div class="top"><h3>{icon("lock", "var(--teal-deep)", 22)}'
        "Guardrails: what stops it</h3><span>Weakest to strongest</span></div>"
        f'<div class="steps">{steps}</div></div>'
    )
    body = (
        header(
            "The harness",
            "An agent is a model inside a harness.",
            "The model writes the code. The harness decides what it knows, what it can touch "
            "and what stops it.",
        )
        + you
        + f'<div class="row">{context}{agent}{tools}</div>'
        + rails
        + foot("2 / 3")
    )
    return page(HARNESS_CSS, body)


# 3. Lifecycle ------------------------------------------------------------------------------------
LIFECYCLE_CSS = """
.strip {
  margin-top: 36px; display: flex; align-items: center; gap: 12px; padding: 14px 20px;
  border-radius: 14px; background: var(--bg-3); font-size: 15.5px; color: var(--ink-2);
}
.strip b { color: var(--ink); font-weight: 600; }
.strip .label { color: var(--teal-deep); }
.grid { margin-top: 18px; display: grid; grid-template-columns: 270px 1fr 1fr 330px; }
.h {
  padding: 0 22px 12px; display: flex; align-items: center; gap: 10px; color: var(--ink-2);
}
.h.p {
  background: var(--bg-ink); color: var(--on-ink); border-radius: 18px 18px 0 0;
  padding-top: 18px;
}
.c {
  padding: 22px; border-top: 1px solid var(--line); font-size: 16.5px; line-height: 1.5;
  display: flex; align-items: center;
}
.c.s { flex-direction: column; align-items: flex-start; justify-content: center; }
.n {
  font-family: var(--fm); font-size: 13px; font-weight: 700; letter-spacing: .12em;
  color: var(--accent);
}
.st {
  font-family: var(--fd); font-weight: 600; font-size: 23px; letter-spacing: -.02em;
  margin-top: 2px;
}
.sub { color: var(--ink-3); font-size: 14px; margin-top: 2px; }
.c.k { background: var(--mint-tint); }
.c.p {
  background: var(--bg-ink); color: var(--on-ink); border-top-color: var(--line-ink);
  flex-direction: column; align-items: flex-start; justify-content: center; gap: 6px;
  font-weight: 500;
}
.c.p.last { border-radius: 0 0 18px 18px; }
.tag {
  font-family: var(--fm); font-size: 12px; letter-spacing: .16em; font-weight: 700;
  color: var(--accent); display: inline-flex; gap: 8px; align-items: center;
}
.tag.hard { color: var(--warn-dark); }
.c.p.hard { box-shadow: inset 0 0 0 2px var(--warn-dark); border-radius: 6px; }
.c.p.auto { color: var(--on-ink-2); font-weight: 400; }
.c.p.auto .tag { color: var(--accent-2); }
.notes { margin-top: 22px; display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
.note {
  display: flex; gap: 14px; align-items: flex-start; padding: 18px 22px;
  border: 1px solid var(--line); border-radius: 14px; background: var(--bg-2);
  font-size: 15.5px; line-height: 1.5; color: var(--ink-2);
}
.note b {
  color: var(--ink); font-weight: 600; display: block; font-family: var(--fd);
  font-size: 17px; letter-spacing: -.01em; margin-bottom: 2px;
}
"""

# Stage, what it covers, what the agent does, what the controls check, and the person's gate:
# ("gate" or "hard", text), or None where the checks decide.
STAGES: list[tuple[str, str, str, str, tuple[str, str] | None]] = [
    (
        "Plan",
        "Spec · plan · threat model",
        "Drafts the spec, then the plan and threat model. No code yet.",
        "AGENTS.md: no code before the plan is approved.",
        ("gate", "You approve the spec and the plan."),
    ),
    (
        "Code",
        "Phases · tests · commits",
        "Builds each phase with tests. A second agent reviews the diff.",
        "Pre-push scan for secrets and vulnerable packages.",
        None,
    ),
    (
        "Build and test",
        "Pull request · CI",
        "Opens the PR and fixes every finding at its cause.",
        "Required checks: tests, Semgrep, CodeQL, Gitleaks, Trivy, Checkov, Terraform plan.",
        None,
    ),
    (
        "Release",
        "Review · merge",
        "Answers review comments, then squash-merges once approved.",
        "Protected main: no direct push. Checks pass on the latest main.",
        ("gate", "You review the diff and the security summary, then approve."),
    ),
    (
        "Deploy",
        "Terraform apply",
        "Can&rsquo;t deploy. Only the pipeline can.",
        "Plan with a read-only role, apply with a separate one, then a health check.",
        ("hard", "You approve every apply. Production runs only by hand."),
    ),
    (
        "Operate and monitor",
        "Status · findings",
        "Updates status and decisions. Turns findings into the next change.",
        "Weekly rescans, Dependabot and alerts on failed runs.",
        ("gate", "You own incidents and decide what&rsquo;s next."),
    ),
]


def person_cell(i: int, person: tuple[str, str] | None) -> str:
    last = " last" if i == len(STAGES) - 1 else ""
    if person is None:
        if i != 1:
            return ""  # The automatic cell spans this row and the one before it.
        tag = f'<span class="tag">{icon("loop", "currentColor", 16)}NO PERSON · INNER LOOP</span>'
        return (
            f'<div class="c p auto" style="grid-row:span 2">{tag}'
            "The agent fixes the cause and reruns until every check passes. "
            "It never weakens a check to get a green run.</div>"
        )
    kind, text = person
    if kind == "hard":
        tag = f'<span class="tag hard">{icon("lock", "currentColor", 16)}HARD GATE</span>'
        return f'<div class="c p hard{last}">{tag}{text}</div>'
    return f'<div class="c p{last}"><span class="tag">GATE</span>{text}</div>'


def column(icon_name: str, color: str, label: str, extra: str = "") -> str:
    return f'<div class="h{extra}">{icon(icon_name, color)}<span class="label">{label}</span></div>'


def lifecycle() -> str:
    cells = [
        '<div class="h"><span class="label">Stage</span></div>',
        column("bot", "var(--teal-deep)", "Agent does"),
        column("shield", "var(--teal-deep)", "Controls check · automatic"),
        column("user", "var(--accent)", "People decide", " p"),
    ]
    for i, (stage, sub, agent, control, person) in enumerate(STAGES):
        cells.append(
            f'<div class="c s"><span class="n">0{i + 1}</span><span class="st">{stage}</span>'
            f'<span class="sub">{sub}</span></div>'
        )
        cells.append(f'<div class="c">{agent}</div>')
        cells.append(f'<div class="c k">{control}</div>')
        cells.append(person_cell(i, person))
    strip = (
        f'<div class="strip">{icon("book", "var(--teal-deep)")}'
        '<span class="label">Context, every stage</span>'
        "<b>AGENTS.md · business context · spec · plan · threat model · decisions</b></div>"
    )
    notes = (
        f'<div class="notes"><div class="note">{icon("loop", "var(--teal-deep)", 22)}'
        "<div><b>Outer loop</b>What you learn in production, from incidents, rescans and "
        "users, becomes the next change to the spec.</div></div>"
        f'<div class="note">{icon("lock", "var(--teal-deep)", 22)}'
        "<div><b>Guardrails around every stage</b>Least-privilege roles, no secrets in reach, "
        "pinned week-old packages, and every change in Git.</div></div></div>"
    )
    body = (
        header(
            "The secure agentic SDLC",
            "Agents do the work. Controls check it. People decide.",
            "Six stages, each with three parts. The checks block what fails, and a person "
            "approves before anything risky moves on.",
        )
        + strip
        + f'<div class="grid">{"".join(cells)}</div>'
        + notes
        + foot("3 / 3")
    )
    return page(LIFECYCLE_CSS, body)


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


def render(name: str, html: str, tmp: str) -> None:
    """Measures the page once its fonts load, then screenshots it at that height, at 2x."""
    src = os.path.join(tmp, name + ".html")
    probe = os.path.join(tmp, name + "-probe.html")
    with open(src, "w", encoding="utf-8") as f:
        f.write(html)
    with open(probe, "w", encoding="utf-8") as f:
        f.write(html.replace("</body>", MEASURE + "</body>"))
    dom = chrome([f"--window-size={WIDTH},3000", "--dump-dom", file_url(probe)])
    height = int(dom.split("<title>")[1].split("</title>")[0])
    out = os.path.join(HERE, name + ".png")
    size = f"--window-size={WIDTH},{height}"
    chrome([size, "--force-device-scale-factor=2", f"--screenshot={out}", file_url(src)])
    print(f"{name}.png  {WIDTH}x{height}")


DIAGRAMS: dict[str, Callable[[], str]] = {
    "evolution": evolution,
    "harness": harness,
    "lifecycle": lifecycle,
}

if __name__ == "__main__":
    wanted = sys.argv[1:] or list(DIAGRAMS)
    with tempfile.TemporaryDirectory() as tmp:
        for name in wanted:
            render(name, DIAGRAMS[name](), tmp)
