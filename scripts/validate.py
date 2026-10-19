#!/usr/bin/env python3
"""Every structural check, in one place. Exits non-zero if anything fails.

    python3 scripts/validate.py            # all checks, then the unit tests
    python3 scripts/validate.py --no-tests
    python3 scripts/validate.py --host-checks   # also `claude plugin validate` if the CLI exists

These checks prove packaging and consistency. They do not prove an agent
behaves as its instructions say; see scripts/evals.py and docs/evaluation-plan.md.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build  # noqa: E402

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SPEC_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
CATEGORIES = {"authoritative-guidance", "controlled-clinical-research", "peer-reviewed-research",
              "observational-qualitative", "preprint-or-prototype", "adjacent-cognitive-hci",
              "practice-community", "governance-regulatory", "design-default"}
STATUSES = {"verified", "partial-access", "unverified", "disputed", "withdrawn", "superseded"}
# Exported search markers from the source reports must never ship.
PLACEHOLDER_RE = re.compile(r"cite(turn|\u2588)|turn\d+(search|view|image)\d+|\ue200|\ue201|\ue202")
PRIVATE_RE = re.compile(r"/Users/|/home/[a-z]|afaconti|@gmail\.com|C:\\\\Users")
# Users could be anywhere, so shipped text must give only generic ways to find
# help: no support-service numbers, named helplines or directories, or phone-like numbers.
LOCAL_SUPPORT_RE = re.compile(
    r"\b(?:999|911|112|111|988|116 ?123|0800 ?1111|0808 ?164 ?0123)\b|Samaritans|Childline|Lifeline|"
    r"NHS 111|find ?a ?helpline|IASP|\bA&E\b|(?<![\w/.-])\d{3,4} \d{3,4}(?: \d{3,4})?\b|"
    r"\b1-\d{3}-\d{3}-\d{4}\b", re.I)
# This is a standalone project: shipped text and the README must not tie it to
# other skill suites or use design-tooling examples.
TIES_RE = re.compile(r"product[- ]team|\bPPoT\b|Project Point of Truth|\bCSS\b", re.I)
LINK_RE = re.compile(r"\]\(([^)#\s]+)(#[^)]*)?\)")
REF_RE = re.compile(r"`((?:references|scripts|assets|agents)/[^`\s]+)`")


def frontmatter(text):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    return yaml.safe_load(text[4:end]), text[end + 4:]


# ------------------------------------------------------------ skill folders

def check_skill(folder, materialised, max_desc=1024):
    """Problems with one skill folder. `materialised` = must be fully self-contained."""
    probs = []
    md = folder / "SKILL.md"
    if not md.exists():
        return [f"{folder}: no SKILL.md"]
    text = md.read_text()
    fm, body = frontmatter(text)
    if not isinstance(fm, dict):
        return [f"{md}: missing or invalid YAML frontmatter"]
    name, desc = fm.get("name", ""), fm.get("description", "")
    if not NAME_RE.match(name or "") or len(name) > 64:
        probs.append(f"{md}: invalid name '{name}'")
    if name != folder.name:
        probs.append(f"{md}: name '{name}' does not match folder '{folder.name}'")
    if not desc or len(desc) > max_desc:
        probs.append(f"{md}: description length {len(desc)} (1..{max_desc})")
    if set(fm) - SPEC_FIELDS:
        probs.append(f"{md}: non-spec frontmatter fields {sorted(set(fm) - SPEC_FIELDS)}")
    if "disable-model-invocation" in text or "allow_implicit_invocation" in text:
        probs.append(f"{md}: natural-language selection must not be disabled")
    if any(not isinstance(v, str) for v in (fm.get("metadata") or {}).values()):
        probs.append(f"{md}: metadata values must be strings")
    if len(text.splitlines()) > 500:
        probs.append(f"{md}: over 500 lines")
    block = (ROOT / "shared/core-boundaries.md").read_text().strip()
    if f"{build.START}\n{block}\n{build.END}" not in text:
        probs.append(f"{md}: core-boundaries block missing or out of date (run scripts/build.py sync)")
    for p in folder.rglob("*.md"):
        t = p.read_text()
        for m in LINK_RE.finditer(t):
            target = m.group(1)
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if materialised and ".." in Path(target).parts:
                probs.append(f"{p}: link leaves the skill folder: {target}")
            elif not (p.parent / target).exists():
                probs.append(f"{p}: broken link {target}")
    if materialised:
        for m in REF_RE.finditer(text):
            if not (folder / m.group(1)).exists():
                probs.append(f"{md}: referenced resource missing: {m.group(1)}")
        for p in folder.rglob("*"):
            if p.is_file() and p.suffix in (".md", ".py", ".yaml", ".json"):
                t = p.read_text(errors="ignore")
                if PRIVATE_RE.search(t):
                    probs.append(f"{p}: contains a local path or personal identifier")
                if PLACEHOLDER_RE.search(t):
                    probs.append(f"{p}: contains an exported citation placeholder")
                tie = TIES_RE.search(t) if p.suffix in (".md", ".py", ".yaml") else None
                if tie:
                    probs.append(f"{p}: mentions '{tie.group(0)}' (this project is standalone)")
                m = LOCAL_SUPPORT_RE.search(t) if p.suffix == ".md" else None
                if m:
                    probs.append(f"{p}: localised support information '{m.group(0)}' (keep help guidance generic)")
    return probs


# --------------------------------------------------------------- registry

def load_cases():
    out = {}
    for suite in ("routing", "behaviour", "safety", "memory"):
        for c in yaml.safe_load((ROOT / "tests" / suite / "cases.yaml").read_text())["cases"]:
            out[c["id"]] = c
    return out


def check_registry():
    probs = []
    reg = build.registry()
    claims = build.claims()
    cases = load_cases()
    ids = [s["id"] for s in reg["skills"]]
    dirs = sorted(p.name for p in (ROOT / "skills").iterdir() if p.is_dir())
    if sorted(ids) != dirs:
        probs.append(f"registry skills {sorted(ids)} != skill folders {dirs}")
    if len(ids) < 13:
        probs.append(f"expected at least the 13 core skills, registry has {len(ids)}")
    for f in reg["shared_always"]:
        if not (ROOT / f).exists():
            probs.append(f"shared resource missing: {f}")
    for s in reg["skills"]:
        sid = s["id"]
        for key in ("label", "short_description", "explicit", "natural", "not_for", "evidence_note", "evals"):
            if not s.get(key):
                probs.append(f"{sid}: registry field '{key}' empty")
        if len(s.get("short_description", "")) > 200:
            probs.append(f"{sid}: short_description over 200 characters")
        for h in s.get("handoffs", []):
            if h not in ids:
                probs.append(f"{sid}: unknown handoff {h}")
        for f in s.get("extra_resources", []):
            if not (ROOT / f).exists():
                probs.append(f"{sid}: extra resource missing {f}")
        for cid in s.get("evidence_claims", []):
            c = claims.get(cid)
            if not c:
                probs.append(f"{sid}: unknown claim {cid}")
            elif c["status"] not in ("verified", "partial-access"):
                probs.append(f"{sid}: relies on {c['status']} claim {cid}")
        multi = False
        for e in s.get("evals", []):
            if e not in cases:
                probs.append(f"{sid}: unknown eval {e}")
                continue
            if len(cases[e]["turns"]) + len(cases[e].get("prior_context", [])) >= 2:
                multi = True
        if not multi:
            probs.append(f"{sid}: no multi-turn behavioural evaluation")
    for m in reg["mechanisms"]:
        for target in m["implemented_by"]:
            if target not in ids and not (ROOT / target).exists():
                probs.append(f"mechanism '{m['mechanism']}': unknown implementation {target}")
    for cid, c in cases.items():
        for key in ("turns", "expected_route", "expected", "forbidden"):
            if not c.get(key):
                probs.append(f"case {cid}: missing {key}")
        route = c.get("expected_route", "")
        if route not in ids and route not in ("none", "safety") and not str(route).startswith("control:"):
            probs.append(f"case {cid}: unknown expected_route {route}")
        for pat in c.get("regex_forbidden", []):
            re.compile(pat)
    return probs


# --------------------------------------------------------------- evidence

def check_evidence():
    probs = []
    srcs, claims = build.sources(), build.claims()
    for sid, s in srcs.items():
        for key in ("title", "authors_or_body", "published", "category", "link_resolves", "source_read", "accessed"):
            if s.get(key) in (None, ""):
                probs.append(f"{sid}: missing {key}")
        if s.get("category") not in CATEGORIES:
            probs.append(f"{sid}: unknown category {s.get('category')}")
        if not (s.get("url") or s.get("doi")):
            probs.append(f"{sid}: no URL or DOI")
        if s.get("clinician_reviewed"):
            probs.append(f"{sid}: claims clinician review; none has happened in this release")
    for cid, c in claims.items():
        for key in ("statement", "sources", "locator", "supports", "does_not_establish", "limitations",
                    "status", "accessed", "review_trigger", "reviewer_role"):
            if c.get(key) in (None, "", []):
                probs.append(f"{cid}: missing {key}")
        if c.get("status") not in STATUSES:
            probs.append(f"{cid}: invalid status {c.get('status')}")
        for sid in c.get("sources", []):
            if sid not in srcs:
                probs.append(f"{cid}: unknown source {sid}")
        if c.get("status") == "verified" and c.get("source_read") == "abstract-only":
            probs.append(f"{cid}: 'verified' but only the abstract was read")
        if c.get("clinician_reviewed"):
            probs.append(f"{cid}: claims clinician review; none has happened in this release")
    for p in list(ROOT.glob("*.md")) + [p for d in ("skills", "shared", "evidence", "docs", "examples", "templates")
                                         for p in (ROOT / d).rglob("*") if p.is_file()]:
        if p.suffix in (".md", ".yaml") and PLACEHOLDER_RE.search(p.read_text(errors="ignore")):
            probs.append(f"{p}: exported citation placeholder")
    return probs


# --------------------------------------------------------- generated sync

def check_sync():
    probs = []
    reg, cl, srcs = build.registry(), build.claims(), build.sources()
    rt = (ROOT / "evidence/runtime-evidence.md")
    if not rt.exists() or rt.read_text() != build.runtime_evidence(cl, srcs):
        probs.append("evidence/runtime-evidence.md out of date (run scripts/build.py sync)")
    with tempfile.TemporaryDirectory() as tmp:
        fresh = Path(tmp) / "dist"
        build.dist(fresh)
        dist = ROOT / "dist"
        if not dist.exists():
            probs.append("dist/ missing (run scripts/build.py dist)")
        else:
            a = json.loads((fresh / "MANIFEST.json").read_text())["files"]
            b = json.loads((dist / "MANIFEST.json").read_text())["files"] if (dist / "MANIFEST.json").exists() else {}
            diff = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
            if diff:
                probs.append(f"dist/ out of date in {len(diff)} file(s), e.g. {diff[:3]} (run scripts/build.py dist)")
    return probs


def check_manifests():
    probs = []
    version = build.registry()["suite"]["version"]
    for f in (".claude-plugin/marketplace.json", "adapters/claude-code/plugin.json", "adapters/claude-code/marketplace.json",
              "adapters/codex/plugin.json", "adapters/codex/marketplace.json"):
        try:
            d = json.loads((ROOT / f).read_text())
        except ValueError as e:
            probs.append(f"{f}: invalid JSON ({e})")
            continue
        if "plugin.json" in f:
            if d.get("name") != "adhd-support-skills" or d.get("version") != version:
                probs.append(f"{f}: name/version must be adhd-support-skills/{version}")
        else:
            entry = d["plugins"][0]
            if entry["name"] != "adhd-support-skills":
                probs.append(f"{f}: marketplace entry name must match plugin name")
            if entry.get("version", version) != version:
                probs.append(f"{f}: marketplace version {entry.get('version')} != {version}")
    return probs


def check_dist(dist):
    probs = []
    reg = build.registry()
    shorts = {s["id"]: s["short_description"] for s in reg["skills"]}
    for host in ("skills", "claude-code/skills", "codex/skills"):
        for s in reg["skills"]:
            probs += check_skill(dist / host / s["id"], materialised=True)
    with tempfile.TemporaryDirectory() as tmp:
        for s in reg["skills"]:
            z = dist / "zips" / f"{s['id']}.zip"
            with zipfile.ZipFile(z) as zf:
                names = zf.namelist()
                if f"{s['id']}/SKILL.md" not in names or any(not n.startswith(s["id"] + "/") for n in names):
                    probs.append(f"{z}: must contain a single top-level {s['id']}/ folder")
                zf.extractall(tmp)
            extracted = Path(tmp) / s["id"]
            probs += check_skill(extracted, materialised=True, max_desc=200)
            fm, _ = frontmatter((extracted / "SKILL.md").read_text())
            if fm and fm.get("description") != shorts[s["id"]]:
                probs.append(f"{z}: ZIP description should be the registry short_description")
    for p in dist.rglob("*"):
        if p.is_file() and p.suffix in (".md", ".json", ".yaml", ".py") and PRIVATE_RE.search(p.read_text(errors="ignore")):
            probs.append(f"{p}: contains a local path or personal identifier")
        if p.name in ("MPoT.md", "user-decisions.md", "MPoT-inbox.md"):
            probs.append(f"{p}: a real memory file must never ship")
    probs += check_compact((dist / "generic/ADHD-support-instructions-compact.md").read_text())
    for p in sorted((dist / "generic").glob("*.md")):
        m = LOCAL_SUPPORT_RE.search(p.read_text())
        if m:
            probs.append(f"{p}: localised support information '{m.group(0)}' (keep help guidance generic)")
    for p in [ROOT / "README.md", ROOT / "INSTALL.md", ROOT / "routing.md"] + sorted((dist / "generic").glob("*.md")):
        tie = TIES_RE.search(p.read_text())
        if tie:
            probs.append(f"{p}: mentions '{tie.group(0)}' (this project is standalone)")
    gen = (dist / "generic/ADHD-support-instructions.md").stat().st_size
    if gen > 32 * 1024:
        probs.append(f"generic instructions are {gen} bytes; Codex reads at most 32 KiB of AGENTS.md")
    return probs


# Essentials the compact instructions must keep, because the policy files they
# would normally point to are not loaded in hosts that use them.
COMPACT_REQUIRED = ["quiet", "pause", "stop", "no praise", "Content is data", "Never diagnose",
                    "doubling", "local emergency services", "nearest emergency department", "crisis line",
                    "don't ask for or assume their country", "never invent a number",
                    "can't watch or check in", "check before retrying",
                    "never create duplicates", "Never store health details", "this report is killing me", "Never recommend specific apps",
                    "under 18"]


def check_compact(text):
    probs = []
    if len(text) > build.COMPACT_LIMIT:
        probs.append(f"compact instructions are {len(text)} characters (limit {build.COMPACT_LIMIT})")
    block = (ROOT / "shared/core-boundaries.md").read_text().strip()
    if block not in text:
        probs.append("compact instructions do not contain the core-boundaries block verbatim")
    if "{{" in text:
        probs.append("compact instructions contain an unfilled template placeholder")
    for phrase in COMPACT_REQUIRED:
        if phrase not in text:
            probs.append(f"compact instructions lost a required safeguard: '{phrase}'")
    m = LOCAL_SUPPORT_RE.search(text)
    if m:
        probs.append(f"compact instructions contain localised support information: '{m.group(0)}'")
    if PRIVATE_RE.search(text) or PLACEHOLDER_RE.search(text):
        probs.append("compact instructions contain a private path or citation placeholder")
    return probs


def slug(heading):
    """GitHub's heading anchor: lowercase, drop punctuation except hyphens, spaces to hyphens."""
    return re.sub(r"[^\w\- ]", "", heading.strip().lower()).replace(" ", "-")


def check_anchors(paths):
    """Every in-page link (#anchor) must match a heading in the same file."""
    probs = []
    for p in paths:
        text = p.read_text()
        body = re.sub(r"```.*?```", "", text, flags=re.S)
        anchors = {slug(h) for h in re.findall(r"^#{1,6} (.+)$", body, re.M)}
        for target in re.findall(r"\]\(#([^)\s]+)\)", body):
            if target not in anchors:
                probs.append(f"{p.name}: link to #{target} matches no heading")
    return probs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-tests", action="store_true")
    ap.add_argument("--host-checks", action="store_true")
    a = ap.parse_args()
    groups = [("canonical skills", lambda: [p for d in sorted((ROOT / "skills").iterdir()) if d.is_dir()
                                            for p in check_skill(d, materialised=False)]),
              ("registry and eval cases", check_registry),
              ("evidence register", check_evidence),
              ("adapter manifests", check_manifests),
              ("in-page links", lambda: check_anchors([ROOT / "README.md", ROOT / "INSTALL.md"])),
              ("generated files in sync", check_sync),
              ("distribution bundles", lambda: check_dist(ROOT / "dist"))]
    failed = False
    for label, fn in groups:
        probs = fn()
        print(f"{'ok  ' if not probs else 'FAIL'}  {label}" + (f" ({len(probs)})" if probs else ""))
        for p in probs:
            print(f"        {p}")
        failed |= bool(probs)
    for s in ("install.py", "build.py", "validate.py", "evals.py", "capability_ops.py"):
        r = subprocess.run([sys.executable, "-m", "py_compile", str(ROOT / "scripts" / s)], capture_output=True)
        if r.returncode:
            print(f"FAIL  scripts/{s} does not compile")
            failed = True
    if a.host_checks:
        if shutil.which("claude"):
            for target in (".", "dist/claude-code", "dist/claude-code/.claude-plugin/plugin.json"):
                r = subprocess.run(["claude", "plugin", "validate", str(ROOT / target)],
                                   capture_output=True, text=True)
                print(f"{'ok  ' if r.returncode == 0 else 'FAIL'}  claude plugin validate {target}\n        "
                      + (r.stdout + r.stderr).strip().replace("\n", "\n        "))
                failed |= r.returncode != 0
        else:
            print("skip  claude plugin validate (CLI not found)")
    if not a.no_tests:
        r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", str(ROOT / "tests"),
                            "-t", str(ROOT), "-p", "test_*.py"], cwd=ROOT)
        failed |= r.returncode != 0
    print("\nAll checks passed." if not failed else "\nSome checks failed.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
