"""Reference procedures for the permission policy's external-action rules.

Host adapters that give the suite real reminder or check-in tools can reuse
these. They are deliberately small and tool-agnostic: a host object supplies
`create(key, when, text)`, `find(key)`, `cancel(item_id)` and optionally
`can_list`. Standard library only (Python 3.9+ for zoneinfo).

Rules implemented (shared/permission-policy.md):
- vague times are clarified before any write;
- local wall-clock times are resolved in a named zone, and DST gaps/overlaps
  are surfaced rather than guessed;
- an ambiguous write is checked before any retry, retries are bounded, and the
  same idempotency key is reused so no duplicate is created;
- failures return copyable text instead of a success claim;
- cancellation touches only items the suite itself created.
"""
import datetime as dt
from dataclasses import dataclass, field
from zoneinfo import ZoneInfo


class Transient(Exception):
    """The tool failed in a way that is safe to retry (nothing was created)."""


class Ambiguous(Exception):
    """The tool may or may not have acted (timeout, lost response)."""


class NeedsClarification(Exception):
    pass


VAGUE = ("morning", "afternoon", "evening", "tonight", "later", "soon", "sometime", "first thing")


def check_specific(time_text):
    """Raise if the user's time words need a question before an external write."""
    words = time_text.lower()
    for v in VAGUE:
        if v in words:
            raise NeedsClarification(f'"{time_text}" is not a specific time. Ask once, e.g. "What time — 8:00?"')


def resolve_local(date, hhmm, zone):
    """Return an aware datetime for a wall-clock time in `zone`, refusing DST gaps and overlaps."""
    tz = ZoneInfo(zone)
    naive = dt.datetime.combine(date, dt.time.fromisoformat(hhmm))
    first, second = naive.replace(tzinfo=tz, fold=0), naive.replace(tzinfo=tz, fold=1)
    # Gap first: in a spring-forward gap both folds also differ, so order matters.
    roundtrip = first.astimezone(dt.timezone.utc).astimezone(tz)
    if roundtrip.replace(tzinfo=None) != naive:
        raise NeedsClarification(f"{hhmm} does not exist on {date} in {zone} (clocks go forward). "
                                 f"Use {roundtrip.strftime('%H:%M')} or another time?")
    if first.utcoffset() != second.utcoffset():
        raise NeedsClarification(f"{hhmm} happens twice on {date} in {zone} (clocks go back). Which one?")
    return first


@dataclass
class Outcome:
    status: str          # created | exists | failed | unknown
    message: str
    copyable: str = ""
    attempts: int = 0


def create_reminder(host, key, when, text, max_retries=1):
    copy = f"{when.strftime('%a %d %b %Y %H:%M %Z')} — {text}"
    attempts = 0
    while True:
        attempts += 1
        try:
            host.create(key, when, text)
            return Outcome("created", "Reminder created.", attempts=attempts)
        except Ambiguous:
            if not getattr(host, "can_list", True):
                return Outcome("unknown", "The reminder tool didn't confirm, and I can't check whether "
                               "it was created. Check your reminders before adding it again.", copy, attempts)
            if host.find(key):
                return Outcome("exists", "Reminder created (confirmed after an unclear response).",
                               attempts=attempts)
        except Transient:
            pass
        if attempts > max_retries:
            return Outcome("failed", "The reminder wasn't created. Here's the text to add yourself.",
                           copy, attempts)


@dataclass
class Session:
    """Items this suite created in the current session, by ID."""
    owned: list = field(default_factory=list)


def cancel_owned(host, session):
    """Cancel only suite-created items. Returns (cancelled, failed) ID lists."""
    cancelled, failed = [], []
    for item in list(session.owned):
        try:
            host.cancel(item)
            cancelled.append(item)
            session.owned.remove(item)
        except Exception:
            failed.append(item)
    return cancelled, failed


def cancel_message(cancelled, failed):
    if failed:
        return f"I couldn't cancel {len(failed)} check-in(s) I'd set — you may still get them."
    if cancelled:
        return "Cancelled the check-in I'd set."
    return ""
