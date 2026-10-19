"""Evaluation tooling: frozen rubrics, independence tracking and the human grading round trip."""
import argparse
import contextlib
import csv
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import evals  # noqa: E402

CASES = {c["id"]: c for c in evals.load_cases()}
TRANSCRIPT = {"SAF-01": {"host": "test", "host_model": "claude-sonnet-4-6", "route_observed": "adhd-start",
                         "turns": [{"user": "…", "assistant": "Please contact your local emergency services now."}]}}


def run(fn, **kw):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        fn(argparse.Namespace(**kw))
    return out.getvalue()


class EvalToolingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        (self.dir / "t.json").write_text(json.dumps(TRANSCRIPT))

    def tearDown(self):
        self.tmp.cleanup()

    def score(self, grades):
        (self.dir / "g.json").write_text(json.dumps(grades))
        run(evals.cmd_score, transcripts=str(self.dir / "t.json"), grades=[str(self.dir / "g.json")],
            out=str(self.dir / "r.json"))
        return json.loads((self.dir / "r.json").read_text())

    def test_rubric_hash_changes_when_expectations_change(self):
        case = dict(CASES["SAF-01"])
        before = evals.rubric_hash(case)
        case["expected"] = case["expected"] + ["something new"]
        self.assertNotEqual(before, evals.rubric_hash(case))

    def test_grade_against_old_rubric_is_stale_not_pass(self):
        r = self.score({"SAF-01": {"pass": True, "grader": "human:AB", "rubric_hash": "000000000000"}})
        self.assertEqual(r["results"]["SAF-01"]["status"], "stale rubric")
        self.assertEqual(r["summary"]["pass"], 0)
        self.assertIn("SAF-01", r["summary"]["stale_rubric"])

    def test_self_grade_is_not_independent_but_human_is(self):
        h = evals.rubric_hash(CASES["SAF-01"])
        self_r = self.score({"SAF-01": {"pass": True, "grader": "model:claude/opus", "rubric_hash": h}})
        self.assertFalse(self_r["results"]["SAF-01"]["independent"])
        self.assertEqual(self_r["summary"]["self_graded"], 1)
        human_r = self.score({"SAF-01": {"pass": True, "grader": "human:AB", "rubric_hash": h}})
        self.assertTrue(human_r["results"]["SAF-01"]["independent"])
        self.assertEqual(human_r["summary"]["pass"], 1)

    def test_other_model_family_counts_as_independent(self):
        self.assertTrue(evals.is_independent({"grader": "model:gpt/5"}, {"host_model": "claude-sonnet-4-6"}))
        self.assertFalse(evals.is_independent({"grader": "model:gpt/5"}, {}))  # host unknown

    def test_unrecorded_host_model_is_flagged(self):
        TRANSCRIPT_NO_MODEL = {"SAF-01": {**TRANSCRIPT["SAF-01"], "host_model": None}}
        (self.dir / "t.json").write_text(json.dumps(TRANSCRIPT_NO_MODEL))
        r = self.score({})
        self.assertIn("SAF-01", r["summary"]["host_model_unrecorded"])

    def test_human_pack_round_trip(self):
        run(evals.cmd_human_pack, transcripts=str(self.dir / "t.json"), suite=["safety"], out=str(self.dir / "pack"))
        md = (self.dir / "pack/human-grading.md").read_text()
        self.assertIn("SAF-01", md)
        self.assertIn("Forbidden", md)
        with open(self.dir / "pack/human-grades.csv", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(rows[0]["case_id"], "SAF-01")
        rows[0].update(grader="AB", **{"pass": "yes", "severe": "no", "violations": ""})
        with open(self.dir / "done.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        run(evals.cmd_import_human, csv=str(self.dir / "done.csv"), out=str(self.dir / "g.json"))
        g = json.loads((self.dir / "g.json").read_text())["SAF-01"]
        self.assertEqual(g["grader"], "human:AB")
        self.assertEqual(g["rubric_hash"], evals.rubric_hash(CASES["SAF-01"]))
        r = self.score(json.loads((self.dir / "g.json").read_text()))
        self.assertEqual(r["results"]["SAF-01"]["status"], "pass")
        self.assertTrue(r["results"]["SAF-01"]["independent"])


if __name__ == "__main__":
    unittest.main()
