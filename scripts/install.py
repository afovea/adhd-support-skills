#!/usr/bin/env python3
"""Install, update, verify or uninstall ADHD Support Skills. Standard library only.

Always say where and how — nothing is assumed:

  python3 install.py --host claude-code --project /path/to/project [--dry-run]
  python3 install.py --host codex --project /path/to/project
  python3 install.py --host claude-code --personal            # ~/.claude/skills, skills only
  python3 install.py --host codex --personal                  # ~/.agents/skills, skills only
  python3 install.py --host generic --skills-dir DIR --instructions FILE
  ... add --router-only (instructions block, no skills), --skills-only, --verify or --uninstall

What it does:
  - copies the self-contained skill folders and records each file's hash in
    <skills dir>/.adhd-support-skills.json (the ownership manifest);
  - adds or updates the router between managed markers in CLAUDE.md / AGENTS.md /
    your chosen file, leaving every other line untouched;
  - re-running updates in place; files you edited are kept and reported (--force replaces them);
  - --uninstall removes only files it installed and has not seen you change, plus the managed block.

It never enables telemetry, creates a personal profile or memory store, changes
health settings, schedules reminders, or touches a My Point of Truth folder.
"""
import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST = ".adhd-support-skills.json"
START, END = "<!-- adhd-support-skills:start -->", "<!-- adhd-support-skills:end -->"
LAYOUT = {  # host -> (skills dir, instructions file) relative to project / home
    "claude-code": {"project": (".claude/skills", "CLAUDE.md"), "personal": (".claude/skills", ".claude/CLAUDE.md")},
    "codex": {"project": (".agents/skills", "AGENTS.md"), "personal": (".agents/skills", ".codex/AGENTS.md")},
}


def bundle():
    """Locate built skills and router: next to this file in dist/, or in the repo's dist/."""
    for base in (HERE, HERE.parent / "dist"):
        if (base / "skills").is_dir() and (base / "generic/routing.md").is_file():
            return base / "skills", base / "generic/routing.md"
    sys.exit("error: built bundle not found. In the source repository run: python3 scripts/build.py dist")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def atomic_write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".tmp-")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, path)


class Plan:
    def __init__(self, dry):
        self.dry, self.lines, self.problems = dry, [], []

    def do(self, msg, fn=None):
        self.lines.append(("would " if self.dry else "") + msg)
        if fn and not self.dry:
            fn()

    def warn(self, msg):
        self.problems.append(msg)


def read_manifest(skills_dir):
    p = skills_dir / MANIFEST
    return json.loads(p.read_text()) if p.exists() else {"files": {}}


# ---------------------------------------------------------------- skills

def install_skills(src, dest, plan, force):
    old = read_manifest(dest)
    owned = old["files"]
    new_files = {}
    for skill in sorted(d for d in src.iterdir() if d.is_dir()):
        target = dest / skill.name
        if target.exists() and not any(k.startswith(skill.name + "/") for k in owned):
            plan.warn(f"{target} already exists and was not installed by this tool — left alone. "
                      "Remove or rename it, then re-run.")
            continue
        for f in sorted(p for p in skill.rglob("*") if p.is_file()):
            rel = f.relative_to(src).as_posix()
            out = dest / rel
            h = sha(f)
            new_files[rel] = h
            if out.exists():
                cur = sha(out)
                if cur == h:
                    continue
                if rel in owned and cur != owned[rel] and not force:
                    plan.warn(f"{out} was edited after install — kept your version (use --force to replace)")
                    new_files[rel] = owned[rel]
                    continue
                plan.do(f"update {out}", lambda f=f, out=out: shutil.copyfile(f, out))
            else:
                plan.do(f"add {out}", lambda f=f, out=out: (out.parent.mkdir(parents=True, exist_ok=True),
                                                             shutil.copyfile(f, out)))
    for rel, h in owned.items():  # files dropped from the new version
        out = dest / rel
        if rel not in new_files and out.exists():
            if sha(out) == h:
                plan.do(f"remove obsolete {out}", out.unlink)
            else:
                plan.warn(f"{out} is no longer shipped but you edited it — kept")
    if new_files != owned:
        plan.do(f"write ownership manifest {dest / MANIFEST}",
                lambda: atomic_write(dest / MANIFEST, json.dumps({"package": "adhd-support-skills",
                                                                   "files": new_files}, indent=1)))


def uninstall_skills(dest, plan):
    m = read_manifest(dest)
    if not m["files"]:
        plan.lines.append(f"no ownership manifest in {dest} — no skill files removed")
        return
    for rel, h in sorted(m["files"].items()):
        out = dest / rel
        if not out.exists():
            continue
        if sha(out) == h:
            plan.do(f"remove {out}", out.unlink)
        else:
            plan.warn(f"{out} was edited after install — kept")
    def prune():
        for d in sorted({(dest / r).parent for r in m["files"]}, key=lambda p: -len(p.parts)):
            while d != dest and d.exists() and not any(d.iterdir()):
                d.rmdir()
                d = d.parent
        (dest / MANIFEST).unlink(missing_ok=True)
    plan.do(f"remove empty skill folders and {dest / MANIFEST}", prune)


# ---------------------------------------------------------------- router

def set_block(instr, router, plan, remove=False):
    text = instr.read_text(encoding="utf-8") if instr.exists() else ""
    has = START in text and END in text
    if remove:
        if not has:
            plan.lines.append(f"no managed block in {instr}")
            return
        head, _, rest = text.partition(START)
        _, _, tail = rest.partition(END)
        new = (head.rstrip("\n") + "\n" + tail.lstrip("\n")) if head.strip() else tail.lstrip("\n")
        if new.strip():
            plan.do(f"remove managed router block from {instr}", lambda: atomic_write(instr, new))
        else:
            plan.do(f"remove {instr} (it held only the router block)", instr.unlink)
        return
    block = f"{START}\n{router.strip()}\n{END}"
    if has:
        head, _, rest = text.partition(START)
        _, _, tail = rest.partition(END)
        new = f"{head}{block}{tail}"
        if new == text:
            return
        plan.do(f"update managed router block in {instr}", lambda: atomic_write(instr, new))
    else:
        new = (text.rstrip("\n") + "\n\n" if text.strip() else "") + block + "\n"
        plan.do(f"{'append router block to' if text.strip() else 'create'} {instr}",
                lambda: atomic_write(instr, new))


# ------------------------------------------------------------------ main

def resolve(a):
    if a.host == "generic":
        if not (a.skills_dir or a.instructions):
            sys.exit("error: generic host needs --skills-dir and/or --instructions")
        return (Path(a.skills_dir).expanduser().resolve() if a.skills_dir else None,
                Path(a.instructions).expanduser().resolve() if a.instructions else None)
    if bool(a.project) == bool(a.personal):
        sys.exit("error: choose exactly one of --project PATH or --personal")
    if a.project:
        base = Path(a.project).expanduser().resolve()
        if not base.is_dir():
            sys.exit(f"error: project folder {base} does not exist")
        if (base / "skills-registry.yaml").exists():
            sys.exit("error: that is the ADHD Support Skills source repository itself; choose a different project")
        sd, inst = LAYOUT[a.host]["project"]
    else:
        base = Path.home()
        sd, inst = LAYOUT[a.host]["personal"]
    skills_dir, instr = base / sd, base / inst
    if a.personal and not a.router_only and not a.with_router:
        instr = None  # personal installs leave global instruction files alone unless asked
    return skills_dir, instr


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--host", required=True, choices=["claude-code", "codex", "generic"])
    where = ap.add_mutually_exclusive_group()
    where.add_argument("--project", help="project folder to install into")
    where.add_argument("--personal", action="store_true", help="your home skills folder (all projects)")
    ap.add_argument("--skills-dir", help="generic host: folder to copy skills into")
    ap.add_argument("--instructions", help="generic host: instruction file to add the router block to")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--skills-only", action="store_true")
    mode.add_argument("--router-only", action="store_true")
    ap.add_argument("--with-router", action="store_true", help="personal installs: also add the router block")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true", help="replace installed files you have edited")
    act = ap.add_mutually_exclusive_group()
    act.add_argument("--uninstall", action="store_true")
    act.add_argument("--verify", action="store_true")
    a = ap.parse_args(argv)

    skills_dir, instr = resolve(a)
    if a.skills_only:
        instr = None
    if a.router_only:
        skills_dir = None
    plan = Plan(a.dry_run or a.verify)

    if a.verify:
        src, _ = bundle()
        if skills_dir:
            m = read_manifest(skills_dir)["files"]
            want = sorted(d.name for d in src.iterdir() if d.is_dir())
            have = [n for n in want if (skills_dir / n / "SKILL.md").exists()]
            print(f"skills: {len(have)}/{len(want)} in {skills_dir}" + ("" if m else " (no ownership manifest)"))
            changed = [r for r, h in m.items() if (skills_dir / r).exists() and sha(skills_dir / r) != h]
            if changed:
                print(f"  edited since install: {len(changed)} file(s)")
        if instr:
            ok = instr.exists() and START in instr.read_text(encoding="utf-8")
            print(f"router block: {'present' if ok else 'missing'} in {instr}")
        return 0

    if a.uninstall:
        if skills_dir:
            uninstall_skills(skills_dir, plan)
        if instr:
            set_block(instr, None, plan, remove=True)
    else:
        src, router = bundle()
        if skills_dir:
            install_skills(src, skills_dir, plan, a.force)
        if instr:
            set_block(instr, router.read_text(encoding="utf-8"), plan)

    print(("DRY RUN — nothing changed\n" if a.dry_run else "") + ("\n".join(plan.lines) or "already up to date"))
    for p in plan.problems:
        print(f"note: {p}")
    if not a.dry_run and not a.uninstall and skills_dir:
        invoke = {"claude-code": "/adhd-help (plugin installs: /adhd-support-skills:adhd-help)",
                  "codex": "$adhd-help", "generic": "the adhd-help skill"}[a.host]
        print(f"\nTry an ordinary request such as \"I know what I need to do but can't start\", "
              f"or invoke {invoke}. Say \"quiet\", \"pause\" or \"stop\" at any time.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
