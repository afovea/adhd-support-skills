"""Packaging and installer tests. Every test builds into a temporary folder and
installs into temporary projects and a temporary HOME — nothing real is touched."""
import contextlib
import importlib.util
import io
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
import sys  # noqa: E402

sys.path.insert(0, str(ROOT / "scripts"))
import build  # noqa: E402
import validate  # noqa: E402

TMP = tempfile.TemporaryDirectory()
DIST = Path(TMP.name) / "dist"
build.dist(DIST)


def load_installer():
    spec = importlib.util.spec_from_file_location("installer", DIST / "install.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


installer = load_installer()


def install(*args):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = installer.main(list(args))
    return code, out.getvalue()


def snapshot(folder):
    return {p.relative_to(folder).as_posix(): p.read_bytes() for p in folder.rglob("*") if p.is_file()}


class BundleTests(unittest.TestCase):
    def test_bundles_pass_structural_checks(self):
        self.assertEqual(validate.check_dist(DIST), [])

    def test_build_is_reproducible(self):
        again = Path(TMP.name) / "dist2"
        build.dist(again)
        self.assertEqual(json.loads((DIST / "MANIFEST.json").read_text()),
                         json.loads((again / "MANIFEST.json").read_text()))

    def test_every_skill_is_self_contained_after_extraction(self):
        with tempfile.TemporaryDirectory() as clean:
            for z in sorted((DIST / "zips").glob("*.zip")):
                shutil.unpack_archive(str(z), clean)
            for d in Path(clean).iterdir():
                for f in ("SKILL.md", "references/shared/safety-policy.md", "references/shared/crisis-resources.md",
                          "references/shared/runtime-evidence.md", "references/evidence-card.md"):
                    self.assertTrue((d / f).exists(), f"{d.name} missing {f}")
                self.assertEqual(validate.check_skill(d, materialised=True, max_desc=200), [])

    def test_manifest_lists_every_skill_and_file(self):
        m = json.loads((DIST / "MANIFEST.json").read_text())
        self.assertEqual(len(m["skills"]), 13)
        for rel in m["files"]:
            self.assertTrue((DIST / rel).exists())

    def test_host_manifests_present(self):
        self.assertTrue((DIST / "claude-code/.claude-plugin/plugin.json").exists())
        self.assertTrue((DIST / "claude-code/.claude-plugin/marketplace.json").exists())
        self.assertTrue((DIST / "codex/plugin.json").exists())
        self.assertTrue((DIST / "codex/.agents/plugins/marketplace.json").exists())

    def test_no_explicit_only_invocation(self):
        for p in DIST.rglob("*"):
            if p.is_file() and p.suffix in (".md", ".yaml", ".json"):
                t = p.read_text()
                self.assertNotIn("disable-model-invocation", t, p)
                self.assertNotIn("allow_implicit_invocation", t, p)


class CompactInstructionsTests(unittest.TestCase):
    def setUp(self):
        self.text = (DIST / "generic/ADHD-support-instructions-compact.md").read_text()

    def test_compact_fits_and_keeps_safeguards(self):
        self.assertLessEqual(len(self.text), build.COMPACT_LIMIT)
        self.assertEqual(validate.check_compact(self.text), [])

    def test_check_catches_dropped_safeguard(self):
        broken = self.text.replace("never invent a number", "")
        self.assertTrue(any("never invent a number" in p for p in validate.check_compact(broken)))

    def test_check_catches_localised_support_info(self):
        for local in ("call 988", "ring Samaritans", "dial 0800 1111", "see findahelpline.com"):
            broken = self.text.replace("a doctor or urgent care service", f"a doctor or urgent care service, or {local}")
            self.assertTrue(any("localised" in p for p in validate.check_compact(broken)), local)

    def test_no_bundle_text_contains_localised_support_info(self):
        for p in DIST.rglob("*.md"):
            self.assertIsNone(validate.LOCAL_SUPPORT_RE.search(p.read_text()), p)

    def test_check_catches_oversize_and_edited_core_block(self):
        self.assertTrue(validate.check_compact(self.text + "x" * build.COMPACT_LIMIT))
        edited = self.text.replace("Controls come first.", "Controls matter.")
        self.assertTrue(any("core-boundaries" in p for p in validate.check_compact(edited)))


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.project = self.base / "project"
        self.project.mkdir()
        (self.project / "CLAUDE.md").write_text("# My project\n\nKeep this line.\n")
        self.home = self.base / "home"
        self.home.mkdir()
        self.old_home = os.environ.get("HOME")
        os.environ["HOME"] = str(self.home)
        # A private MPoT folder the installer must never touch.
        self.mpot = self.home / "private-mpot"
        self.mpot.mkdir()
        (self.mpot / "MPoT.md").write_text("private")

    def tearDown(self):
        if self.old_home is not None:
            os.environ["HOME"] = self.old_home
        self.tmp.cleanup()

    def skills(self, layout=".claude/skills"):
        return sorted(p.parent.name for p in (self.project / layout).glob("*/SKILL.md"))

    def test_dry_run_changes_nothing(self):
        before = snapshot(self.project)
        code, out = install("--host", "claude-code", "--project", str(self.project), "--dry-run")
        self.assertEqual(code, 0)
        self.assertIn("DRY RUN", out)
        self.assertEqual(snapshot(self.project), before)

    def test_project_install_preserves_instructions_and_is_idempotent(self):
        install("--host", "claude-code", "--project", str(self.project))
        self.assertEqual(len(self.skills()), 13)
        text = (self.project / "CLAUDE.md").read_text()
        self.assertTrue(text.startswith("# My project\n\nKeep this line.\n"))
        self.assertEqual(text.count(installer.START), 1)
        code, out = install("--host", "claude-code", "--project", str(self.project))
        self.assertIn("already up to date", out)
        self.assertEqual((self.project / "CLAUDE.md").read_text(), text)

    def test_update_keeps_user_edits_and_reports_them(self):
        install("--host", "claude-code", "--project", str(self.project))
        edited = self.project / ".claude/skills/adhd-start/SKILL.md"
        edited.write_text(edited.read_text() + "\nmy note\n")
        code, out = install("--host", "claude-code", "--project", str(self.project))
        self.assertIn("edited after install", out)
        self.assertIn("my note", edited.read_text())
        code, out = install("--host", "claude-code", "--project", str(self.project), "--force")
        self.assertNotIn("my note", edited.read_text())

    def test_foreign_skill_with_same_name_is_not_overwritten(self):
        foreign = self.project / ".claude/skills/adhd-start"
        foreign.mkdir(parents=True)
        (foreign / "SKILL.md").write_text("someone else's skill")
        code, out = install("--host", "claude-code", "--project", str(self.project))
        self.assertIn("was not installed by this tool", out)
        self.assertEqual((foreign / "SKILL.md").read_text(), "someone else's skill")

    def test_uninstall_removes_only_owned_files_and_block(self):
        other = self.project / ".claude/skills/my-own-skill/SKILL.md"
        other.parent.mkdir(parents=True)
        other.write_text("mine")
        install("--host", "claude-code", "--project", str(self.project))
        kept = self.project / ".claude/skills/adhd-time/SKILL.md"
        kept.write_text("edited by me")
        code, out = install("--host", "claude-code", "--project", str(self.project), "--uninstall")
        self.assertEqual(self.skills(), ["adhd-time", "my-own-skill"])
        self.assertEqual(kept.read_text(), "edited by me")
        self.assertEqual((self.project / "CLAUDE.md").read_text(), "# My project\n\nKeep this line.\n")
        self.assertEqual((self.mpot / "MPoT.md").read_text(), "private")

    def test_codex_layout(self):
        install("--host", "codex", "--project", str(self.project))
        self.assertEqual(len(self.skills(".agents/skills")), 13)
        self.assertIn(installer.START, (self.project / "AGENTS.md").read_text())
        self.assertFalse((self.project / ".claude/skills").exists())

    def test_router_only_installs_no_skills(self):
        install("--host", "codex", "--project", str(self.project), "--router-only")
        self.assertFalse((self.project / ".agents").exists())
        self.assertIn("adhd-start", (self.project / "AGENTS.md").read_text())

    def test_personal_install_leaves_global_instructions_alone(self):
        install("--host", "claude-code", "--personal")
        self.assertEqual(len(list((self.home / ".claude/skills").glob("*/SKILL.md"))), 13)
        self.assertFalse((self.home / ".claude/CLAUDE.md").exists())

    def test_generic_host_inserts_block_into_chosen_file(self):
        f = self.base / "instructions.md"
        f.write_text("existing text\n")
        install("--host", "generic", "--instructions", str(f))
        t = f.read_text()
        self.assertTrue(t.startswith("existing text\n"))
        install("--host", "generic", "--instructions", str(f), "--uninstall")
        self.assertEqual(f.read_text(), "existing text\n")

    def test_refuses_source_repo_and_missing_folder(self):
        with self.assertRaises(SystemExit):
            install("--host", "claude-code", "--project", str(ROOT))
        with self.assertRaises(SystemExit):
            install("--host", "claude-code", "--project", str(self.base / "nope"))
        with self.assertRaises(SystemExit):
            install("--host", "claude-code")  # no target given

    def test_verify_reports_state(self):
        install("--host", "claude-code", "--project", str(self.project))
        code, out = install("--host", "claude-code", "--project", str(self.project), "--verify")
        self.assertIn("skills: 13/13", out)
        self.assertIn("router block: present", out)


if __name__ == "__main__":
    unittest.main()
