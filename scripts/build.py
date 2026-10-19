#!/usr/bin/env python3
"""Sync generated sections into the canonical skills, and build distributable bundles.

    python3 scripts/build.py sync     # core boundaries, evidence cards, runtime evidence
    python3 scripts/build.py dist     # sync, then rebuild dist/ from scratch
    python3 scripts/build.py dist --out DIR

Canonical source: skills/, shared/, routing.md, evidence/, templates/, adapters/.
Generated (never edit by hand): the core-boundaries block inside each SKILL.md,
skills/*/references/evidence-card.md, evidence/runtime-evidence.md, dist/.

Requires PyYAML (a build-time dependency only; installed bundles need nothing).
"""
import argparse
import hashlib
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
START, END = "<!-- core-boundaries:start -->", "<!-- core-boundaries:end -->"
EXCLUDE = {".DS_Store", "__pycache__"}
ZIP_DATE = (2026, 1, 1, 0, 0, 0)  # fixed so ZIPs are reproducible
STATUS_LABEL = {"verified": "verified against the source",
                "partial-access": "checked against an abstract or summary only"}


def registry():
    return yaml.safe_load((ROOT / "skills-registry.yaml").read_text())


def claims():
    return {c["id"]: c for c in yaml.safe_load((ROOT / "evidence/claims.yaml").read_text())["claims"]}


def sources():
    return {s["id"]: s for s in yaml.safe_load((ROOT / "evidence/sources.yaml").read_text())["sources"]}


def write_if_changed(path, text):
    if not path.exists() or path.read_text() != text:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return True
    return False


def source_links(claim, srcs):
    out = []
    for sid in claim["sources"]:
        s = srcs[sid]
        url = s.get("url") or (f"https://doi.org/{s['doi']}" if s.get("doi") else "")
        out.append(f"[{s['title']}]({url})" if url else s["title"])
    return "; ".join(out)


# ------------------------------------------------------------------- sync

def sync():
    reg, cl, srcs = registry(), claims(), sources()
    changed = []
    block = (ROOT / "shared/core-boundaries.md").read_text().strip()
    for s in reg["skills"]:
        skill = ROOT / "skills" / s["id"] / "SKILL.md"
        text = skill.read_text()
        new = re.sub(re.escape(START) + r".*?" + re.escape(END), f"{START}\n{block}\n{END}", text, flags=re.S)
        if write_if_changed(skill, new):
            changed.append(str(skill.relative_to(ROOT)))
        card = [f"# Evidence card — {s['label']}", "", s["evidence_note"], ""]
        if s["evidence_claims"]:
            card += ["Use only these claims, within the scope stated. None of them tested this software.", ""]
            for cid in s["evidence_claims"]:
                c = cl[cid]
                card += [f"- **{cid}** ({STATUS_LABEL.get(c['status'], c['status'])}): {c['statement']}",
                         f"  Source: {source_links(c, srcs)}."]
            card.append("")
        card += ["Full register, statuses and limitations: `evidence/claims.yaml` in the source repository. "
                 "Runtime snapshot: `references/shared/runtime-evidence.md`. "
                 "No claim has been reviewed by a clinician.", ""]
        p = ROOT / "skills" / s["id"] / "references/evidence-card.md"
        if write_if_changed(p, "\n".join(card)):
            changed.append(str(p.relative_to(ROOT)))
    if write_if_changed(ROOT / "evidence/runtime-evidence.md", runtime_evidence(cl, srcs)):
        changed.append("evidence/runtime-evidence.md")
    return changed


def runtime_evidence(cl, srcs):
    lines = ["# Runtime evidence snapshot", "",
             "Generated from `evidence/claims.yaml`. Every claim was checked on its `accessed` date by the "
             "building agent. **No claim has been reviewed by a clinician.** Use these claims only within "
             "the scope stated. Say when the snapshot may be out of date. Never quote an effect size from "
             "an abstract-only claim.", ""]
    for status, heading, note in (
            ("verified", "Verified against the source", "You may state these, with the source link."),
            ("partial-access", "Checked against an abstract or summary only",
             "State these only with a hedge, e.g. \"a study summary reports…\". Do not quote numbers.")):
        lines += [f"## {heading}", "", note, ""]
        for cid, c in cl.items():
            if c["status"] != status:
                continue
            lines += [f"### {cid}", "", c["statement"], "",
                      f"- Source: {source_links(c, srcs)} ({c.get('locator', '')})",
                      f"- Does not establish: {c.get('does_not_establish', '').strip()}",
                      f"- Accessed: {c.get('accessed')}", ""]
    excluded = [cid for cid, c in cl.items() if c["status"] not in STATUS_LABEL]
    lines += ["## Excluded", "", "These claims are not asserted at runtime: " + (", ".join(excluded) or "none") + ".", ""]
    return "\n".join(lines)


# ------------------------------------------------------------------- dist

def copytree(src, dst):
    for p in sorted(src.rglob("*")):
        if any(part in EXCLUDE for part in p.parts):
            continue
        t = dst / p.relative_to(src)
        if p.is_dir():
            t.mkdir(parents=True, exist_ok=True)
        else:
            t.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(p, t)


def materialise(s, reg, dst):
    """One self-contained skill folder: no links outside itself."""
    copytree(ROOT / "skills" / s["id"], dst)
    shared = dst / "references/shared"
    shared.mkdir(parents=True, exist_ok=True)
    for f in reg["shared_always"]:
        shutil.copyfile(ROOT / f, shared / Path(f).name)
    for f in s.get("extra_resources", []):
        target = (dst / "references" / Path(f).name) if f.startswith("templates/") else (shared / Path(f).name)
        shutil.copyfile(ROOT / f, target)
    oy = {"interface": {"display_name": s["label"], "short_description": s["short_description"],
                        "default_prompt": f"Use ${s['id']}: {s['natural'][0]}"}}
    (dst / "agents").mkdir(exist_ok=True)
    (dst / "agents/openai.yaml").write_text(yaml.safe_dump(oy, sort_keys=False, allow_unicode=True))


def short_frontmatter(skill_md, short):
    text = skill_md.read_text()
    return re.sub(r"^description: .*$", "description: " + json.dumps(short, ensure_ascii=False), text,
                  count=1, flags=re.M)


def deterministic_zip(folder, zip_path, override=None):
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(folder.rglob("*")):
            if p.is_dir():
                continue
            arc = f"{folder.name}/{p.relative_to(folder).as_posix()}"
            info = zipfile.ZipInfo(arc, ZIP_DATE)
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            data = override(p) if override and p.name == "SKILL.md" and p.parent == folder else p.read_bytes()
            z.writestr(info, data)


def generic_instructions(reg):
    parts = ["<!-- ADHD Support Skills: single-file instructions for hosts without skill support. -->",
             (ROOT / "routing.md").read_text().strip(),
             (ROOT / "shared/core-boundaries.md").read_text().strip(),
             (ROOT / "shared/interaction-policy.md").read_text().strip(),
             (ROOT / "shared/safety-policy.md").read_text().strip(),
             (ROOT / "evidence/crisis-resources.md").read_text().strip(),
             "## Deeper skill behaviour\n\nFor a specific skill's full workflow, paste its `SKILL.md` from "
             "`dist/skills/<name>/` into the conversation, or attach the folder if your host allows files."]
    return "\n\n---\n\n".join(parts) + "\n"


def dist(out):
    reg = registry()
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    version = reg["suite"]["version"]
    for s in reg["skills"]:
        materialise(s, reg, out / "skills" / s["id"])
    for host in ("claude-code", "codex"):
        copytree(out / "skills", out / host / "skills")
    (out / "claude-code/.claude-plugin").mkdir(parents=True)
    for f in ("plugin.json", "marketplace.json"):
        shutil.copyfile(ROOT / "adapters/claude-code" / f, out / "claude-code/.claude-plugin" / f)
    shutil.copyfile(ROOT / "adapters/codex/plugin.json", out / "codex/plugin.json")
    (out / "codex/.agents/plugins").mkdir(parents=True)
    shutil.copyfile(ROOT / "adapters/codex/marketplace.json", out / "codex/.agents/plugins/marketplace.json")
    (out / "generic").mkdir()
    shutil.copyfile(ROOT / "routing.md", out / "generic/routing.md")
    (out / "generic/ADHD-support-instructions.md").write_text(generic_instructions(reg))
    shutil.copyfile(ROOT / "scripts/install.py", out / "install.py")
    (out / "zips").mkdir()
    for s in reg["skills"]:
        deterministic_zip(out / "skills" / s["id"], out / "zips" / f"{s['id']}.zip",
                          override=lambda p, s=s: short_frontmatter(p, s["short_description"]).encode())
    files = {}
    for p in sorted(out.rglob("*")):
        if p.is_file():
            files[p.relative_to(out).as_posix()] = {"sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                                                   "bytes": p.stat().st_size}
    manifest = {"package": reg["suite"]["package"], "version": version,
                "skills": [{"id": s["id"], "version": version} for s in reg["skills"]],
                "bundles": {"skills": "dist/skills (standalone Agent Skills folders)",
                            "claude-code": "dist/claude-code (plugin + local marketplace)",
                            "codex": "dist/codex (plugin + local marketplace)",
                            "generic": "dist/generic (router and single-file instructions)",
                            "zips": "dist/zips (claude.ai upload; descriptions shortened to <=200 chars)"},
                "files": files}
    (out / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["sync", "dist"])
    ap.add_argument("--out", type=Path, default=ROOT / "dist")
    a = ap.parse_args()
    changed = sync()
    for c in changed:
        print(f"synced {c}")
    if a.cmd == "dist":
        m = dist(a.out)
        print(f"built {a.out} — {len(m['skills'])} skills, {len(m['files'])} files, version {m['version']}")


if __name__ == "__main__":
    sys.exit(main())
