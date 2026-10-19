# adhd-support-skills

Practical, low-pressure help with the *doing* side of everyday life: getting things out of your head, choosing what's next, starting, keeping going, getting back to it after an interruption, switching tasks, remembering later, and stopping when you need to.

It is **14 portable [Agent Skills](https://agentskills.io/specification)** with a small routing brain, plus **My Point of Truth**, a private register of how you like to be helped that you control. It runs inside the AI assistant you already use: Claude, ChatGPT, Codex, or any assistant you can give instructions to.

**You don't need a diagnosis, and you don't need to explain yourself.** Ask in ordinary words.

> **Not medical care.** It doesn't diagnose ADHD or anything else, doesn't advise on medicine or treatment, and hasn't been clinically validated. For health decisions, talk to your doctor, prescriber or pharmacist. If you're in danger, contact your local emergency services.

**→ [What it helps with](#the-13-skills)**
What each skill does, in plain words, with the request that triggers it.

**→ [Works with the apps you already use](#working-with-your-other-apps)**
Calendars, reminder apps, Obsidian and other notes apps, task managers: through a real connection, or a file or list to import. No product is pushed.

**→ [Example conversations](./examples/conversations.md)**
Six made-up conversations covering overdue paperwork, writing, a home task, an interruption, a routine and preparing for an appointment. They show how it is meant to behave.

**→ [Evidence, honestly](#evidence-honestly)**
What the research does and doesn't support. Every health claim traces to a checked source. None of that research tested this software.

## Contents

- [Quick start](#quick-start): find your row before you copy anything
  - [A · Claude web (`claude.ai` in a browser)](#a--claude-web-claudeai-in-a-browser)
  - [B · Claude app, Chat tab](#b--claude-app-chat-tab)
  - [C · Claude app, Code tab (Claude Code)](#c--claude-app-code-tab-claude-code)
  - [D · Claude Code in a terminal](#d--claude-code-in-a-terminal)
  - [E · ChatGPT](#e--chatgpt)
  - [F · Codex, and other `SKILL.md` hosts](#f--codex-and-other-skillmd-hosts)
  - [G · Any other assistant](#g--any-other-assistant)
- [Using it](#using-it): ordinary words, naming a skill, and the controls that always work
- [What it won't do](#what-it-wont-do)
- [The 14 skills](#the-14-skills): grouped, with when to reach for each
- [Working with your other apps](#working-with-your-other-apps): calendars, reminders, Obsidian, task apps
- [My Point of Truth](#my-point-of-truth): private, approved preferences, with deletion that really deletes
- [Safety and health boundaries](#safety-and-health-boundaries)
- [Evidence, honestly](#evidence-honestly)
- [Privacy](#privacy)
- [Install options](#install-options): every route compared, plus the installer
- [Compatibility](#compatibility): how each host loads and invokes the skills
- [Repository layout](#repository-layout)
- [Building from source](#building-from-source)
- [Conventions](#conventions)
- [Versioning](#versioning)
- [Licence](#licence)
- [Contributing](#contributing)

## Quick start

**Find your row, then read that section.** Which app you're in decides the method.

| Where you are | Method | Section |
|---|---|---|
| **Claude web** (`claude.ai` in a browser) | Upload skill ZIPs | [A](#a--claude-web-claudeai-in-a-browser) |
| **Claude app**, **Chat** tab | Upload skill ZIPs | [B](#b--claude-app-chat-tab) |
| **Claude app**, **Code** tab | Two typed lines, all 14 | [C](#c--claude-app-code-tab-claude-code) |
| **Claude Code** in a terminal | Two typed lines, all 14 | [D](#d--claude-code-in-a-terminal) |
| **ChatGPT** (custom GPT or Project) | Paste the compact instructions | [E](#e--chatgpt) |
| **Codex**, or any host that reads `SKILL.md` | One command, all 14 | [F](#f--codex-and-other-skillmd-hosts) |
| **Any other assistant** | Paste the single-file instructions | [G](#g--any-other-assistant) |

---

### A · Claude web (`claude.ai` in a browser)

1. **Settings → Capabilities**, then switch on **Code execution**. Skills don't run without it.
2. Download a skill from [`dist/zips/`](./dist/zips). Start with [adhd-help.zip](./dist/zips/adhd-help.zip), the one that picks the right support. **Don't unzip it.**
3. **Customize → Skills → + → Upload a skill**, choose the file, and switch it on.
4. Ask in ordinary words: *"I know what I need to do but I can't start the report."*

Add more skills the same way. Each ZIP has one skill folder and a description of 200 characters or fewer, the stricter of the two limits claude.ai's documentation states.

### B · Claude app, Chat tab

These are the same files and the same account as A, so skills you uploaded in the browser are already here. If not, follow A, using **Customize** in the left sidebar.

### C · Claude app, Code tab (Claude Code)

This installs all 14 at once. Type the two lines into the ordinary message box:

```
/plugin marketplace add afovea/adhd-support-skills
/plugin install adhd-support-skills@adhd-support-skills
```

If it says `Run /reload-plugins to activate.`, run that too. Plugin skills are namespaced, so you can name one directly:

```
/adhd-support-skills:adhd-start I can't start my expenses claim.
```

You don't have to, though. Natural-language selection is on, so *"I can't start my expenses claim"* is enough.

To try the plugin for one session without installing anything, use `claude --plugin-dir dist/claude-code` from a clone.

### D · Claude Code in a terminal

This is identical to C. Run `claude` from any folder, then type the same two lines.

If you also want the routing brain in a project's `CLAUDE.md` (a plugin can't add it), see [Install options](#install-options).

### E · ChatGPT

ChatGPT custom GPT instructions are reportedly limited to about 8,000 characters, so there's a compact version built for it.

1. Copy all of [`dist/generic/ADHD-support-instructions-compact.md`](./dist/generic/ADHD-support-instructions-compact.md) (about 7,200 characters).
2. In ChatGPT, create a GPT (**Explore GPTs → Create → Configure**) and paste it into **Instructions**. Or paste it into a Project's instructions.
3. Optional: upload [`dist/generic/ADHD-support-instructions.md`](./dist/generic/ADHD-support-instructions.md) and a few `dist/skills/*/SKILL.md` files as Knowledge, for deeper behaviour.

The compact file keeps the shared safety rules word for word. The build fails if it exceeds 7,800 characters or loses a required safeguard. Menu names may differ on your plan.

### F · Codex, and other `SKILL.md` hosts

The skills follow the [Agent Skills](https://agentskills.io) standard, so any host built on it can read them. In Codex they live in `.agents/skills/`, and you invoke one with `$name`.

```bash
git clone https://github.com/afovea/adhd-support-skills.git
cd adhd-support-skills
python3 scripts/install.py --host codex --personal --dry-run
python3 scripts/install.py --host codex --personal
```

That installs all 14 into `~/.agents/skills/`. Restart Codex, then try: `$adhd-start I can't start the report.` A Codex plugin and local marketplace also ship in [`dist/codex`](./dist/codex).

### G · Any other assistant

Paste [`dist/generic/ADHD-support-instructions.md`](./dist/generic/ADHD-support-instructions.md) (about 30 KB) into your assistant's custom or project instructions, or use the compact version if it has a size limit. Then talk normally.

Without a skills feature, your assistant can't load the detailed skill files, so this is a lighter version. The safety rules and controls are included.

---

**➡️ [Step-by-step guide for all of these](./INSTALL.md)**: updating, checking what's installed, removing it, turning on memory, and troubleshooting.

[↑ Back to contents](#contents)

## Using it

**Just ask in ordinary words.** The routing brain works out which kind of help you need. It won't announce the routing; it just helps ("Let's make the first step smaller").

| You say | What happens |
|---|---|
| "I know what I need to do but can't start the report" | One small starting step, then it gets out of the way |
| "Everything is in my head: …" | Your list, sorted into NOW / NEXT / LATER / BLOCKED, with nothing invented |
| "I have five things and don't know what to do first" | One recommendation with a reason, and any guesses labelled |
| "Body double me while I tidy" | Quiet company on your terms, and honest about what an AI can't do |
| "I have forty minutes" | Work time, wrap-up time, a spare buffer and a stopping point |
| "Don't let me forget the parcel tomorrow" | A "when X, do Y" cue and copyable reminder text, or a real reminder if your app can confirm it |
| "Where was I?" | Your last confirmed place, or a short question if it doesn't know |
| "I need to switch to a meeting" | A save point, then the next thing |
| "Help me make mornings simpler" | One small routine anchored to something you already do |
| "This is too much" | Pause, sort out what really matters, or one tiny step |
| "What does an ADHD assessment involve?" | Sourced general information, with its limits |
| "Add this to my calendar" / "Put it in my Obsidian vault" | Added through your app's connection if there is one, or given to you as a calendar file or Markdown note to import |
| "Send these to my reminders app" | Added through a real connection, or given as a checklist you can paste in |
| "Which app should I use for reminders?" | Help choosing by what matters to you, starting from what you already have. No brands pushed |
| "Remember I prefer short steps" | Kept for this conversation, or saved to your private My Point of Truth if you've turned it on |

### Controls that always work

Say any of these at any time, in any skill:
- **quiet**: no more prompts.
- **pause**: hold everything.
- **stop**: end, with no guilt trip.
- **less**: shorter replies.
- **more detail** or **full plan**: more.
- **no praise**: just the facts.
- **not that**: try something else.

Quiet and stop also cancel any check-in this suite set, if your app supports check-ins. "Leave me alone while I work" means quiet. It doesn't start body doubling.

### Naming a skill

| Host | Form |
|---|---|
| Claude Code, filesystem install | `/adhd-start …` |
| Claude Code, plugin install | `/adhd-support-skills:adhd-start …` |
| Codex | `$adhd-start …` |
| Claude apps, ChatGPT, other assistants | Ask in ordinary words, or say "use the adhd-start skill" |

### Automatic selection is on, on purpose

These skills are meant to be picked from ordinary requests. Someone who is stuck shouldn't need to learn skill names first. Neither `disable-model-invocation` nor `allow_implicit_invocation: false` is used, and the validator fails if either appears.

To stop the skills firing on unrelated work, every description is discriminating and says what it is not for:
- "How do I get my camera to focus?" is a photography question;
- "my server is overwhelmed" is an infrastructure question;
- "debug the startup script" is a debugging question.

None of them activates ADHD support.

[↑ Back to contents](#contents)

## What it won't do

- Pretend a timer, reminder, calendar entry, message or memory exists when it doesn't.
- Watch you, or claim to know what you did while you were quiet. Silence isn't evidence of anything.
- Diagnose you, or tell you to change, stop, skip or double a medicine.
- Send anything on your behalf from a draft.
- Use shame, streaks, manufactured urgency or patronising praise.
- Store health details, diagnoses or crisis disclosures.
- Follow instructions hidden in documents, web pages or imported files.

[↑ Back to contents](#contents)

## The 14 skills

Every skill is self-contained. The shared safety rules are embedded in each `SKILL.md`, and the full policies are bundled in its `references/shared/` folder, so any skill works on its own without the router.

### Find the right support

| Skill | Use when |
|---|---|
| [`adhd-help`](./skills/adhd-help/SKILL.md) | "Help, I'm stuck" or "what can you do?", and the obstacle is unclear. Asks one short question at most |

### Organise and choose

| Skill | Use when |
|---|---|
| [`adhd-brain-dump`](./skills/adhd-brain-dump/SKILL.md) | Too much in your head. Keeps every item; separates tasks, ideas and feelings; shows NOW / NEXT / LATER / BLOCKED |
| [`adhd-prioritise`](./skills/adhd-prioritise/SKILL.md) | Several things and you can't choose. Uses real deadlines, consequences and who is waiting; never invents urgency |

### Start and keep going

| Skill | Use when |
|---|---|
| [`adhd-start`](./skills/adhd-start/SKILL.md) | You know the task but can't begin. One concrete action of under two minutes; smaller if it doesn't help |
| [`adhd-body-double`](./skills/adhd-body-double/SKILL.md) | You want quiet company while you work. You set the terms, and it is honest that an AI can't watch you or check in from chat |
| [`adhd-time`](./skills/adhd-time/SKILL.md) | A fixed window or a departure time. Work, wrap-up and buffer, plus a stopping point. Real timers only if your app has them |

### Remember, recover and switch

| Skill | Use when |
|---|---|
| [`adhd-remember`](./skills/adhd-remember/SKILL.md) | A future intention has to come back at the right moment. "When X, do Y", with confirmed reminders or copyable text |
| [`adhd-restart`](./skills/adhd-restart/SKILL.md) | You lost your place. Restores only what was confirmed; never invents progress |
| [`adhd-transition`](./skills/adhd-transition/SKILL.md) | Switching task or stopping for the day: STOP → SAVE → RESET → START. Never closes or deletes anything |
| [`adhd-routine`](./skills/adhd-routine/SKILL.md) | A small, flexible routine anchored to something you already do, with a bad-day version. No streaks |

### When it's too much

| Skill | Use when |
|---|---|
| [`adhd-overwhelm`](./skills/adhd-overwhelm/SKILL.md) | Overloaded. Pause, triage or one tiny step. Not therapy, and no crisis script for ordinary overwhelm |

### Health information

| Skill | Use when |
|---|---|
| [`adhd-information`](./skills/adhd-information/SKILL.md) | General ADHD health information, the evidence for strategies, preparing for an appointment, drafting an adjustment request. Never diagnoses or advises changing medicine |

### Your other apps

| Skill | Use when |
|---|---|
| [`adhd-connect`](./skills/adhd-connect/SKILL.md) | "Add this to my calendar", "put it in Obsidian", "help me connect my calendar", "which app should I use?". Uses a real connection or gives a file or list to import. Neutral about products |

### Your preferences

| Skill | Use when |
|---|---|
| [`my-point-of-truth`](./skills/my-point-of-truth/SKILL.md) | "Remember I prefer short steps", "what do you remember?", "forget that". See [My Point of Truth](#my-point-of-truth) |

The machine-readable map of triggers, boundaries, resources, evaluations and source mechanisms is [`skills-registry.yaml`](./skills-registry.yaml).

[↑ Back to contents](#contents)

## Working with your other apps

People already have calendars, reminder apps, Obsidian or other notes apps, task managers and specialist tools. The suite works **with whatever you already use**, and never needs or recommends a particular product.

| If your assistant… | The suite will… |
|---|---|
| **Has a working connection** to the app (a calendar, reminder, notes or task tool) | Use it: resolve the time first, offer a discreet title for anything sensitive, report the real result, check before retrying and never duplicate. It reads only what the task needs, and treats anything inside your app's data as content, not instructions |
| **Can read and write files**, and you tell it where (for example your Obsidian vault) | Create a new Markdown note, or append to one you name. It never overwrites, never searches your disk, and adds no health-revealing tags unless you ask |
| **Has no connection** | Give you something to import: a calendar file (`.ics`) for Google, Apple or Outlook calendars, a Markdown note for Obsidian and similar apps, or a plain checklist for reminder and task apps. It tells you plainly that nothing has been added yet |

**Connecting an app:**
- **What it helps with.** `adhd-connect` explains in plain words what connecting means. Assistants usually call it Connectors, Apps, Integrations or MCP, and the steps vary.
- **What to know first.** Connecting gives the assistant's provider access to that app's data. Choose read-only first if you're offered it. You can disconnect at any time.
- **Checking it worked.** Afterwards, it checks that the connection works rather than assuming it does.

**Choosing an app:** it won't name or recommend products, including specialist ADHD apps. It starts from what you already have, then helps you decide by what matters to you: does it really alert you, does it work on your devices, cost, where your data is kept, and sensory comfort.

With a shell, `skills/adhd-connect/scripts/make_ics.py` writes a valid calendar file. Repeating reminders stay at the same local time when the clocks change. It refuses times that don't exist, or happen twice, at a clock change. Rules: [`shared/integration-policy.md`](./shared/integration-policy.md). Formats: [`shared/handoff-formats.md`](./shared/handoff-formats.md).

[↑ Back to contents](#contents)

## My Point of Truth

**My Point of Truth (MPoT)** is your private, human-governed record of how you want to be helped. It is an inspectable operating manual, not a profile of who you are.

- **Off by default.** Without it, everything is session-only and you get a copyable preferences card.
- **You choose where it lives**: a private folder outside any project or repository, or your app's own memory. It never ships in the plugin and is never committed.
- **Only what you approve is confirmed.** Patterns the agent notices ("you often work late") stay proposals until you approve them. It never quietly changes how it behaves.
- **Scoped.** "Ten-minute blocks for writing tasks" applies to writing, not to everything.
- **Deletion is real.** "Forget that" removes the entry, its earlier versions, related decisions and any derived summaries. It then tells you honestly what it can't reach: your app's own history, backups and copies you exported.
- **Never stores** diagnoses, health details, crisis disclosures, moods, personality labels or secrets.

With a shell, the bundled tool does the work. It writes atomically, refuses to write if the file changed since you read it, and refuses a location inside a Git repository:

```bash
python3 dist/skills/my-point-of-truth/scripts/mpot.py --store ~/Private/mpot init
python3 dist/skills/my-point-of-truth/scripts/mpot.py --store ~/Private/mpot view
python3 dist/skills/my-point-of-truth/scripts/mpot.py --store ~/Private/mpot forget PREF-003
```

The policy is in [`shared/memory-policy.md`](./shared/memory-policy.md).

[↑ Back to contents](#contents)

## Safety and health boundaries

These rules apply in every skill, including when a skill is invoked directly ([`shared/safety-policy.md`](./shared/safety-policy.md)):

- **Proportionate.** "This report is killing me" is ordinary frustration and gets ordinary help. If something is genuinely unclear, it asks one direct question.
- **Urgent danger stops the task.** The reply is warm and brief, and urges immediate human help. **The guidance is generic, because the user could be anywhere.** It points to local emergency services or the nearest emergency department, a crisis line where the user lives, a doctor, or someone they trust. It gives no phone numbers or named services, and never asks which country the user is in. The build fails if a support number or a named helpline appears in anything it ships.
- **No diagnosis.** It explains that a specialist assessment is needed and offers to help organise your notes.
- **No medicine decisions.** It won't choose, change, stop, time, double or calculate any medicine or dose. A reminder repeats only a schedule you give it.
- **No coercive accountability.** It declines requests for insults, humiliation or skipping food or sleep, and offers a firm, respectful alternative.
- **Adults first.** Younger users get age-appropriate help and encouragement to talk to a trusted adult, and no adult clinical information.

These are instructions, not enforcement. Your app's own safety systems, permissions and retention govern what actually happens. See [`docs/privacy-and-retention.md`](./docs/privacy-and-retention.md).

[↑ Back to contents](#contents)

## Evidence, honestly

Some of the ideas here are consistent with ADHD guidance and with what adults with ADHD say helps: breaking tasks down, external reminders, timers, shorter focus periods and routines. **None of that research tested this software.** Evidence for clinician-delivered CBT is not evidence for an AI plugin.

Body doubling is popular. In one self-selected survey of 220 adults, most said they were more likely to finish tasks with someone present. That is self-report with no comparison group. A small controlled study found no significant difference, a tiny VR study used a human-operated "AI", and no mechanism such as "dopamine" has been established.

| File | What it holds |
|---|---|
| [`evidence/sources.yaml`](./evidence/sources.yaml) | 46 sources, each with category, access date, how much was read, and whether it tested an AI |
| [`evidence/claims.yaml`](./evidence/claims.yaml) | 43 claims: 26 verified against the source, 16 checked against an abstract only, and 1 unverified, which is excluded |
| [`evidence/evidence-audit.md`](./evidence/evidence-audit.md) | Every place the source research reports disagreed with the original papers, and how each was resolved |
| [`evidence/runtime-evidence.md`](./evidence/runtime-evidence.md) | The generated snapshot the skills may cite |

"Link resolves", "source read", "claim verified" and "clinician reviewed" are recorded separately; none implies another.

[↑ Back to contents](#contents)

## Privacy

- **No telemetry, no recording, no passive observation.** Nothing is sent anywhere by this suite.
- Task details stay in the conversation. Memory is off unless you turn it on.
- Your AI app keeps its own conversation history under its own terms. The suite can't see or erase that.
- External actions such as reminders, calendar entries or messages happen only through your app's tools, only when you ask, and only reported as done when the tool confirms it.

The full picture is in [`docs/privacy-and-retention.md`](./docs/privacy-and-retention.md): what is stored, where, what can be deleted, and what can't be verified.

[↑ Back to contents](#contents)

## Install options

| Route | How | You get |
|---|---|---|
| **Plugin from GitHub** | `/plugin marketplace add afovea/adhd-support-skills`, then `/plugin install adhd-support-skills@adhd-support-skills` | All 14 skills, namespaced. No routing brain (a plugin can't write `CLAUDE.md`) |
| **Plugin, one session** | `claude --plugin-dir dist/claude-code` | All 14 for that session only. Nothing installed |
| **Project, Claude Code** | `python3 scripts/install.py --host claude-code --project PATH` | Skills in `.claude/skills/`, plus the router in a managed block in `CLAUDE.md` |
| **Project, Codex** | `python3 scripts/install.py --host codex --project PATH` | Skills in `.agents/skills/`, plus the router in `AGENTS.md` |
| **Router only** | add `--router-only` | Just the managed router block. Use with a plugin install |
| **Personal** | `--personal` | Skills in `~/.claude/skills/` or `~/.agents/skills/`. Your global instruction file is left alone unless you add `--with-router` |
| **Other `SKILL.md` hosts** | `--host generic --skills-dir DIR --instructions FILE` | Skills where you choose, plus the router in any instruction file |
| **Claude apps** | Upload ZIPs from [`dist/zips/`](./dist/zips) | The skills you upload |
| **ChatGPT, any assistant** | Paste from [`dist/generic/`](./dist/generic) | The router, safety rules and controls as instructions |

The installer is plain Python with no dependencies:

```bash
python3 scripts/install.py --host claude-code --project ~/my-project --dry-run    # see what would change
python3 scripts/install.py --host claude-code --project ~/my-project              # install or update
python3 scripts/install.py --host claude-code --project ~/my-project --verify     # what's installed?
python3 scripts/install.py --host claude-code --project ~/my-project --uninstall  # remove it
```

**What the installer does and doesn't touch:**
- **Updates in place.** Re-running updates the suite. Files you've edited are kept and reported (`--force` replaces them).
- **Records ownership.** Each installed file's hash goes into an ownership manifest.
- **Stays inside its markers.** The router sits between `<!-- adhd-support-skills:start -->` and `<!-- adhd-support-skills:end -->`; every other line of your instruction file is untouched.
- **Removes only what it installed.** Uninstall removes only files it installed and you haven't changed, plus the managed block.
- **Leaves everything else alone.** It never touches your other skills or any My Point of Truth folder, and never turns on telemetry, memory or reminders.

The full guide, written for non-technical users, is in [INSTALL.md](./INSTALL.md).

[↑ Back to contents](#contents)

## Compatibility

Based on each host's documentation (Agent Skills spec, Claude Code, Codex, claude.ai), checked 19 October 2026.

| | Claude Code | Codex | Claude apps | ChatGPT / other |
|---|---|---|---|---|
| Skills location | `.claude/skills/` or plugin | `.agents/skills/` or plugin | Uploaded ZIPs | Pasted instructions |
| Invocation | `/name` or `/adhd-support-skills:name` | `$name` | Ordinary words | Ordinary words |
| Automatic selection | On (default) | On (default; `allow_implicit_invocation` not set) | On | Via the pasted router |
| Router | `CLAUDE.md` managed block | `AGENTS.md` managed block (under 32 KiB) | n/a | In the pasted file |
| Plugin manifest | `.claude-plugin/` | root `plugin.json` plus `.agents/plugins/marketplace.json` | n/a | n/a |

Cell-by-cell detail is in [`docs/capability-matrix.md`](./docs/capability-matrix.md).

Timers, reminders, calendars, files, web search and memory are all **unavailable until your app proves otherwise**: a tool exists and returns a confirming result ([`shared/permission-policy.md`](./shared/permission-policy.md)). Basic help works in a plain text chat with none of them.

[↑ Back to contents](#contents)

## Repository layout

```
adhd-support-skills/
├── .claude-plugin/marketplace.json  # GitHub marketplace → serves dist/claude-code
├── skills/                          # canonical source: 14 skills, one folder each
│   ├── adhd-start/
│   │   ├── SKILL.md                 # includes the generated core-boundaries block
│   │   └── references/evidence-card.md   # generated from the evidence register
│   ├── adhd-connect/
│   │   ├── SKILL.md
│   │   └── scripts/make_ics.py      # valid calendar files
│   ├── my-point-of-truth/
│   │   ├── SKILL.md
│   │   └── scripts/mpot.py          # private, file-backed MPoT operations
│   └── ...
├── shared/                          # policies, copied into every skill at build time
│   ├── core-boundaries.md           # the safety block embedded in every SKILL.md
│   ├── interaction-policy.md        # controls, tone, accessibility, timing defaults
│   ├── safety-policy.md             # proportionate levels, generic urgent help
│   ├── evidence-policy.md           # how health claims are made at runtime
│   ├── permission-policy.md         # capability contract, external-action protocol
│   ├── integration-policy.md        # connected apps, file access, neutral app choice
│   ├── handoff-formats.md           # .ics, Markdown (Obsidian) and checklist handoffs
│   ├── memory-policy.md             # My Point of Truth rules
│   └── execution-state.md           # five states, restart card, handoff shape
├── routing.md                       # the routing brain
├── skills-registry.yaml             # triggers, boundaries, resources, evals, mechanism map
├── evidence/                        # sources, claims, audit, generic urgent-help guidance
├── templates/                       # MPoT, decision log, restart card
├── adapters/                        # Claude Code and Codex manifests, generic and compact templates
├── scripts/
│   ├── build.py                     # sync generated sections; build dist/
│   ├── validate.py                  # every structural check, then the tests
│   ├── install.py                   # install / update / verify / uninstall
│   ├── evals.py                     # export blind cases, score, native Claude runner
│   └── capability_ops.py            # reference procedures for reminders and check-ins
├── tests/                           # eval cases, unit tests, recorded results
├── docs/                            # design decisions, capability matrix, privacy,
│                                    #   evaluation plan, release readiness, source analysis
├── examples/conversations.md        # synthetic example conversations
├── site-plan/                       # consumer website plan and the ChatGPT test log
└── dist/                            # GENERATED, don't edit
    ├── skills/                      # standalone, self-contained skill folders
    ├── claude-code/                 # plugin + local marketplace
    ├── codex/                       # plugin + local marketplace
    ├── generic/                     # router, full and compact instructions
    ├── zips/                        # claude.ai uploads
    ├── install.py
    └── MANIFEST.json                # every file with its sha256
```

`dist/` is committed so that people who can't run a terminal can download a ZIP or copy a file directly. The validator fails if it drifts from a fresh build.

[↑ Back to contents](#contents)

## Building from source

```bash
python3 scripts/build.py dist             # sync generated sections, rebuild dist/
python3 scripts/validate.py --host-checks
```

Building and validating need Python 3.9+ and PyYAML. The installed skills need nothing, and the installer and MPoT tool need only the Python standard library.

[↑ Back to contents](#contents)

## Conventions

- **UK English.** Short, concrete language, with no hype, pity or "superpower" framing.
- **Spec-only frontmatter** (`name`, `description`, `metadata`), so the same files work on every host.
- **Don't edit generated text by hand.** The core-boundaries block in each `SKILL.md`, the evidence cards and `runtime-evidence.md` are generated. Edit `shared/core-boundaries.md` or `evidence/claims.yaml`, then run `build.py sync`.
- **Every skill has the same sections:** purpose, exclusions, entry examples, inputs, workflow, stop conditions, missing-capability behaviour, a good example, a failure example, safeguards, evidence, and at least one multi-turn evaluation linked in the registry.
- **Under 500 lines.** Keep skill bodies under 500 lines. Put detail in `references/`.
- **Claims must trace.** A health or scientific claim must trace to a `verified` or `partial-access` entry in `evidence/claims.yaml`. Anything unverified is never asserted.
- **Generic urgent help.** No phone numbers, named services or questions about country, anywhere.

[↑ Back to contents](#contents)

## Versioning

Semver: `v<MAJOR>.<MINOR>.<PATCH>`.

- **MAJOR:** a breaking change to a skill's contract, an installed path or the MPoT format.
- **MINOR:** a new skill, capability or install route.
- **PATCH:** wording, evidence updates or fixes.

The version lives in `skills-registry.yaml` and both plugin manifests. The validator checks they match.

[↑ Back to contents](#contents)

## Licence

No licence has been chosen yet, so all rights are reserved.

[↑ Back to contents](#contents)

## Contributing

Before changing behaviour:

- Edit the canonical files (`skills/`, `shared/`, `routing.md`, `evidence/`), never `dist/`.
- Add or update an evaluation case in `tests/` for any behaviour change, and keep every skill's registry `evals` list pointing at a multi-turn case.
- Trace any new health claim to a checked source in `evidence/claims.yaml`, with its limits.
- Run `python3 scripts/build.py dist` and `python3 scripts/validate.py --host-checks` before committing.
- Record decisions in [`docs/design-decisions.md`](./docs/design-decisions.md). Don't mark anything as reviewed or approved unless it has been.

[↑ Back to contents](#contents)
