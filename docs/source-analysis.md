# Source analysis

What the build inputs contributed, what was rejected, and how each mechanism was carried into the suite.

## Inputs read

| Input | Role | Treated as |
|---|---|---|
| `deep-research-report (9).md` — body-doubling agent specification | Design input | Research and design ideas. Not requirements and not clinical evidence |
| `deep-research-report (10).md` — ADHD-support agent behavioural specification | Design input | Same |
| `My-Point-of-Truth-Guidance.md` | Concept definition for MPoT | Design authority for the MPoT concept, within the brief's safety and privacy rules |
| Official host documentation, accessed 2026-10-19 | Host facts | See `capability-matrix.md` |

The source files were left unchanged. Nothing from the reports was copied into a runtime prompt without being checked first.

## What the reports got right, and what was kept

- **Minimum effective intervention.** Make one visible next step, then make it smaller, then change strategy, then replan or defer, rather than escalating reminders. → `shared/interaction-policy.md` and `adhd-start`.
- **Five execution states.** Organise, Activate, Maintain, Recover and Transition. → `shared/execution-state.md`.
- **Quiet presence as a complete mode** for body doubling, with an agreed interruption contract and honest artificial identity. → `adhd-body-double`.
- **No fabricated tool success.** A list of assertions that need verification. → `shared/permission-policy.md` and core boundaries.
- **Preferences, not dossiers**, with inspect, correct and delete controls. → MPoT.
- **Functional success measures** in place of engagement. → `evaluation-plan.md`.

## What was rejected or changed

| Report content | Problem | Decision |
|---|---|---|
| Embedded "system prompt modules" | These were written as authoritative prompts with no attached evidence status | Rewritten into skills and policies. Evidence claims are linked to the verified register |
| Exported `cite…turn…` markers | Not references, and could not be resolved | Every original source was located independently. See `evidence/evidence-audit.md` |
| "Evidence strength: high/moderate" ratings for each mechanism | These are engineering confidence ratings, not GRADE, and they mix clinician-delivered CBT evidence with evidence for software | Replaced by evidence categories plus per-claim status. No GRADE-style labels |
| Trial sizes (60–100, 120–200, 12 sessions, and so on) | Planning hypotheses with no research question or power analysis behind them | Kept only as hypotheses in `evaluation-plan.md`. Not adopted |
| 25/5 and 10-minute timings | Product heuristics | Kept as configurable defaults, labelled as such |
| "Fade support" as a goal | The brief says continuing to use an accommodation that works is valid | Reframed: offer less support when it isn't needed; never push the user to withdraw from support |
| "ADHD-support execution agent for adults" role framing | Could imply a clinical identity, or require a diagnosis | No persona. Practical help needs no diagnosis or disclosure |
| UK-specific crisis routes (NHS 111, 999) | Jurisdiction-specific; users may be anywhere; source review dates had lapsed | Removed. Only generic guidance on finding help locally. No numbers, named services or country questions |
| Body-double "visible avatar", camera and audio modalities | Out of scope for a text-first instruction plugin. They also create privacy risk | No sensing or monitoring. Text presence only |
| Measurement after every session (0–10 scales) | Questionnaire burden | At most one optional reflection question |

## Mechanism map

Every mechanism in the reports maps to a skill or a shared behaviour. The machine-readable version is the `mechanisms` section of `skills-registry.yaml`, which the validator checks.

| Mechanism | Where it lives |
|---|---|
| Executive-function offloading (NOW / NEXT / LATER / BLOCKED) | `adhd-brain-dump`, `execution-state.md` |
| Task initiation scaffolding | `adhd-start` |
| Cognitive load reduction | `interaction-policy.md` (shared behaviour) |
| Temporal scaffolding | `adhd-time` |
| Attention recovery and resumption | `adhd-restart`, restart card |
| Decision and prioritisation | `adhd-prioritise` |
| Prospective memory (cue–action pairs) | `adhd-remember` |
| Immediate reinforcement | `interaction-policy.md`: factual, optional encouragement only |
| Routine and habit scaffolding | `adhd-routine` |
| Overwhelm management | `adhd-overwhelm`, `safety-policy.md` |
| Task switching (STOP / SAVE / RESET / START) | `adhd-transition` |
| Adaptive support and self-management | `my-point-of-truth`, `memory-policy.md` |
| Delegation / automation authority levels | `permission-policy.md` |
| Body doubling: roles, contract, failure modes | `adhd-body-double` |
| Within-person comparison of presence against structure | `evaluation-plan.md` |
| MPoT: precedence, entry types, statuses, decision log, inbox | `my-point-of-truth`, `memory-policy.md`, `templates/` |
