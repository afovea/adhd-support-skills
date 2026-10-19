#!/usr/bin/env python3
"""Write a valid calendar file (.ics) for one event or reminder. Standard library only.

    python3 make_ics.py --title "Call GP surgery" --date 2026-10-20 --time 08:00 \
        [--minutes 15] [--alarm 10] [--tz Europe/London] [--repeat daily|weekly|weekdays] \
        [--notes "..."] [--out call-gp.ics]

Without --tz the time is "floating": the same wall-clock time wherever the
device is. With --tz it is fixed to that zone and written in UTC; times that
don't exist or happen twice on a daylight-saving change are refused so the
user can choose. Without --out the file is printed. Nothing is sent anywhere.
Exit codes: 0 ok, 2 needs a decision from the user.
"""
import argparse
import datetime as dt
import hashlib
import sys

REPEAT = {"daily": "FREQ=DAILY", "weekly": "FREQ=WEEKLY",
          "weekdays": "FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR"}


class NeedsDecision(Exception):
    pass


def escape(text):
    return (text.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,")
            .replace("\r\n", "\\n").replace("\n", "\\n"))


def fold(line):
    """Fold to 75 octets per RFC 5545, never splitting a UTF-8 character."""
    out, cur = [], b""
    for ch in line:
        b = ch.encode("utf-8")
        if len(cur) + len(b) > (75 if not out else 74):
            out.append(cur)
            cur = b""
        cur += b
    out.append(cur)
    return "\r\n ".join(part.decode("utf-8") for part in out)


def resolve(date, hhmm, zone):
    """Aware datetime in `zone`, refusing DST gaps and repeated times."""
    from zoneinfo import ZoneInfo
    tz = ZoneInfo(zone)
    naive = dt.datetime.combine(date, dt.time.fromisoformat(hhmm))
    first, second = naive.replace(tzinfo=tz, fold=0), naive.replace(tzinfo=tz, fold=1)
    if first.astimezone(dt.timezone.utc).astimezone(tz).replace(tzinfo=None) != naive:
        raise NeedsDecision(f"{hhmm} doesn't exist on {date} in {zone} (the clocks go forward). Pick another time.")
    if first.utcoffset() != second.utcoffset():
        raise NeedsDecision(f"{hhmm} happens twice on {date} in {zone} (the clocks go back). Which one?")
    return first


def build(title, date, hhmm, minutes=15, alarm=None, zone=None, repeat=None, notes=None, now=None):
    now = now or dt.datetime.now(dt.timezone.utc)
    start_naive = dt.datetime.combine(date, dt.time.fromisoformat(hhmm))
    if zone:
        start = resolve(date, hhmm, zone).astimezone(dt.timezone.utc)
        fmt = lambda d: d.strftime("%Y%m%dT%H%M%SZ")  # noqa: E731
    else:
        start = start_naive
        fmt = lambda d: d.strftime("%Y%m%dT%H%M%S")  # noqa: E731
    end = start + dt.timedelta(minutes=minutes)
    uid = hashlib.sha256(f"{title}|{date}|{hhmm}|{zone}".encode()).hexdigest()[:16] + "@adhd-support-skills"
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//ADHD Support Skills//EN", "CALSCALE:GREGORIAN",
             "BEGIN:VEVENT", f"UID:{uid}", f"DTSTAMP:{now.strftime('%Y%m%dT%H%M%SZ')}",
             f"DTSTART:{fmt(start)}", f"DTEND:{fmt(end)}", f"SUMMARY:{escape(title)}"]
    if notes:
        lines.append(f"DESCRIPTION:{escape(notes)}")
    if repeat:
        lines.append(f"RRULE:{REPEAT[repeat]}")
    if alarm is not None:
        lines += ["BEGIN:VALARM", "ACTION:DISPLAY", f"DESCRIPTION:{escape(title)}",
                  f"TRIGGER:-PT{int(alarm)}M", "END:VALARM"]
    lines += ["END:VEVENT", "END:VCALENDAR"]
    return "\r\n".join(fold(l) for l in lines) + "\r\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--title", required=True)
    ap.add_argument("--date", required=True, type=dt.date.fromisoformat, help="YYYY-MM-DD")
    ap.add_argument("--time", required=True, help="HH:MM, 24-hour, local wall-clock")
    ap.add_argument("--minutes", type=int, default=15)
    ap.add_argument("--alarm", type=int, help="minutes before to alert")
    ap.add_argument("--tz", help="IANA zone, e.g. Europe/London; omit for floating time")
    ap.add_argument("--repeat", choices=sorted(REPEAT))
    ap.add_argument("--notes")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    try:
        text = build(a.title, a.date, a.time, a.minutes, a.alarm, a.tz, a.repeat, a.notes)
    except NeedsDecision as e:
        print(f"needs a decision: {e}", file=sys.stderr)
        return 2
    if a.out:
        with open(a.out, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        print(f"Wrote {a.out}. Open it to add the event to your calendar; nothing has been added yet.")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
