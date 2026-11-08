"""Turns scanner output into PR annotations and one security summary. Standard library only.

parse <tool> <report.json> <out.json>: print PR annotations, write a summary for the report job.
comment <dir> <sha>: build the PR comment from every summary in <dir>.
"""

import json
import pathlib
import sys

CHECKS = {
    "gitleaks": "Secrets",
    "trivy": "Packages and IaC",
    "checkov": "IaC policies",
    "semgrep": "Code",
}
MARKER = "<!-- security-report -->"


def rel(path):
    for prefix in ("/repo/", "/src/", "/"):
        if path.startswith(prefix):
            return path[len(prefix) :]
    return path


def esc(text):
    return str(text).replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def gitleaks(data):
    for f in data or []:
        yield f["File"], f.get("StartLine", 1), f["RuleID"], "Secret found (redacted)"


def trivy(data):
    for r in data.get("Results") or []:
        for v in r.get("Vulnerabilities") or []:
            fixed = v.get("FixedVersion") or "no fix yet"
            pkg = f"{v['PkgName']} {v['InstalledVersion']}"
            yield r["Target"], 1, v["VulnerabilityID"], f"{v['Severity']}: {pkg}, fixed in {fixed}"
        for m in r.get("Misconfigurations") or []:
            line = (m.get("CauseMetadata") or {}).get("StartLine") or 1
            yield r["Target"], line, m["ID"], f"{m['Severity']}: {m['Title']}"


def checkov(data):
    for block in data if isinstance(data, list) else [data]:
        for c in (block.get("results") or {}).get("failed_checks") or []:
            line = (c.get("file_line_range") or [1])[0]
            yield c["file_path"].lstrip("/"), line, c["check_id"], c["check_name"]


def semgrep(data):
    for r in data.get("results") or []:
        rule = r["check_id"].split(".")[-1]
        yield r["path"], r["start"]["line"], rule, r["extra"]["message"].split("\n")[0]


def findings(tool, data):
    """Yield (file, line, rule, message) for each finding."""
    yield from {"gitleaks": gitleaks, "trivy": trivy, "checkov": checkov, "semgrep": semgrep}[tool](
        data
    )


def skips(tool, data):
    if tool != "checkov":
        return 0
    return sum(
        (b.get("summary") or {}).get("skipped", 0)
        for b in (data if isinstance(data, list) else [data])
    )


def parse(tool, report, out):
    try:
        text = pathlib.Path(report).read_text(encoding="utf-8").strip()
        data = json.loads(text) if text else ([] if tool == "gitleaks" else {})
    except (OSError, json.JSONDecodeError):
        data = None
    if data is None:
        summary = {"tool": tool, "error": True, "count": 0, "top": [], "skips": 0}
    else:
        items = [(rel(f), int(line), rule, msg) for f, line, rule, msg in findings(tool, data)]
        for f, line, rule, msg in items[:50]:
            print(f"::error file={esc(f)},line={line},title={esc(tool + ' ' + rule)}::{esc(msg)}")
        top = [f"{rule}: {msg} ({f}:{line})" for f, line, rule, msg in items[:3]]
        summary = {
            "tool": tool,
            "error": False,
            "count": len(items),
            "top": top,
            "skips": skips(tool, data),
        }
    pathlib.Path(out).write_text(json.dumps(summary), encoding="utf-8")


def cell(text):
    return text.replace("|", "\\|").replace("\n", " ")


def comment(folder, sha):
    rows, failed = [], 0
    for tool, check in CHECKS.items():
        path = pathlib.Path(folder) / f"{tool}.json"
        s = (
            json.loads(path.read_text(encoding="utf-8"))
            if path.exists()
            else {"error": True, "count": 0, "top": [], "skips": 0}
        )
        if s["error"]:
            failed += 1
            result = "**Error:** the scan didn't finish; see the job log"
        elif s["count"]:
            failed += 1
            more = (
                f"<br>and {s['count'] - len(s['top'])} more" if s["count"] > len(s["top"]) else ""
            )
            result = f"**{s['count']} found:**<br>" + "<br>".join(cell(t) for t in s["top"]) + more
        else:
            result = "Pass"
        if s.get("skips"):
            result += f", {s['skips']} skips with reasons"
        rows.append(f"| {check} ({tool.capitalize()}) | {result} |")
    status = "all passed" if not failed else f"{failed} failed"
    print(f"{MARKER}\n### Security checks: {status} ({sha[:7]})\n")
    print("| Check | Result |\n|---|---|")
    print("\n".join(rows))
    if failed:
        print("\nEach finding is also marked on its line under Files changed.")


if __name__ == "__main__":
    if sys.argv[1] == "parse":
        parse(*sys.argv[2:5])
    else:
        comment(*sys.argv[2:4])
