# Handoff formats — getting things into other apps without a connection

Use these when no connected tool exists (`integration-policy.md`). Only confirmed details go in. Leave a field out rather than guess. Offer a discreet wording for anything sensitive, because notifications and shared calendars can be seen by other people.

## Calendar event or timed reminder (`.ics`)

Google, Apple, Outlook and most calendar apps can import an `.ics` file. Opening the file usually offers to add the event.

**Easiest:** if a shell or code execution is available and the `adhd-connect` skill is installed, run its `scripts/make_ics.py`. It handles line endings, escaping, time zones and daylight-saving checks:

```bash
python3 scripts/make_ics.py --title "Call GP surgery" --date 2026-10-20 --time 08:00 --minutes 15 --alarm 10 --out call-gp.ics
```

**By hand**, use this exact shape. Each line ends with CRLF. Escape `\`, `;` and `,` in text as `\\`, `\;` and `\,`. Write newlines in DESCRIPTION as `\n`. Keep each line to 75 characters or fewer.

```text
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//ADHD Support Skills//EN
BEGIN:VEVENT
UID:20261020T080000-call-gp@adhd-support-skills
DTSTAMP:20261019T120000Z
DTSTART:20261020T080000
DTEND:20261020T081500
SUMMARY:Call GP surgery
DESCRIPTION:Number is in your phone under GP.
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:Call GP surgery
TRIGGER:-PT10M
END:VALARM
END:VEVENT
END:VCALENDAR
```

- **Floating time** (`DTSTART:20261020T080000`, with no `Z`) means "08:00 wherever the device is". This is usually right for personal reminders.
- **Fixed time zone:** if the event must stay at 08:00 London time even while travelling, use the script with `--tz Europe/London`. It writes the UTC time with a `Z`. The script refuses times that don't exist, or happen twice, on a daylight-saving change, and asks you to choose.
- **Repeating:** add `RRULE:FREQ=DAILY`, `RRULE:FREQ=WEEKLY` or `RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR`. Only add a repeat when the user asked for one.
- **Telling the user:** "Save this as `call-gp.ics` and open it. Your calendar should offer to add it." Never claim it has been added.

## Notes: Obsidian and other Markdown apps

Plain Markdown works in Obsidian and in most notes apps. Tasks use `- [ ]`.

```markdown
# Grant application — restart

Created: 2026-10-19

## Resume
- Done: intro and section 1
- Resume at: budget table
- Next action: add the laptop quote

## Later
- [ ] Ask Sam for the equipment quote
- [ ] Check the deadline on the funder's page
```

- **Brain dump:** use headings for NOW, NEXT, LATER and BLOCKED, with tasks as `- [ ]`. Put ideas under `## Ideas` as plain bullets, not tasks.
- No tags by default. Add tags only if the user asks for them.
- With file access to a vault the user named, create a new note (for example `Restart – Grant application.md`). Otherwise give the text to paste into a new note.

## Reminder and task apps: plain checklist

One item per line, short and action-first. Most reminder and task apps accept pasted or typed items. Some create several items from a pasted list, but behaviour varies, so tell the user to check.

```text
Put parcel by the front door (when closing laptop, 17:30)
Book boiler service
Call GP surgery 08:00
```

If the app supports due times, say which item has which time. Don't invent times.

## Choosing the format

| The user wants… | Offer |
|---|---|
| Something to happen at a time | Calendar file (`.ics`) with an alert, or the checklist line with the time |
| To keep a list or a restart card | Markdown note |
| Tasks in a reminder or task app | Plain checklist |
| Not sure | Ask one question: "Which app do you want this in?" |
