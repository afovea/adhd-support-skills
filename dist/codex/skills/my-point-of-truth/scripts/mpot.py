#!/usr/bin/env python3
"""My Point of Truth (MPoT) store operations for ADHD Support Skills.

A private, human-governed register of working preferences kept as plain
Markdown in a folder the user chooses. Standard library only.

    python3 mpot.py --store DIR init
    python3 mpot.py --store DIR view [--scope TEXT] [--history]
    python3 mpot.py --store DIR add --type PREF --title T --statement S --scope SC
    python3 mpot.py --store DIR propose ...          (agent suggestion -> inbox)
    python3 mpot.py --store DIR approve ID | reject ID
    python3 mpot.py --store DIR supersede ID --statement S [--title T] [--scope SC]
    python3 mpot.py --store DIR decide --title T --decision D --scope SC ...
    python3 mpot.py --store DIR forget ID... | --match TEXT
    python3 mpot.py --store DIR reset --yes
    python3 mpot.py --store DIR export OUTFILE
    python3 mpot.py --store DIR import FILE [--to-inbox]
    python3 mpot.py --store DIR hash

The store may also come from the MPOT_STORE environment variable. There is no
default location: nothing is created unless the user chose a folder.

Every write takes a lock, re-reads the files, refuses if --expect-hash no
longer matches, and replaces files atomically. Exit codes: 0 ok, 1 error,
2 not found, 3 conflict, 4 refused.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import sys
import tempfile
import time
from pathlib import Path

REGISTER, INBOX, DECISIONS, STATE, LOCK = (
    "MPoT.md", "MPoT-inbox.md", "user-decisions.md", ".mpot-state.json", ".mpot.lock")
CACHE_DIR = ".cache"

TYPES = ["PREF", "GOAL", "CONSTRAINT", "CONTEXT", "VOCAB", "EXAMPLE", "ASM", "CONFLICT", "Q"]
STATUSES = ["proposed", "confirmed", "inferred", "provisional", "disputed", "superseded", "expired"]
CURRENT = {"confirmed", "provisional", "inferred", "disputed"}
ENTRY_FIELDS = ["Type", "Statement", "Scope", "Status", "Source", "Owner", "Observed", "Approved",
                "Review", "Sensitivity", "Retention", "Supersedes", "Superseded by"]
DECISION_FIELDS = ["Decision", "Status", "Scope", "Decided", "Decided by", "Context", "Rationale",
                   "Consequences", "Reconsider when", "Relates to", "Supersedes", "Superseded by"]
LINK_FIELDS = ("Supersedes", "Superseded by", "Relates to")

HEADERS = {
    REGISTER: "# My Point of Truth\n\nPrivate working preferences for ADHD Support Skills. "
              "Only entries you approve are confirmed. Plain text, not encrypted.\n\n## Entries\n\n",
    INBOX: "# MPoT inbox\n\nProposed entries waiting for your approval. "
           "Nothing here is used as confirmed.\n\n## Proposals\n\n",
    DECISIONS: "# User decisions\n\nConsequential decisions about how agents should work with you. "
               "Deletion requests override this history.\n\n## Decisions\n\n",
}

# Guards. Crisis content and secrets are never stored; health content needs an
# explicit, separate decision. Patterns are deliberately simple and over-match.
CRISIS_RE = re.compile(r"suicid|self[- ]?harm|kill (my|him|her|them)sel|overdos|end (my|it all)|crisis", re.I)
SECRET_RE = re.compile(r"password|passcode|api[ _-]?key|secret key|token\b|\bpin\b", re.I)
HEALTH_RE = re.compile(r"\badhd\b|diagnos|medicat|medicine|\bdose\b|\bmg\b|prescri|depress|anxiety|"
                       r"autis|bipolar|therap|psychiatr|disorder|symptom", re.I)
INJECTION_RE = re.compile(
    r"ignore (all |any |the |previous |prior |your )*(instructions|rules|safety|policy|policies)|"
    r"disregard|override|system prompt|jailbreak|pre-?approved|authori[sz]ed? to|grant(s|ed)? permission|"
    r"\b(send|email|upload|forward|share|post)\b.{0,40}\b(to|all)\b|"
    r"\binstall\b|\bexecute\b|\brun (this|the|a)\b|curl |wget |https?://", re.I)

HEAD_RE = re.compile(r"^### ([A-Z]+-\d+) — (.*)$")
FIELD_RE = re.compile(r"^- \*\*(.+?):\*\* ?(.*)$")


class Refused(Exception):
    code = 4


class Conflict(Exception):
    code = 3


class NotFound(Exception):
    code = 2


def today():
    return datetime.date.today().isoformat()


# ---------------------------------------------------------------- parsing

def parse(text):
    """Split a store file into (preamble, entries). Comment blocks are kept verbatim."""
    preamble, entries, cur, in_comment = [], [], None, False
    for line in text.splitlines():
        opens, closes = "<!--" in line, "-->" in line
        m = None if in_comment else HEAD_RE.match(line)
        if m:
            cur = {"id": m.group(1), "title": m.group(2).strip(), "fields": {}, "extra": []}
            entries.append(cur)
        elif cur is None:
            preamble.append(line)
        else:
            f = None if in_comment else FIELD_RE.match(line)
            if f:
                cur["fields"][f.group(1)] = f.group(2).strip()
            elif line.strip() or in_comment:
                cur["extra"].append(line)
        if opens and not closes:
            in_comment = True
        elif closes:
            in_comment = False
    return "\n".join(preamble).rstrip() + "\n\n", entries


def render(preamble, entries, order):
    out = [preamble.rstrip() + "\n"]
    for e in entries:
        lines = [f"### {e['id']} — {e['title']}"]
        keys = [k for k in order if k in e["fields"]] + [k for k in e["fields"] if k not in order]
        lines += [f"- **{k}:** {e['fields'][k]}" for k in keys]
        lines += e["extra"]
        out.append("\n".join(lines) + "\n")
    return "\n".join(out)


# ------------------------------------------------------------------ store

class Store:
    def __init__(self, path):
        self.dir = Path(path).expanduser().resolve()

    def p(self, name):
        return self.dir / name

    def exists(self):
        return self.p(REGISTER).exists()

    def read(self, name):
        path = self.p(name)
        if not path.exists():
            return HEADERS.get(name, ""), []
        return parse(path.read_text(encoding="utf-8"))

    def digest(self):
        h = hashlib.sha256()
        for name in (REGISTER, INBOX, DECISIONS):
            path = self.p(name)
            h.update(name.encode())
            h.update(path.read_bytes() if path.exists() else b"\0")
        return h.hexdigest()[:16]

    def write(self, name, preamble, entries):
        order = DECISION_FIELDS if name == DECISIONS else ENTRY_FIELDS
        atomic_write(self.p(name), render(preamble, entries, order))

    def state(self):
        try:
            return json.loads(self.p(STATE).read_text())
        except (OSError, ValueError):
            return {"next": {}}

    def next_id(self, prefix):
        seen = [0]
        for name in (REGISTER, INBOX, DECISIONS):
            for e in self.read(name)[1]:
                if e["id"].startswith(prefix + "-"):
                    seen.append(int(e["id"].split("-")[1]))
        st = self.state()
        n = max(max(seen) + 1, st["next"].get(prefix, 1))
        st["next"][prefix] = n + 1  # never reuse an ID, even after deletion
        atomic_write(self.p(STATE), json.dumps(st))
        return f"{prefix}-{n:03d}"

    def locked(self, expect_hash=None):
        return _Lock(self, expect_hash)


class _Lock:
    """Exclusive lock for a read-modify-write. Stale locks (>120 s) are broken."""

    def __init__(self, store, expect_hash):
        self.store, self.expect, self.fd = store, expect_hash, None

    def __enter__(self):
        path = self.store.p(LOCK)
        deadline = time.time() + 5
        while True:
            try:
                self.fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                break
            except FileExistsError:
                try:
                    if time.time() - path.stat().st_mtime > 120:
                        path.unlink()
                        continue
                except FileNotFoundError:
                    continue
                if time.time() > deadline:
                    raise Conflict("another write is in progress; try again")
                time.sleep(0.05)
        if self.expect and self.expect != self.store.digest():
            self.__exit__(None, None, None)
            raise Conflict("the store changed since you last read it; re-read and show the user "
                           "the current entries before writing")
        return self.store

    def __exit__(self, *exc):
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None
            try:
                self.store.p(LOCK).unlink()
            except FileNotFoundError:
                pass


def atomic_write(path, text):
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".tmp-", suffix=path.suffix)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


# ------------------------------------------------------------------ guards

def check_location(path):
    """Refuse locations inside a Git working tree or inside this plugin."""
    path = Path(path).expanduser().resolve()
    for parent in [path] + list(path.parents):
        if (parent / ".git").exists():
            raise Refused(f"{path} is inside a Git repository ({parent}). Choose a private folder "
                          "outside any project so preferences are never committed.")
        if (parent / "skills-registry.yaml").exists() or (parent / ".claude-plugin").exists() \
                or (parent / "SKILL.md").exists():
            raise Refused(f"{path} is inside the plugin itself ({parent}). Choose a private folder "
                          "outside the plugin.")


def check_content(texts, sensitivity, health_approved):
    blob = " ".join(t for t in texts if t)
    if CRISIS_RE.search(blob):
        raise Refused("Crisis or self-harm information is never stored in MPoT.")
    if SECRET_RE.search(blob):
        raise Refused("Passwords, keys and other secrets are never stored in MPoT.")
    if HEALTH_RE.search(blob) and not (sensitivity == "health" and health_approved):
        raise Refused("This looks like health information. Store the practical accommodation "
                      "instead (e.g. 'prefer written steps'), or, only if the user has explicitly "
                      "decided to keep it, repeat with --sensitivity health --health-approved.")


def require(store):
    if not store.exists():
        raise NotFound(f"No MPoT at {store.dir}. Memory is off; run 'init' only after the user "
                       "chooses this folder.")


def find(entries, eid):
    for i, e in enumerate(entries):
        if e["id"] == eid:
            return i, e
    return None, None


def new_entry(store, a, status, approved):
    eid = store.next_id(a.type)
    fields = {"Type": a.type, "Statement": a.statement, "Scope": a.scope, "Status": status,
              "Source": a.source or "user request in chat", "Owner": "user", "Observed": today(),
              "Approved": today() if approved else "pending", "Review": a.review or "when the user asks",
              "Sensitivity": a.sensitivity, "Retention": "until changed or deleted",
              "Supersedes": "none", "Superseded by": "none"}
    return {"id": eid, "title": a.title, "fields": fields, "extra": []}


# ---------------------------------------------------------------- commands

def cmd_init(store, a):
    check_location(store.dir)
    if store.exists():
        print(f"MPoT already exists at {store.dir}; nothing changed.")
        return
    store.dir.mkdir(parents=True, exist_ok=True)
    for name in (REGISTER, DECISIONS):
        atomic_write(store.p(name), HEADERS[name])
    print(f"Created MPoT at {store.dir}\n  {REGISTER}, {DECISIONS}\n"
          "Plain text, not encrypted. Delete with 'reset --yes' or by deleting the folder.")


def cmd_view(store, a):
    require(store)
    shown = 0
    for name, label in ((REGISTER, "Register"), (INBOX, "Proposals (not yet approved)"),
                        (DECISIONS, "Decision log")):
        entries = store.read(name)[1]
        if not a.history:
            entries = [e for e in entries if e["fields"].get("Status") not in ("superseded", "expired")]
        if a.scope:
            entries = [e for e in entries if a.scope.lower() in e["fields"].get("Scope", "").lower()
                       or e["fields"].get("Scope", "").lower() in ("all", "everything", "all tasks")]
        if not entries:
            continue
        print(f"## {label}")
        for e in entries:
            f = e["fields"]
            print(f"- {e['id']} [{f.get('Status', '?')}] {e['title']}: "
                  f"{f.get('Statement') or f.get('Decision', '')} (scope: {f.get('Scope', '?')})")
            shown += 1
    if not shown:
        print("Nothing stored.")
    print(f"hash: {store.digest()}")


def cmd_add(store, a, propose=False):
    require(store)
    if a.type not in TYPES:
        raise Refused(f"type must be one of {', '.join(TYPES)} (decisions use 'decide')")
    check_content([a.title, a.statement, a.scope], a.sensitivity, a.health_approved)
    with store.locked(a.expect_hash):
        name = INBOX if propose else REGISTER
        pre, entries = store.read(name)
        if not propose:
            for e in entries:
                if e["fields"].get("Status") in CURRENT and \
                        e["fields"].get("Statement", "").strip().lower() == a.statement.strip().lower():
                    print(f"Already stored as {e['id']}; nothing changed.")
                    return
        e = new_entry(store, a, "proposed" if propose else a.status, approved=not propose)
        entries.append(e)
        store.write(name, pre, entries)
    print(f"{'Proposed' if propose else 'Saved'} {e['id']}: {a.statement} (scope: {a.scope})")
    print(f"hash: {store.digest()}")


def cmd_approve(store, a):
    require(store)
    with store.locked(a.expect_hash):
        ipre, inbox = store.read(INBOX)
        i, e = find(inbox, a.id)
        if e is None:
            raise NotFound(f"{a.id} is not in the inbox")
        inbox.pop(i)
        e["fields"].update(Status="confirmed", Approved=today())
        rpre, reg = store.read(REGISTER)
        reg.append(e)
        store.write(REGISTER, rpre, reg)
        store.write(INBOX, ipre, inbox)
    print(f"Approved {a.id}: {e['fields'].get('Statement')}")


def cmd_reject(store, a):
    require(store)
    with store.locked(a.expect_hash):
        pre, inbox = store.read(INBOX)
        i, e = find(inbox, a.id)
        if e is None:
            raise NotFound(f"{a.id} is not in the inbox")
        inbox.pop(i)
        store.write(INBOX, pre, inbox)
    print(f"Rejected and removed {a.id}.")


def cmd_supersede(store, a):
    require(store)
    with store.locked(a.expect_hash):
        pre, reg = store.read(REGISTER)
        i, old = find(reg, a.id)
        if old is None:
            raise NotFound(f"{a.id} is not in the register")
        f = old["fields"]
        a.type = f.get("Type", a.id.split("-")[0])
        a.title = a.title or old["title"]
        a.scope = a.scope or f.get("Scope", "")
        check_content([a.title, a.statement, a.scope], a.sensitivity, a.health_approved)
        new = new_entry(store, a, "confirmed", approved=True)
        new["fields"]["Supersedes"] = old["id"]
        f.update({"Status": "superseded", "Superseded by": new["id"]})
        reg.append(new)
        store.write(REGISTER, pre, reg)
    print(f"{new['id']} replaces {a.id}: {a.statement}")


def cmd_decide(store, a):
    require(store)
    check_content([a.title, a.decision, a.context, a.rationale, a.consequences], a.sensitivity,
                  a.health_approved)
    with store.locked(a.expect_hash):
        pre, decs = store.read(DECISIONS)
        eid = store.next_id("UDEC")
        fields = {"Decision": a.decision, "Status": "confirmed", "Scope": a.scope, "Decided": today(),
                  "Decided by": "user", "Context": a.context or "not recorded",
                  "Rationale": a.rationale or "not recorded",
                  "Consequences": a.consequences or "not recorded",
                  "Reconsider when": a.reconsider or "the user asks", "Relates to": a.relates or "none",
                  "Supersedes": a.supersedes or "none", "Superseded by": "none"}
        if a.supersedes:
            _, old = find(decs, a.supersedes)
            if old is None:
                raise NotFound(f"{a.supersedes} is not in the decision log")
            old["fields"].update({"Status": "superseded", "Superseded by": eid})
        decs.append({"id": eid, "title": a.title, "fields": fields, "extra": []})
        store.write(DECISIONS, pre, decs)
    print(f"Recorded {eid}: {a.decision}")


def _links(e):
    out = set()
    for k in LINK_FIELDS:
        out |= set(re.findall(r"[A-Z]+-\d+", e["fields"].get(k, "")))
    return out


def cmd_forget(store, a):
    require(store)
    if not a.ids and not a.match:
        raise Refused("name the entries to forget (IDs) or use --match TEXT")
    with store.locked(a.expect_hash):
        files = {n: store.read(n) for n in (REGISTER, INBOX, DECISIONS)}
        everything = [e for n in files for e in files[n][1]]
        doomed = set(a.ids or [])
        if a.match:
            needle = a.match.lower()
            doomed |= {e["id"] for e in everything
                       if needle in (e["title"] + " " + " ".join(e["fields"].values())).lower()}
        # Follow supersession chains and decisions that relate to a deleted entry:
        # an earlier version of a deleted preference is the same personal data.
        changed = True
        while changed:
            changed = False
            for e in everything:
                linked = _links(e)
                if e["id"] in doomed:
                    # Only supersession links are followed outward from a doomed entry.
                    chain = {x for x in re.findall(r"[A-Z]+-\d+", e["fields"].get("Supersedes", "") +
                                                   " " + e["fields"].get("Superseded by", ""))
                             if x not in doomed}
                    if chain:
                        doomed |= chain
                        changed = True
                elif e["id"].startswith("UDEC-") and linked & doomed and \
                        not (set(re.findall(r"[A-Z]+-\d+", e["fields"].get("Relates to", ""))) - doomed):
                    doomed.add(e["id"])
                    changed = True
        missing = set(a.ids or []) - {e["id"] for e in everything}
        removed = []
        for name, (pre, entries) in files.items():
            keep = []
            for e in entries:
                if e["id"] in doomed:
                    removed.append(e["id"])
                    continue
                for k in LINK_FIELDS:
                    if k in e["fields"]:
                        v = e["fields"][k]
                        for d in doomed:
                            v = re.sub(rf"\b{re.escape(d)}\b", "deleted", v)
                        e["fields"][k] = v
                keep.append(e)
            if store.p(name).exists():
                store.write(name, pre, keep)
        cache = store.p(CACHE_DIR)
        cache_note = ""
        if cache.exists():
            for f in sorted(cache.rglob("*"), reverse=True):
                f.unlink() if f.is_file() else f.rmdir()
            cache.rmdir()
            cache_note = " Removed derived cache."
    if not removed:
        raise NotFound("Nothing matched; nothing deleted." + (f" Unknown IDs: {', '.join(sorted(missing))}" if missing else ""))
    print(f"Deleted: {', '.join(sorted(removed))}.{cache_note}")
    if missing:
        print(f"Not found: {', '.join(sorted(missing))}")
    print("Not covered: the host's conversation history or its own memory, backups, file-sync "
          "copies and anything previously exported. These are outside this tool's control.")


def cmd_reset(store, a):
    require(store)
    if not a.yes:
        raise Refused("reset deletes the whole register, inbox and decision log; repeat with --yes "
                      "after the user confirms")
    with store.locked(a.expect_hash):
        for name in (REGISTER, INBOX, DECISIONS, STATE):
            if store.p(name).exists():
                store.p(name).unlink()
        cache = store.p(CACHE_DIR)
        if cache.exists():
            for f in sorted(cache.rglob("*"), reverse=True):
                f.unlink() if f.is_file() else f.rmdir()
            cache.rmdir()
    print(f"Deleted the MPoT files in {store.dir} (the folder itself was left in place). "
          "Host history, backups and exported copies are outside this tool's control.")


def cmd_export(store, a):
    require(store)
    data = {"exported": today(), "store": str(store.dir)}
    for name in (REGISTER, INBOX, DECISIONS):
        data[name] = [{"id": e["id"], "title": e["title"], **e["fields"]} for e in store.read(name)[1]]
    Path(a.out).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Exported to {a.out}. That copy is now outside MPoT: deleting entries later will not "
          "delete it.")


def cmd_import(store, a):
    text = Path(a.file).read_text(encoding="utf-8")
    _, entries = parse(text)
    flagged, clean = [], []
    for e in entries:
        blob = e["title"] + " " + " ".join(e["fields"].values()) + " " + " ".join(e["extra"])
        reasons = []
        if INJECTION_RE.search(blob):
            reasons.append("contains instructions or actions, not a preference")
        if CRISIS_RE.search(blob) or SECRET_RE.search(blob):
            reasons.append("crisis information or secrets")
        elif HEALTH_RE.search(blob):
            reasons.append("health information")
        (flagged if reasons else clean).append((e, reasons))
    for e, _ in clean:
        print(f"candidate {e['id']}: {e['fields'].get('Statement') or e['title']}")
    for e, reasons in flagged:
        print(f"FLAGGED {e['id']}: {'; '.join(reasons)} — not imported")
    if not a.to_inbox:
        print("Nothing written. Imported entries are untrusted; show them to the user, then use "
              "--to-inbox to add the candidates as proposals.")
        return
    require(store)
    with store.locked(a.expect_hash):
        pre, inbox = store.read(INBOX)
        for e, _ in clean:
            f = e["fields"]
            typ = f.get("Type", e["id"].split("-")[0])
            if typ not in TYPES:
                continue
            ns = argparse.Namespace(type=typ, title=e["title"], statement=f.get("Statement", e["title"]),
                                    scope=f.get("Scope", "unspecified"),
                                    source=f"imported from {Path(a.file).name} on {today()}",
                                    review=None, sensitivity="low")
            inbox.append(new_entry(store, ns, "proposed", approved=False))
        store.write(INBOX, pre, inbox)
    print(f"Added {len(clean)} proposals to the inbox; none are confirmed until approved.")


def cmd_hash(store, a):
    require(store)
    print(store.digest())


# -------------------------------------------------------------------- main

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--store", default=os.environ.get("MPOT_STORE"),
                    help="private folder the user chose (or MPOT_STORE)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def entry_args(p, need_type=True):
        if need_type:
            p.add_argument("--type", required=True, choices=TYPES)
            p.add_argument("--title", required=True)
            p.add_argument("--scope", required=True)
        p.add_argument("--statement", required=True)
        p.add_argument("--source")
        p.add_argument("--review")
        p.add_argument("--sensitivity", default="low", choices=["low", "personal", "health"])
        p.add_argument("--health-approved", action="store_true")

    def write_args(p):
        p.add_argument("--expect-hash", help="hash from your last read; refuse if the store changed")

    sub.add_parser("init")
    v = sub.add_parser("view")
    v.add_argument("--scope")
    v.add_argument("--history", action="store_true", help="include superseded and expired entries")
    p = sub.add_parser("add")
    entry_args(p)
    p.add_argument("--status", default="confirmed", choices=["confirmed", "provisional"])
    write_args(p)
    p = sub.add_parser("propose")
    entry_args(p)
    write_args(p)
    for name in ("approve", "reject"):
        p = sub.add_parser(name)
        p.add_argument("id")
        write_args(p)
    p = sub.add_parser("supersede")
    p.add_argument("id")
    entry_args(p, need_type=False)
    p.add_argument("--title")
    p.add_argument("--scope")
    write_args(p)
    p = sub.add_parser("decide")
    for f in ("title", "decision", "scope"):
        p.add_argument(f"--{f}", required=True)
    for f in ("context", "rationale", "consequences", "reconsider", "relates", "supersedes"):
        p.add_argument(f"--{f}")
    p.add_argument("--sensitivity", default="low", choices=["low", "personal", "health"])
    p.add_argument("--health-approved", action="store_true")
    write_args(p)
    p = sub.add_parser("forget")
    p.add_argument("ids", nargs="*")
    p.add_argument("--match")
    write_args(p)
    p = sub.add_parser("reset")
    p.add_argument("--yes", action="store_true")
    write_args(p)
    p = sub.add_parser("export")
    p.add_argument("out")
    p = sub.add_parser("import")
    p.add_argument("file")
    p.add_argument("--to-inbox", action="store_true")
    write_args(p)
    sub.add_parser("hash")

    a = ap.parse_args(argv)
    if not a.store:
        print("No store chosen. Memory stays session-only until the user picks a private folder "
              "(--store DIR or MPOT_STORE).", file=sys.stderr)
        return 1
    store = Store(a.store)
    cmds = {"init": cmd_init, "view": cmd_view, "add": cmd_add,
            "propose": lambda s, x: cmd_add(s, x, propose=True), "approve": cmd_approve,
            "reject": cmd_reject, "supersede": cmd_supersede, "decide": cmd_decide,
            "forget": cmd_forget, "reset": cmd_reset, "export": cmd_export, "import": cmd_import,
            "hash": cmd_hash}
    try:
        if a.cmd not in ("init", "import"):
            check_location(store.dir)
        cmds[a.cmd](store, a)
        return 0
    except (Refused, Conflict, NotFound) as e:
        print(f"{type(e).__name__.lower()}: {e}", file=sys.stderr)
        return e.code


if __name__ == "__main__":
    sys.exit(main())
