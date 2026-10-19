"""Deterministic mocked-tool harness for reminders, retries, cancellation and time resolution.

No real notifications are sent. Every tool outcome is scripted.
"""
import datetime as dt
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import capability_ops as ops  # noqa: E402


class MockHost:
    """Scripted reminder tool. `script` is a list of outcomes for successive create() calls:
    'ok', 'transient', 'ambiguous-created', 'ambiguous-missing'."""

    def __init__(self, script=(), can_list=True, cancel_fails=()):
        self.script, self.can_list = list(script), can_list
        self.items, self.calls, self.cancel_fails = {}, [], set(cancel_fails)

    def create(self, key, when, text):
        self.calls.append(("create", key))
        outcome = self.script.pop(0) if self.script else "ok"
        if outcome == "ok":
            self.items[key] = (when, text)
        elif outcome == "transient":
            raise ops.Transient()
        elif outcome == "ambiguous-created":
            self.items[key] = (when, text)
            raise ops.Ambiguous()
        elif outcome == "ambiguous-missing":
            raise ops.Ambiguous()

    def find(self, key):
        self.calls.append(("find", key))
        return key in self.items

    def cancel(self, item):
        self.calls.append(("cancel", item))
        if item in self.cancel_fails:
            raise RuntimeError("cancel failed")
        self.items.pop(item, None)


WHEN = ops.resolve_local(dt.date(2026, 11, 3), "17:30", "Europe/London")


class ReminderTests(unittest.TestCase):
    def test_success_is_reported_only_after_tool_confirms(self):
        host = MockHost(["ok"])
        out = ops.create_reminder(host, "k1", WHEN, "Put the parcel by the door")
        self.assertEqual(out.status, "created")
        self.assertIn("k1", host.items)

    def test_failure_returns_copyable_details_not_success(self):
        host = MockHost(["transient", "transient"])
        out = ops.create_reminder(host, "k1", WHEN, "Put the parcel by the door")
        self.assertEqual(out.status, "failed")
        self.assertIn("parcel", out.copyable)
        self.assertNotIn("created", out.message.split(".")[0].lower().replace("wasn't created", ""))
        self.assertEqual(out.attempts, 2)  # bounded: one retry only

    def test_ambiguous_but_created_is_checked_not_duplicated(self):
        host = MockHost(["ambiguous-created"])
        out = ops.create_reminder(host, "k1", WHEN, "Call GP")
        self.assertEqual(out.status, "exists")
        self.assertEqual([c for c in host.calls if c[0] == "create"], [("create", "k1")])
        self.assertEqual(len(host.items), 1)

    def test_ambiguous_and_missing_retries_once_with_same_key(self):
        host = MockHost(["ambiguous-missing", "ok"])
        out = ops.create_reminder(host, "k1", WHEN, "Call GP")
        self.assertEqual(out.status, "created")
        self.assertEqual(host.calls, [("create", "k1"), ("find", "k1"), ("create", "k1")])

    def test_ambiguous_without_state_check_does_not_retry(self):
        host = MockHost(["ambiguous-created"], can_list=False)
        out = ops.create_reminder(host, "k1", WHEN, "Call GP")
        self.assertEqual(out.status, "unknown")
        self.assertEqual(len([c for c in host.calls if c[0] == "create"]), 1)
        self.assertIn("Call GP", out.copyable)


class CancellationTests(unittest.TestCase):
    def test_quiet_cancels_only_suite_created_checkpoints(self):
        host = MockHost()
        host.items = {"suite-checkin": None, "users-own-dentist-reminder": None}
        session = ops.Session(owned=["suite-checkin"])
        cancelled, failed = ops.cancel_owned(host, session)
        self.assertEqual(cancelled, ["suite-checkin"])
        self.assertIn("users-own-dentist-reminder", host.items)
        self.assertEqual(ops.cancel_message(cancelled, failed), "Cancelled the check-in I'd set.")

    def test_cancellation_failure_is_reported_honestly(self):
        host = MockHost(cancel_fails={"suite-checkin"})
        session = ops.Session(owned=["suite-checkin"])
        cancelled, failed = ops.cancel_owned(host, session)
        self.assertEqual(failed, ["suite-checkin"])
        self.assertIn("couldn't cancel", ops.cancel_message(cancelled, failed))


class TimeResolutionTests(unittest.TestCase):
    def test_vague_time_needs_clarification_before_write(self):
        with self.assertRaises(ops.NeedsClarification):
            ops.check_specific("tomorrow morning")
        ops.check_specific("tomorrow at 08:00")  # specific enough

    def test_wall_clock_time_survives_dst_change(self):
        before = ops.resolve_local(dt.date(2026, 10, 24), "09:00", "Europe/London")
        after = ops.resolve_local(dt.date(2026, 10, 26), "09:00", "Europe/London")
        self.assertEqual((before.hour, after.hour), (9, 9))
        self.assertEqual(before.utcoffset(), dt.timedelta(hours=1))
        self.assertEqual(after.utcoffset(), dt.timedelta(0))

    def test_repeated_hour_on_fall_back_is_surfaced(self):
        with self.assertRaises(ops.NeedsClarification) as e:
            ops.resolve_local(dt.date(2026, 10, 25), "01:30", "Europe/London")
        self.assertIn("twice", str(e.exception))

    def test_missing_hour_on_spring_forward_is_surfaced(self):
        with self.assertRaises(ops.NeedsClarification) as e:
            ops.resolve_local(dt.date(2027, 3, 28), "01:30", "Europe/London")
        self.assertIn("does not exist", str(e.exception))

    def test_travel_zone_changes_instant_not_wall_clock(self):
        london = ops.resolve_local(dt.date(2026, 11, 3), "08:00", "Europe/London")
        new_york = ops.resolve_local(dt.date(2026, 11, 3), "08:00", "America/New_York")
        self.assertEqual(new_york - london, dt.timedelta(hours=5))


if __name__ == "__main__":
    unittest.main()
