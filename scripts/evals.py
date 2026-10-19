#!/usr/bin/env python3
"""Behavioural evaluation tooling.

    python3 scripts/evals.py list
    python3 scripts/evals.py export --out DIR      # blind inputs (no expectations) + grading sheets
    python3 scripts/evals.py run-claude --out FILE # real Claude Code host, text-only cases
    python3 scripts/evals.py score TRANSCRIPTS.json [GRADES.json ...] --out RESULTS.json

Transcript format (one object per case):
    {"CASE-ID": {"route_observed": "adhd-start" | "none" | ..., "host": "...",
                 "turns": [{"user": "...", "assistant": "...", "tool_calls": ["name(args) -> result"]}]}}
Grades format: {"CASE-ID": {"pass": true|false, "violations": [...], "notes": "..."}}

A static check that a SKILL.md contains an instruction is not evidence the
agent follows it. Only `score` output built from real transcripts counts as an
observed outcome, and it records which host produced each transcript.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SUITES = ["routing", "behaviour", "safety", "memory"]


def load_cases():
    cases = []
    for suite in SUITES:
        d = yaml.safe_load((ROOT / "tests" / suite / "cases.yaml").read_text())
        for c in d["cases"]:
            merged = {"suite": suite, "skill": "router", "invocation": "natural", "prior_context": [],
                      "tools": {}, "regex_forbidden": [], "critical": False, **d.get("defaults", {}), **c}
            merged["capabilities"] = {**d.get("defaults", {}).get("capabilities", {}), **c.get("capabilities", {})}
            cases.append(merged)
    return cases


BLIND_KEYS = ("id", "invocation", "prior_context", "capabilities", "permissions", "tools", "turns")


def cmd_list(a):
    for c in load_cases():
        print(f"{c['id']:<14} {c['suite']:<9} turns={len(c['turns'])} critical={c['critical']} -> {c['expected_route']}")


def cmd_export(a):
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    cases = load_cases()
    blind = [{k: c[k] for k in BLIND_KEYS if k in c} for c in cases]
    (out / "blind-inputs.json").write_text(json.dumps(blind, indent=2, ensure_ascii=False))
    sheets = [{k: c[k] for k in ("id", "suite", "skill", "expected_route", "expected", "forbidden", "critical")}
              for c in cases]
    (out / "grading-sheets.json").write_text(json.dumps(sheets, indent=2, ensure_ascii=False))
    print(f"wrote {len(cases)} cases to {out}")


def regex_violations(case, transcript):
    text = "\n".join(t.get("assistant", "") for t in transcript.get("turns", []))
    return [p for p in case.get("regex_forbidden", []) if re.search(p, text)]


def route_ok(case, observed):
    want = case["expected_route"]
    if want == "safety":
        return True  # safety may be handled inside any skill; the grader judges it
    if want == "none" or want.startswith("control:"):
        return observed in (None, "none", "router")  # must not launch a support skill
    return observed == want


def cmd_score(a):
    cases = {c["id"]: c for c in load_cases()}
    transcripts = json.loads(Path(a.transcripts).read_text())
    grades = {}
    for g in a.grades:
        grades.update(json.loads(Path(g).read_text()))
    results, summary = {}, {"pass": 0, "fail": 0, "not_run": 0, "route_mismatch": [], "critical_fail": []}
    for cid, case in cases.items():
        t = transcripts.get(cid)
        if not t:
            results[cid] = {"status": "not run"}
            summary["not_run"] += 1
            continue
        rv = regex_violations(case, t)
        g = grades.get(cid, {})
        r_ok = route_ok(case, t.get("route_observed"))
        # Behaviour decides pass/fail; a different-but-defensible skill choice is
        # reported in route_ok rather than hidden or counted as unsafe.
        passed = bool(g.get("pass")) and not rv
        results[cid] = {"status": "pass" if passed else ("fail" if g else "ungraded"),
                        "host": t.get("host"), "route_expected": case["expected_route"],
                        "route_observed": t.get("route_observed"), "route_ok": r_ok,
                        "regex_violations": rv, "grader": g, "critical": case["critical"],
                        "capabilities": case["capabilities"], "permissions": case.get("permissions", []),
                        "prior_context": case["prior_context"], "turns": t.get("turns")}
        if not r_ok:
            summary["route_mismatch"].append(cid)
        if passed:
            summary["pass"] += 1
        elif g:
            summary["fail"] += 1
            if case["critical"]:
                summary["critical_fail"].append(cid)
    Path(a.out).write_text(json.dumps({"summary": summary, "results": results}, indent=2, ensure_ascii=False))
    print(json.dumps(summary, indent=2))
    return 1 if summary["critical_fail"] else 0


def cmd_run_claude(a):
    """Run text-only cases in Claude Code with the built plugin, isolated from user settings."""
    if not shutil.which("claude"):
        print("claude CLI not found; nothing run.")
        return 1
    plugin = ROOT / "dist/claude-code"
    work = Path(a.workdir)
    work.mkdir(parents=True, exist_ok=True)
    out = {}
    for c in load_cases():
        if c["tools"] or c["prior_context"]:
            continue  # needs the simulated harness; see docs/evaluation-plan.md
        sid, turns, route = str(uuid.uuid4()), [], None
        for i, msg in enumerate(c["turns"]):
            cmd = ["claude", "-p", "--plugin-dir", str(plugin), "--setting-sources", "project",
                   "--tools", "Skill,Read", "--allowedTools", "Skill Read", "--output-format", "stream-json",
                   "--verbose", "--max-budget-usd", str(a.budget)]
            cmd += (["--session-id", sid] if i == 0 else ["--resume", sid])
            if a.model:
                cmd += ["--model", a.model]
            proc = subprocess.run(cmd + [msg], cwd=work, capture_output=True, text=True, stdin=subprocess.DEVNULL)
            text, tools = [], []
            for line in proc.stdout.splitlines():
                try:
                    e = json.loads(line)
                except ValueError:
                    continue
                if e.get("type") == "assistant":
                    for part in e["message"]["content"]:
                        if part["type"] == "text":
                            text.append(part["text"])
                        elif part["type"] == "tool_use":
                            tools.append(f"{part['name']}({json.dumps(part['input'])[:200]})")
                            if part["name"] == "Skill" and route is None:
                                route = part["input"].get("skill", "").split(":")[-1]
            turns.append({"user": msg, "assistant": "\n".join(text), "tool_calls": tools})
        out[c["id"]] = {"host": "claude-code-cli", "route_observed": route or "none", "turns": turns}
        print(c["id"], route, (turns[-1]["assistant"][:80] if turns else ""))
    Path(a.out).write_text(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    p = sub.add_parser("export")
    p.add_argument("--out", required=True)
    p = sub.add_parser("score")
    p.add_argument("transcripts")
    p.add_argument("grades", nargs="*")
    p.add_argument("--out", required=True)
    p = sub.add_parser("run-claude")
    p.add_argument("--out", required=True)
    p.add_argument("--workdir", default=str(Path.home() / ".cache/adhd-support-skills-evals"))
    p.add_argument("--model")
    p.add_argument("--budget", type=float, default=0.5)
    a = ap.parse_args()
    return {"list": cmd_list, "export": cmd_export, "score": cmd_score, "run-claude": cmd_run_claude}[a.cmd](a) or 0


if __name__ == "__main__":
    sys.exit(main())
