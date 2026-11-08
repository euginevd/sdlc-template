"""Builds the guide diagrams as HTML and renders each to a PNG beside this file.

Usage: python -I guides/assets/diagrams.py
Needs Google Chrome and a network connection for the fonts (Geist, Inter, Geist Mono).
"""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = os.environ.get("CHROME", r"C:\Program Files\Google\Chrome\Application\chrome.exe")
WIDTH = 1600

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Geist+Mono:wght@400;500;700&family=Inter:wght@400;500;600&display=swap');
:root {
  --bg:#fbf7f0; --bg-2:#fffdfa; --bg-3:#f3ece0; --bg-ink:#17120c; --on-ink:#f6efe3;
  --ink:#1b1610; --ink-2:#6e6457; --ink-3:#9a8e7e; --line:rgba(27,22,16,.10); --line-2:rgba(27,22,16,.16);
  --line-ink:rgba(246,239,227,.14); --on-ink-2:#b0a492;
  --accent:oklch(0.58 0.155 196); --accent-2:oklch(0.68 0.135 172); --teal-deep:#0c5c68;
  --warn:#b0700f; --warn-dark:oklch(0.80 0.13 74);
  --accent-tint:color-mix(in oklab, var(--accent) 7%, var(--bg-2));
  --accent-weak:color-mix(in oklab, var(--accent) 28%, transparent);
  --mint-tint:color-mix(in oklab, var(--accent-2) 11%, var(--bg-2));
  --fd:'Geist', system-ui, sans-serif; --fb:'Inter', system-ui, sans-serif; --fm:'Geist Mono', ui-monospace, monospace;
}
* { box-sizing:border-box; }
html, body { margin:0; background:var(--bg); }
.page { width:__W__px; padding:64px 72px 60px; background:var(--bg); color:var(--ink); font-family:var(--fb);
  position:relative; overflow:hidden; }
.page::before { content:""; position:absolute; inset:0; pointer-events:none;
  background-image:radial-gradient(var(--line) 1px, transparent 1.2px); background-size:26px 26px;
  -webkit-mask-image:radial-gradient(ellipse 70% 45% at 85% 0%, #000 0%, transparent 70%); }
.eyebrow { font-family:var(--fm); font-size:13px; letter-spacing:.18em; text-transform:uppercase; font-weight:700;
  color:var(--accent); display:flex; align-items:center; gap:12px; }
.eyebrow::before { content:""; width:28px; height:1px; background:var(--accent); }
h1 { font-family:var(--fd); font-weight:600; font-size:46px; letter-spacing:-.03em; line-height:1.04; margin:16px 0 0; max-width:30ch; }
.lead { color:var(--ink-2); font-size:19px; line-height:1.55; margin:14px 0 0; max-width:68ch; }
.label { font-family:var(--fm); font-size:12px; letter-spacing:.16em; text-transform:uppercase; font-weight:700; }
.ico { display:inline-block; vertical-align:middle; width:20px; height:20px; flex:none; }
.ico svg { width:100%; height:100%; display:block; }
.foot { margin-top:28px; display:flex; justify-content:space-between; color:var(--ink-3); font-family:var(--fm);
  font-size:12px; letter-spacing:.08em; }
""".replace("__W__", str(WIDTH))

ICONS = {
    "bot": '<path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "user": '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    "book": '<path d="M12 7v14"/><path d="M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3 3 3 0 0 0-3-3z"/>',
    "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
    "loop": '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>',
    "lock": '<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "cpu": '<rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/>',
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "down": '<path d="M12 5v14"/><path d="m19 12-7 7-7-7"/>',
}


def icon(name, color="currentColor", size=20):
    return (f'<span class="ico" style="width:{size}px;height:{size}px;color:{color}"><svg viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg></span>')


def page(css, body):
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><style>{CSS}{css}</style></head><body><div class="page">{body}</div></body></html>'


FOOT = '<div class="foot"><span>SDLC-TEMPLATE · GUIDES/03</span><span>{}</span></div>'


# 1. Evolution ------------------------------------------------------------------------------------
def evolution():
    eras = [
        ("1970s", "Waterfall", "One pass, from requirements to release.", "Feedback arrives at the end."),
        ("2001", "Agile", "Short sprints with customer feedback.", "Shipping is still slow and manual."),
        ("2009", "DevOps", "Dev and ops share one automated pipeline.", "Security is checked last."),
        ("2010s", "DevSecOps", "Security shifts left, into every stage.", "People still write every line."),
        ("2021", "AI-assisted", "Copilots suggest code while a person drives.", "Helps with coding, not delivery."),
        ("Now", "Secure agentic", "Agents plan, build and test. Controls check. People decide.", "Every DevSecOps control, plus agents."),
    ]
    css = """
.line { position:relative; margin-top:52px; display:grid; grid-template-columns:repeat(5,1fr) 1.15fr; gap:26px; }
.line::before { content:""; position:absolute; left:0; right:0; top:7px; height:1px; background:var(--line-2); }
.era { position:relative; padding-top:34px; }
.dot { position:absolute; top:0; left:0; width:15px; height:15px; border-radius:50%; background:var(--bg); border:2px solid var(--ink-3); }
.when { font-family:var(--fm); font-size:12px; letter-spacing:.14em; font-weight:700; color:var(--ink-3); text-transform:uppercase; }
.name { font-family:var(--fd); font-weight:600; font-size:24px; letter-spacing:-.02em; margin:6px 0 10px; }
.did { font-size:16px; line-height:1.5; color:var(--ink); min-height:72px; }
.gap { margin-top:16px; padding-top:14px; border-top:1px solid var(--line); }
.gap .label { color:var(--ink-3); font-size:11px; }
.gap p { margin:6px 0 0; font-size:15px; line-height:1.45; color:var(--ink-2); }
.era.now { padding-top:0; }
.era.now .card { background:var(--bg-ink); color:var(--on-ink); border-radius:18px; padding:30px 20px 22px; margin-top:4px; }
.era.now .dot { left:20px; z-index:1; }
.era.now .dot { background:var(--accent); border-color:var(--accent); box-shadow:0 0 0 6px var(--accent-weak); }
.era.now .when { color:var(--accent); }
.era.now .did { color:var(--on-ink); }
.era.now .gap { border-color:var(--line-ink); }
.era.now .gap .label { color:var(--accent-2); }
.era.now .gap p { color:var(--on-ink-2); }
.who { margin-top:40px; display:flex; align-items:center; gap:14px; flex-wrap:wrap; padding:18px 22px; border:1px solid var(--line);
  border-radius:14px; background:var(--bg-2); font-size:16px; color:var(--ink-2); }
.who b { color:var(--ink); font-weight:600; }
"""
    cols = []
    for i, (when, name, did, gap) in enumerate(eras):
        now = i == len(eras) - 1
        cols.append(f'<div class="era{" now" if now else ""}"><span class="dot"></span><div class="card">'
                    f'<div class="when">{when}</div><div class="name">{name}</div><div class="did">{did}</div>'
                    f'<div class="gap"><span class="label">{"What it keeps" if now else "What it left open"}</span><p>{gap}</p></div></div></div>')
    body = (f'<div class="eyebrow">How we got here</div><h1>Each step fixed the last one&rsquo;s biggest gap.</h1>'
            f'<p class="lead">Nothing earlier is thrown away. Agents are new workers on the same pipeline, with the same controls.</p>'
            f'<div class="line">{"".join(cols)}</div>'
            f'<div class="who"><span class="label" style="color:var(--ink-3)">Who writes the code</span>'
            f'<b>People</b>{icon("arrow", "var(--ink-3)", 18)}<b>People, with AI suggestions</b>{icon("arrow", "var(--ink-3)", 18)}'
            f'<b>Agents, inside rules people set and checks they can&rsquo;t skip</b></div>'
            + FOOT.format("1 / 3"))
    return page(css, body)


# 2. Harness --------------------------------------------------------------------------------------
def harness():
    css = """
.you { margin:44px auto 0; width:420px; text-align:center; padding:16px 20px; border-radius:100px; border:1px solid var(--line-2); background:var(--bg-2); }
.you b { font-family:var(--fd); font-size:20px; font-weight:600; letter-spacing:-.02em; display:inline-flex; align-items:center; gap:10px; }
.you span { display:block; color:var(--ink-2); font-size:15px; margin-top:2px; }
.down { display:flex; justify-content:center; margin:10px 0; color:var(--ink-3); }
.row { display:grid; grid-template-columns:1fr 1.05fr 1fr; gap:22px; align-items:stretch; }
.card { border:1px solid var(--line); background:var(--bg-2); border-radius:18px; padding:26px 26px 24px; }
.card h3 { font-family:var(--fd); font-weight:600; font-size:22px; letter-spacing:-.02em; margin:12px 0 4px; }
.card .sub { color:var(--ink-2); font-size:15px; margin:0 0 14px; }
.chips { display:flex; flex-wrap:wrap; gap:8px; }
.chip { font-family:var(--fm); font-size:13px; padding:6px 10px; border-radius:6px; border:1px solid var(--line-2); color:var(--ink); background:var(--bg); }
.agent { background:var(--bg-ink); color:var(--on-ink); border:0; text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center; }
.agent .label { color:var(--accent); }
.agent h3 { font-size:26px; margin:8px 0 18px; }
.model { display:inline-flex; align-items:center; gap:10px; padding:12px 22px; border-radius:100px; border:1px solid var(--line-ink);
  background:rgba(246,239,227,.06); font-family:var(--fd); font-weight:600; font-size:18px; }
.agent p { color:var(--on-ink-2); font-size:15px; margin:16px 0 0; }
.rails { margin-top:22px; border:1px solid var(--line); background:var(--bg-2); border-radius:18px; padding:26px 26px 28px; }
.rails .top { display:flex; align-items:baseline; justify-content:space-between; }
.rails h3 { font-family:var(--fd); font-weight:600; font-size:22px; letter-spacing:-.02em; margin:0; display:flex; gap:10px; align-items:center; }
.rails .top span { color:var(--ink-3); font-family:var(--fm); font-size:12px; letter-spacing:.14em; text-transform:uppercase; font-weight:700; }
.steps { margin-top:22px; display:grid; grid-template-columns:repeat(5,1fr); gap:16px; align-items:start; }
.barwrap { height:86px; display:flex; align-items:flex-end; margin-bottom:14px; }
.bar { width:100%; border-radius:10px 10px 4px 4px; background:var(--accent); }
.step .label { color:var(--teal-deep); }
.step p { margin:6px 0 0; font-size:15px; line-height:1.45; color:var(--ink-2); }
"""
    steps = [("1 · Asked", "AGENTS.md rules", 18), ("2 · Checked", "Pre-push scan", 34), ("3 · Enforced", "Required PR checks, protected main", 50),
             ("4 · Limited", "AWS only in the pipeline, read-only plan role", 66), ("5 · Approved", "You sign off the merge and every deploy", 82)]
    bars = "".join(f'<div class="step"><div class="barwrap"><div class="bar" style="height:{h}px;opacity:{0.28 + i * 0.18:.2f}"></div></div><span class="label">{k}</span><p>{v}</p></div>'
                   for i, (k, v, h) in enumerate(steps))
    chips = lambda items: '<div class="chips">' + "".join(f'<span class="chip">{c}</span>' for c in items) + "</div>"
    body = (f'<div class="eyebrow">The harness</div><h1>An agent is a model inside a harness.</h1>'
            f'<p class="lead">The model writes the code. The harness decides what it knows, what it can touch and what stops it.</p>'
            f'<div class="you"><b>{icon("user", "var(--ink)", 20)}You</b><span>set the goal and approve each gate</span></div>'
            f'<div class="down">{icon("down", "var(--ink-3)", 22)}</div>'
            f'<div class="row">'
            f'<div class="card">{icon("book", "var(--teal-deep)", 24)}<h3>Context</h3><p class="sub">What it knows</p>'
            + chips(["AGENTS.md", "business context", "spec", "plan", "threat model", "code standards", "status", "decisions"])
            + f'</div><div class="card agent"><span class="label">The agent</span><h3>Coding agent</h3>'
            f'<span class="model">{icon("cpu", "var(--accent)", 20)}Model</span><p>plans, writes, tests, fixes</p></div>'
            f'<div class="card">{icon("wrench", "var(--teal-deep)", 24)}<h3>Tools</h3><p class="sub">What it can touch</p>'
            + chips(["git", "gh", "uv", "npm", "terraform validate", "local scanners", "review subagents"])
            + f'</div></div>'
            f'<div class="rails"><div class="top"><h3>{icon("lock", "var(--teal-deep)", 22)}Guardrails: what stops it</h3><span>Weakest to strongest</span></div>'
            f'<div class="steps">{bars}</div></div>'
            + FOOT.format("2 / 3"))
    return page(css, body)


# 3. Lifecycle ------------------------------------------------------------------------------------
def lifecycle():
    rows = [
        ("Plan", "Spec · plan · threat model", "Drafts the spec, then the plan and threat model. No code yet.",
         "AGENTS.md: no code before the plan is approved.", ("gate", "You approve the spec and the plan.")),
        ("Code", "Phases · tests · commits", "Builds each phase with tests. A second agent reviews the diff.",
         "Pre-push scan for secrets and vulnerable packages.", None),
        ("Build and test", "Pull request · CI", "Opens the PR and fixes every finding at its cause.",
         "Required checks: tests, Semgrep, CodeQL, Gitleaks, Trivy, Checkov, Terraform plan.", None),
        ("Release", "Review · merge", "Answers review comments, then squash-merges once approved.",
         "Protected main: no direct push. Checks pass on the latest main.", ("gate", "You review the diff and the security summary, then approve.")),
        ("Deploy", "Terraform apply", "Can&rsquo;t deploy. Only the pipeline can.",
         "Plan with a read-only role, apply with a separate one, then a health check.", ("hard", "You approve every apply. Production runs only by hand.")),
        ("Operate and monitor", "Status · findings", "Updates status and decisions. Turns findings into the next change.",
         "Weekly rescans, Dependabot and alerts on failed runs.", ("gate", "You own incidents and decide what&rsquo;s next.")),
    ]
    css = """
.strip { margin-top:36px; display:flex; align-items:center; gap:12px; padding:14px 20px; border-radius:14px; background:var(--bg-3); font-size:15.5px; color:var(--ink-2); }
.strip b { color:var(--ink); font-weight:600; }
.strip .label { color:var(--teal-deep); }
.grid { margin-top:18px; display:grid; grid-template-columns:270px 1fr 1fr 330px; }
.h { padding:0 22px 12px; display:flex; align-items:center; gap:10px; color:var(--ink-2); }
.h.p { background:var(--bg-ink); color:var(--on-ink); border-radius:18px 18px 0 0; padding-top:18px; }
.c { padding:22px; border-top:1px solid var(--line); font-size:16.5px; line-height:1.5; display:flex; align-items:center; }
.c.s { flex-direction:column; align-items:flex-start; justify-content:center; }
.n { font-family:var(--fm); font-size:13px; font-weight:700; letter-spacing:.12em; color:var(--accent); }
.st { font-family:var(--fd); font-weight:600; font-size:23px; letter-spacing:-.02em; margin-top:2px; }
.sub { color:var(--ink-3); font-size:14px; margin-top:2px; }
.c.a { color:var(--ink); }
.c.k { color:var(--ink); background:var(--mint-tint); }
.c.p { background:var(--bg-ink); color:var(--on-ink); border-top-color:var(--line-ink); flex-direction:column; align-items:flex-start; justify-content:center; gap:6px; font-weight:500; }
.c.p.last { border-radius:0 0 18px 18px; }
.tag { font-family:var(--fm); font-size:12px; letter-spacing:.16em; font-weight:700; color:var(--accent); display:inline-flex; gap:8px; align-items:center; }
.tag.hard { color:var(--warn-dark); }
.c.p.hard { box-shadow:inset 0 0 0 2px var(--warn-dark); border-radius:6px; }
.c.p.auto { color:var(--on-ink-2); font-weight:400; }
.c.p.auto .tag { color:var(--accent-2); }
.notes { margin-top:22px; display:grid; grid-template-columns:1fr 1fr; gap:18px; }
.note { display:flex; gap:14px; align-items:flex-start; padding:18px 22px; border:1px solid var(--line); border-radius:14px; background:var(--bg-2); font-size:15.5px; line-height:1.5; color:var(--ink-2); }
.note b { color:var(--ink); font-weight:600; display:block; font-family:var(--fd); font-size:17px; letter-spacing:-.01em; margin-bottom:2px; }
"""
    cells = [f'<div class="h"><span class="label">Stage</span></div>',
             f'<div class="h">{icon("bot", "var(--teal-deep)")}<span class="label">Agent does</span></div>',
             f'<div class="h">{icon("shield", "var(--teal-deep)")}<span class="label">Controls check · automatic</span></div>',
             f'<div class="h p">{icon("user", "var(--accent)")}<span class="label">People decide</span></div>']
    for i, (stage, sub, agent, control, person) in enumerate(rows):
        cells.append(f'<div class="c s"><span class="n">0{i + 1}</span><span class="st">{stage}</span><span class="sub">{sub}</span></div>')
        cells.append(f'<div class="c a">{agent}</div>')
        cells.append(f'<div class="c k">{control}</div>')
        last = " last" if i == len(rows) - 1 else ""
        if person is None:
            if i == 1:
                cells.append(f'<div class="c p auto" style="grid-row:span 2"><span class="tag">{icon("loop", "currentColor", 16)}NO PERSON · INNER LOOP</span>'
                             f'The agent fixes the cause and reruns until every check passes. It never weakens a check to get a green run.</div>')
        elif person[0] == "hard":
            cells.append(f'<div class="c p hard{last}"><span class="tag hard">{icon("lock", "currentColor", 16)}HARD GATE</span>{person[1]}</div>')
        else:
            cells.append(f'<div class="c p{last}"><span class="tag">GATE</span>{person[1]}</div>')
    body = (f'<div class="eyebrow">The secure agentic SDLC</div><h1>Agents do the work. Controls check it. People decide.</h1>'
            f'<p class="lead">Six stages, each with three parts. The checks block what fails, and a person approves before anything risky moves on.</p>'
            f'<div class="strip">{icon("book", "var(--teal-deep)")}<span class="label">Context, every stage</span>'
            f'<b>AGENTS.md · business context · spec · plan · threat model · decisions</b></div>'
            f'<div class="grid">{"".join(cells)}</div>'
            f'<div class="notes">'
            f'<div class="note">{icon("loop", "var(--teal-deep)", 22)}<div><b>Outer loop</b>What you learn in production, from incidents, rescans and users, becomes the next change to the spec.</div></div>'
            f'<div class="note">{icon("lock", "var(--teal-deep)", 22)}<div><b>Guardrails around every stage</b>Least-privilege roles, no secrets in reach, pinned week-old packages, and every change in Git.</div></div>'
            f'</div>' + FOOT.format("3 / 3"))
    return page(css, body)


def render(name, html, tmp):
    src = os.path.join(tmp, name + ".html")
    with open(src, "w", encoding="utf-8") as f:
        f.write(html)
    url = "file:///" + src.replace("\\", "/")
    args = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
            "--virtual-time-budget=10000", f"--window-size={WIDTH},3000"]
    # Measure the page height first, then screenshot exactly that tall.
    js = os.path.join(tmp, name + "-h.html")
    with open(js, "w", encoding="utf-8") as f:
        f.write(html.replace("</body>", "<script>document.fonts.ready.then(()=>{document.title=Math.ceil(document.querySelector('.page').getBoundingClientRect().height)})</script></body>"))
    dom = subprocess.run([*args, "--dump-dom", "file:///" + js.replace("\\", "/")], capture_output=True, text=True, encoding="utf-8").stdout
    height = int(dom.split("<title>")[1].split("</title>")[0])
    args[-1] = f"--window-size={WIDTH},{height}"
    out = os.path.join(HERE, name + ".png")
    subprocess.run([*args, f"--screenshot={out}", url], check=True, capture_output=True)
    print(f"{name}.png  {WIDTH}x{height}")


with tempfile.TemporaryDirectory() as tmp:
    for name, build in [("evolution", evolution), ("harness", harness), ("lifecycle", lifecycle)]:
        if len(sys.argv) == 1 or name in sys.argv[1:]:
            render(name, build(), tmp)
