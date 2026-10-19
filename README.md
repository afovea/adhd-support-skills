# ADHD Support Skills

Practical, low-pressure help with the *doing* side of everyday life: getting things out of your head, choosing what's next, starting, keeping going, getting back to it after an interruption, switching tasks, remembering later, and stopping when you need to.

It is a set of 13 portable [Agent Skills](https://agentskills.io/specification) with a small router. It works in Claude Code and Codex, and has a plain-text fallback for any assistant.

**You don't need a diagnosis, and you don't need to explain yourself.** Ask in ordinary words.

> This is not a medical service. It doesn't diagnose ADHD or anything else, doesn't advise on medicine or treatment, and hasn't been clinically validated. For health decisions, talk to your GP, prescriber or pharmacist. If you're in danger, contact your local emergency services.

## Quick start

Install it (see [INSTALL.md](INSTALL.md)), then just ask:

| You say | What happens |
|---|---|
| "I know what I need to do but can't start the report" | One small starting step, then it gets out of the way |
| "Everything is in my head: …" | Your list, sorted into NOW / NEXT / LATER, with nothing invented |
| "I have five things and don't know what to do first" | One recommendation with a reason, and any guesses labelled |
| "Body double me while I tidy" | Quiet company on your terms, and honest about what an AI can't do |
| "I have forty minutes" | Work time, wrap-up time, a spare buffer and a stopping point |
| "Don't let me forget the parcel tomorrow" | A "when X, do Y" cue and copyable reminder text (or a real reminder, if your app supports it) |
| "Where was I?" | Your last confirmed place, or a short question if it doesn't know |
| "I need to switch to a meeting" | A save point, then the next thing |
| "Help me make mornings simpler" | One small routine anchored to something you already do |
| "This is too much" | Pause, sort out what really matters, or one tiny step |
| "What does an ADHD assessment involve?" | Sourced general information, with its limits |
| "Remember I prefer short steps" | Kept for this conversation, or saved to your private My Point of Truth if you've turned that on |

You can also name a skill: `/adhd-start` in Claude Code (`/adhd-support-skills:adhd-start` if installed as a plugin), or `$adhd-start` in Codex.

## You're in control

Say any of these at any time:
- **"quiet"**: no more prompts.
- **"pause"**: hold everything for now.
- **"stop"**: end the session, with no guilt trip.
- **"less"**: shorter replies.
- **"more detail"** or **"full plan"**: more information.
- **"no praise"**: just the facts.
- **"not that"**: try something else.

Quiet and stop also cancel any check-in this suite set, where your app supports that.

## What it won't do

- Pretend a timer, reminder, calendar entry, message or memory exists when it doesn't.
- Watch you, or claim to know what you did while you were quiet.
- Diagnose you, or tell you to change, stop or double a medicine.
- Send anything on your behalf from a draft.
- Use shame, streaks, manufactured urgency or patronising praise.
- Store health details or crisis disclosures.

## Your data

Task details stay in the conversation. Long-term memory (**My Point of Truth**) is off unless you turn it on and choose a private folder. You can view, correct, export or delete it at any time. Deletion is real, but the suite can't erase what your app keeps in its own history. See [docs/privacy-and-retention.md](docs/privacy-and-retention.md).

## Evidence, honestly

Some of the ideas here, such as breaking tasks down, external reminders, timers and routines, are consistent with ADHD guidance and with what adults with ADHD say helps. **None of that research tested this software.** Body doubling is popular, but the evidence is descriptive and preliminary, and no mechanism (such as "dopamine") has been established. Every health claim the skills make is traced to a checked source in [evidence/](evidence/), with its limits. Nothing has been reviewed by a clinician yet.

## The skills

| Skill | Purpose |
|---|---|
| `adhd-help` | Find the right support when you're not sure what you need |
| `adhd-brain-dump` | Get it out of your head |
| `adhd-prioritise` | Choose what's next |
| `adhd-start` | Get started |
| `adhd-body-double` | Quiet company while you work |
| `adhd-time` | Make time visible |
| `adhd-remember` | Remember to do it later |
| `adhd-restart` | Get back to it |
| `adhd-transition` | Switch tasks safely |
| `adhd-routine` | Build a flexible routine |
| `adhd-overwhelm` | Too much right now |
| `adhd-information` | ADHD health information |
| `my-point-of-truth` | Your saved preferences (My Point of Truth) |

## Repository map

| Path | What |
|---|---|
| `skills/` | Canonical skills, one `SKILL.md` each, plus a generated evidence card. MPoT includes `scripts/mpot.py` |
| `shared/` | Interaction, safety, evidence, permission and memory policies; execution state; core boundaries |
| `routing.md` · `skills-registry.yaml` | The router, and the machine-readable registry (triggers, boundaries, resources, evals, mechanism map) |
| `evidence/` | Sources, claims, audit, generic urgent-help guidance, generated runtime snapshot |
| `templates/` | MPoT, decision-log and restart-card templates |
| `adapters/` | Claude Code and Codex manifests; generic setup guide |
| `scripts/` | `build.py`, `validate.py`, `install.py`, `evals.py`, `capability_ops.py` |
| `tests/` | Routing, behaviour, safety and memory cases; unit tests; recorded results |
| `docs/` | Source analysis, design decisions, capability matrix, privacy, evaluation plan, release readiness |
| `examples/` | Synthetic example conversations |
| `dist/` | **Generated** bundles. Don't edit; run `python3 scripts/build.py dist` |

## For maintainers

```bash
python3 scripts/build.py dist
```

```bash
python3 scripts/validate.py --host-checks
```

Build and validation need Python 3.9+ and PyYAML. The installed skills and the installer need only the Python standard library, and the skills need nothing at all. Edit `shared/core-boundaries.md` rather than the copies inside each SKILL.md; `build.py sync` updates them.

Status: **0.1.0, local build.** This is not a public release. See [docs/release-readiness.md](docs/release-readiness.md).
