"""Calendar-file (.ics) maker: valid structure, time zones, DST refusals, escaping, folding."""
import contextlib
import datetime as dt
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("make_ics", ROOT / "skills/adhd-connect/scripts/make_ics.py")
ics = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ics)
NOW = dt.datetime(2026, 10, 19, 12, 0, tzinfo=dt.timezone.utc)


def lines(text):
    assert text.endswith("\r\n")
    return text.split("\r\n")[:-1]


class MakeIcsTests(unittest.TestCase):
    def test_floating_time_event_with_alarm(self):
        out = ics.build("Call GP surgery", dt.date(2026, 10, 20), "08:00", 15, alarm=10, now=NOW)
        ls = lines(out)
        self.assertEqual(ls[0], "BEGIN:VCALENDAR")
        self.assertEqual(ls[-1], "END:VCALENDAR")
        self.assertIn("DTSTART:20261020T080000", ls)
        self.assertIn("DTEND:20261020T081500", ls)
        self.assertIn("TRIGGER:-PT10M", ls)
        self.assertIn("DTSTAMP:20261019T120000Z", ls)
        for block in ("VCALENDAR", "VEVENT", "VALARM"):
            self.assertEqual(ls.count(f"BEGIN:{block}"), ls.count(f"END:{block}"))

    def test_fixed_zone_written_in_utc_across_dst(self):
        before = ics.build("Bank", dt.date(2026, 10, 24), "09:00", zone="Europe/London", now=NOW)
        after = ics.build("Bank", dt.date(2026, 10, 26), "09:00", zone="Europe/London", now=NOW)
        self.assertIn("DTSTART:20261024T080000Z", before)  # BST, UTC+1
        self.assertIn("DTSTART:20261026T090000Z", after)   # GMT, UTC+0

    def test_refuses_repeated_and_missing_times(self):
        with self.assertRaises(ics.NeedsDecision):
            ics.build("Car", dt.date(2026, 10, 25), "01:30", zone="Europe/London")
        with self.assertRaises(ics.NeedsDecision):
            ics.build("Car", dt.date(2027, 3, 28), "01:30", zone="Europe/London")
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = ics.main(["--title", "Car", "--date", "2026-10-25", "--time", "01:30", "--tz", "Europe/London"])
        self.assertEqual(code, 2)
        self.assertIn("twice", err.getvalue())

    def test_escaping_and_folding(self):
        title = "Pay rent, council tax; and check\\notes " + "very long words " * 8
        out = ics.build(title, dt.date(2026, 10, 20), "08:00", notes="line one\nline two", now=NOW)
        self.assertIn("rent\\, council tax\\; and check\\\\notes", out.replace("\r\n ", ""))
        self.assertIn("DESCRIPTION:line one\\nline two", out)
        for physical in out.split("\r\n"):
            self.assertLessEqual(len(physical.encode("utf-8")), 75)

    def test_repeat_only_when_asked(self):
        self.assertNotIn("RRULE", ics.build("Plan", dt.date(2026, 10, 20), "08:00", now=NOW))
        self.assertIn("RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR",
                      ics.build("Plan", dt.date(2026, 10, 20), "08:00", repeat="weekdays", now=NOW))

    def test_writes_file_and_says_nothing_added(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "gp.ics"
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = ics.main(["--title", "Call GP", "--date", "2026-10-20", "--time", "08:00", "--out", str(path)])
            self.assertEqual(code, 0)
            self.assertIn("nothing has been added yet", out.getvalue())
            self.assertTrue(path.read_bytes().startswith(b"BEGIN:VCALENDAR\r\n"))


if __name__ == "__main__":
    unittest.main()
