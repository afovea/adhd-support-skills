# Privacy and retention

Plain answers to: what is stored, where it is kept, what can be deleted, and what the suite cannot control.

## What the plugin itself stores

| Data | Stored? | Where | Default |
|---|---|---|---|
| Current task, next action, restart marker | Only in the conversation | Host conversation | Session-only |
| Restart cards | Only if you copy them, or ask for one to be saved to a file | Wherever you put them | Not saved |
| My Point of Truth preferences | Only if you turn memory on and choose a folder (or use the host's own memory) | `MPoT.md`, `user-decisions.md`, optional `MPoT-inbox.md` in **your** folder | Off |
| Proposed preferences (inbox) | In the conversation, unless you agree to a persistent inbox | Same folder | Session-only |
| Telemetry, analytics, recordings, attention scores | **Never** | — | — |
| Camera, microphone, screen, keystroke or app activity | **Never collected** | — | — |
| Crisis or self-harm disclosures | **Never stored** (MPoT refuses them) | — | — |

The installer writes only the skill files, an ownership manifest (`.adhd-support-skills.json`, which lists file hashes and holds no personal data) and the managed router block. It never creates a profile or memory folder, enables reminders, or touches health settings.

## What the host may store separately

The host application (Claude Code, Codex, claude.ai or another) may keep:
- conversation history;
- its own memory features;
- logs;
- cloud backups.

These follow the host's own retention policy, and the suite cannot see, change or delete them. Reminders or calendar events created through a host tool live in that tool, under its rules.

## Where private data lives

Only where you choose. The MPoT tool refuses to:
- put a store inside a Git working tree (so preferences are never committed);
- put a store inside the plugin folder (so they never ship in a bundle).

It never syncs remotely. It does not encrypt anything; if you need encryption, put the folder on encrypted storage. One person's MPoT is never applied to another person.

## What can be deleted, and what cannot be verified

| You ask | The suite does | It cannot verify |
|---|---|---|
| "Forget that preference" | Removes the entry, the earlier versions it superseded, related proposals, related decision-log entries and suite-created caches | Host conversation history, host memory, backups, sync copies, exported copies |
| "Reset my memory" | Deletes `MPoT.md`, `MPoT-inbox.md`, `user-decisions.md` and the ID counter (after one confirmation) | Same as above |
| "Export my preferences" | Writes a copy where you choose | Anything that happens to that copy afterwards |

Deletion overrides the append-only decision log. Nothing deleted is kept "for audit".

## Optional integrations

All integrations are optional and off unless the host provides them and you use them: timers, notifications, calendars, files, web search, memory, and external messaging. Without them, the suite gives copyable text.

## Which actions send content anywhere

- **Every message goes to the host's model provider.** That is how the host works; this suite adds nothing to it.
- **Reminders, calendar events and files**, only through a host tool you asked for. The reminder text is what you see. A discreet wording is offered for sensitive items.
- **Web retrieval**, if the host has it. This sends search terms, not your private documents. The suite never uploads documents just to look up general health information.
- **Messages and emails**: drafts only, unless you explicitly say to send a specific message and the host has a tool for it.

## When the host lacks a safety or capability mechanism

- Urgent help: the suite gives only generic guidance on finding help locally. It never looks up or names local services.
- No scheduler: no check-ins or reminders are promised.
- No memory: session-only, with a copyable card.
- No permission controls: the suite relies on its instructions, which **are not enforcement**.

## Instruction-level safeguards versus enforced controls

| Instruction-level only (SKILL.md text) | Enforced in code |
|---|---|
| No diagnosis or medicine advice; safety escalation; no fake success; content treated as data; no sending without authority | MPoT tool: no store in a repository or the plugin; refuses crisis content, secrets and unapproved health data; atomic writes; stale-hash conflict refusal; cascading delete |
| Quiet and stop cancel suite check-ins | Reference procedure `capability_ops.cancel_owned` cancels only suite-owned IDs (a host adapter must wire it in) |
| | Installer: ownership manifest; never overwrites foreign or edited files; uninstall removes only owned, unmodified files |

## Before any public deployment

User consent in this design is **not** a legal compliance finding. Before public deployment:
- Assess UK GDPR / EU GDPR, or the applicable data-protection duties. Health data and inferences about health can be special-category data (CLM-GD-ICO-SPECIAL). ICO guidance was under review following the Data (Use and Access) Act when accessed.
- Decide whether a DPIA is needed. It probably is, given the health context.
- Assess medical-device qualification from the intended purpose, the marketing claims and the actual functions (CLM-GD-MHRA-SAMD). The product cannot certify its own exemption through wording.
- Have a privacy/legal reviewer confirm this document.
