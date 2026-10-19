# Design decisions

These are routine assumptions, recorded so that work could proceed without blocking. Each has a reconsideration trigger.

| # | Decision | Why | Reconsider when |
|---|---|---|---|
| D1 | **The first release is aimed at adults.** No age questionnaire and no birth-date collection. A known younger user gets age-appropriate practical and safety help. | Most of the source material concerns adults. Asking for age before ordinary task help adds friction and collects data | Before any child- or teen-specific product or marketing. That needs a separate safeguarding, developmental and clinical review |
| D2 | **No diagnosis or disclosure is needed.** ADHD is never inferred from writing or use. | Dignity and privacy. Inferred health data is special-category data under UK GDPR (CLM-GD-ICO-SPECIAL) | Never relaxed |
| D3 | **Not a clinical product.** No diagnosis, treatment, titration or clinical monitoring. Not marketed as clinically validated. | What the product does and claims determines its regulatory status (CLM-GD-MHRA-SAMD). A disclaimer does not | Any change in intended purpose or claims needs a regulatory assessment first |
| D4 | **One canonical skill set, materialised at build time.** Shared policies live in `shared/` and are copied into each skill's `references/shared/`. | Every skill must work alone, with no parent-directory links. Claude Code plugin paths refuse `..` | A host gains verified support for shared resources |
| D5 | **The core-boundaries block is embedded verbatim in every SKILL.md** and checked by the validator. | Each independently callable skill must carry its essential safeguards without loading the router | Never removed. Wording changes go through `shared/core-boundaries.md` |
| D6 | **Natural-language selection is on.** Neither explicit-only flag is used. | Product requirement | If over-triggering is observed, tighten the descriptions first |
| D7 | **Descriptions are discriminating, with exclusions** ("Not for coding, cameras, servers or startup scripts"). | Words like help, focus and overwhelmed appear in unrelated technical work | Routing evals show misfires |
| D8 | **ZIPs for claude.ai use 200-character descriptions taken from the registry.** | The host docs disagree (200 vs 1,024 characters), so the safe choice was taken | The claude.ai limit is confirmed |
| D9 | **Quiet, user-led presence is the default for body doubling.** The skill states once that it cannot observe or check in. | Matches the evidence that an over-talkative partner is a failure mode, and is honest about turn-based chat | A host offers verified scheduling. A checkpoint is still created only on request |
| D10 | **No timers, reminders or check-ins are simulated.** No waiting loops. | A simulated timer is a fake capability | Never |
| D11 | **Timings (25/5, 10 minutes, under-2-minute starts) are labelled heuristics.** | No optimal interval is established | User research gives grounds to change the defaults |
| D12 | **Urgent-help guidance is generic and works anywhere.** No phone numbers, named helplines, directories or national services, and no asking for the user's country. It tells people how to find help: local emergency services, a crisis line where they live, a doctor or urgent care, someone they trust. | The user could be anywhere. Localised details are wrong for most people, go stale, and can delay help. Product owner decision, 2026-10-19 | Clinical review of the generic wording before release |
| D13 | **MPoT is file-backed in a folder the user chooses, or uses host memory.** It is never global by default, never inside a Git repository, and never inside the plugin. | Private data must not ship or leak between projects | A host provides an audited private store |
| D14 | **MPoT refuses crisis content and secrets outright, and refuses health details unless separately approved.** | The memory policy says to store the practical accommodation, not the condition | Never relaxed for crisis content |
| D15 | **Deletion overrides append-only history.** `forget` follows supersession chains and related decisions. | The brief says deletion requests take priority over history | Never |
| D16 | **Evidence: "verified" requires reading the relevant passage.** Claims checked only against an abstract are recorded as `partial-access`. | Status must reflect what was actually read | Full texts are obtained |
| D17 | **The installer is written in Python (stdlib only)**, not Bash. | Works on macOS, Linux and Windows, and gives atomic writes and a JSON ownership manifest | — |
| D18 | **No licence file.** Owner and author are left unset in the manifests (the marketplace has an `OWNER-TO-BE-CONFIRMED` placeholder). | No licence or owner was authorised, and inventing one would be wrong | Before any public release |
| D19 | **Router text names skills only, never paths.** | Removes path rewriting and the drift that comes with it | — |
| D21 | **App linking works with what the user already uses**: a real connected tool, then file access to a folder they named, then portable handoffs (`.ics`, Markdown, checklist). No suite-built connectors. | Portable, no new code touching personal data, no per-app upkeep. Product owner decision, 2026-10-19 | A host-neutral connector standard is stable, and a security review is budgeted |
| D22 | **Neutral about products.** The suite never names or recommends apps, including specialist ADHD apps. It helps by the user's own criteria. | Avoids implied endorsement, commercial steering, stale lists and unsupported claims. Product owner decision, 2026-10-19 | Never relaxed without a reviewed, dated, conflict-of-interest-free process |
| D20 | **Synthetic examples only.** No real health records, no real notifications. | Privacy | — |

## Host limitations accepted

- A turn-based chat cannot speak first. Body doubling and reminders are honest about this rather than emulating presence.
- SKILL.md instructions are not enforcement. Sandboxing, encryption, tool interception, crisis detection and deletion from host records are not guaranteed. See `privacy-and-retention.md`.
- Codex and the claude.ai upload route could not be exercised in this build environment. See `capability-matrix.md`.
