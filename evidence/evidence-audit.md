# Evidence audit

This file records how the evidence register was built, every point where the supplied research reports disagree with the original sources, and what remains open.

- **Register:** `sources.yaml` (46 sources) and `claims.yaml` (42 claims).
- **Runtime snapshot:** `runtime-evidence.md`, generated from `claims.yaml` by `scripts/build.py sync`.
- **Verification date:** 2026-10-19.
- **Verified by:** the building agent and its research subagents, reading the pages and abstracts linked. **No clinician, librarian or independent reviewer has checked any of it.**

## What the status fields mean

These are four separate questions. A "yes" to one does not imply a "yes" to any other.

| Field | Meaning |
|---|---|
| `link_resolves` | The URL or DOI opened on the access date |
| `source_read` | `full`, `partial` (the relevant section), `abstract-only`, or `none` |
| `status` | `verified`: the relevant passage was read and the wording matches it. `partial-access`: the wording was checked against an abstract or summary only. `unverified`: the source was not found, or it does not support the wording. `disputed`, `withdrawn` and `superseded` are also allowed. |
| `clinician_reviewed` | Always `false` in this release |

### Rules for `status`

- Any claim checked only against an abstract is downgraded from `verified` to `partial-access`, even where a subagent reported it as verified.
- `runtime-evidence.md` lists `verified` claims as usable at runtime. It lists `partial-access` claims separately, with a "say this was checked against a summary only" flag.
- Unverified claims are left out of the runtime snapshot.

## Method

1. Material health, efficacy and mechanism claims were extracted from deep-research reports (9) and (10). The `cite…` tokens in those reports were exported search markers, not references, so they could not be followed.
2. Each original source was located by title, author, DOI or search. Authoritative pages (NICE, NHS, AADPA, CADDRA, MHRA, ICO, WHO, W3C) were read directly where access allowed. NICE NG87 refused automated fetching (HTTP 403), so the guideline text was downloaded directly and read.
3. Each proposed runtime wording was checked against the source's population and design. It was then rewritten as a bounded statement that says what the source does not establish.
4. Disagreements between the reports and the sources are listed below. Where they disagree, the source wins.

## Corrections to the supplied reports

| Report said | Source shows | Handling |
|---|---|---|
| Eagle et al.: n=220; "186 respondents more likely to complete" | n=220 confirmed. 186 said "somewhat more likely **or** more likely"; only 108 said "more likely". The figures are self-report with no comparison condition and no diagnosis requirement. The paper gives two different counts of neurodivergent respondents (193 and 198); 139 self-identified ADHD. | CLM-BD-SURVEY wording says this. Do not call these "ADHD participants" or "completion outcomes". |
| Schuenke et al.: n=26, null result, quiet neutral double | N=26 and no significant differences confirmed **from the abstract only**. The abstract also reports "promising trends" for unmedicated ADHD participants. The "quiet, neutral double" instruction could not be checked because the full text returned 403. | CLM-BD-EEG is partial-access. The design default of quiet presence is labelled a design choice, not evidence from this study. |
| Ara et al. VR: n=12, AI condition | Confirmed. The "AI" double was operated by a human (Wizard-of-Oz), but participants were told it was AI. ADHD was screened with the ASRS, not formally diagnosed. Preprint. Accuracy differences were not significant. | CLM-BD-VR and CLM-BD-NO-AI. |
| Tan et al.: "twelve dimensions" | The abstract says twelve, section 3.2.4 says ten, and about eleven are named. The count is internally inconsistent. Work in progress, no new data. | Described as a design taxonomy only. No dimension count is stated at runtime. |
| O'Connell et al.: n=11, 10 of 11 continued | 12 recruited and 11 completed. 10 of 11 kept using the robot in the voluntary week (the third week by design; the abstract says the second). The robot made random pre-programmed motions, was not AI and did not respond to the student. No performance outcome was measured. | CLM-BD-ROBOT says acceptability only. |
| Bond & Titus: 241 studies, ~24,000 participants | Confirmed from the abstract. Effects were small (0.3–3% of variance). The simple-task accuracy gain was slight and vulnerable to publication bias. Non-ADHD research, not body doubling. | CLM-BD-SOCIALFAC is partial-access and labelled adjacent evidence. |
| Component NMA, 43 trials and 3,817 participants (author not given) | Matsumoto, Hamatani, Kunisato & Mizuno, BMJ Mental Health, December 2024. The protocol covered ages 10–60. | Not described as adult-only. Abstract only, so partial-access. |
| 2026 experiment, 196 adults: episodic future thinking helps prospective memory | Stelz, Edel & Altgassen 2026 (n=196). A similar 2026 study (Altgassen et al., n=127) found the effect was not significant after controlling for verbal ability. | Mixed findings stated. Not used in runtime advice beyond group-level difficulty. |
| "Preparing a resumption intention reduces resumption cost" (Trafton 2003) | The manipulation was a **warning** before the interruption. Sample size was not confirmed: the abstract was seen only in search snippets, and the PDF is an unextractable scan. | CLM-RS-INTERRUPTION is partial-access and worded as "a warning that allows preparation was associated with faster resumption". |
| 2026 unguided digital trial, 307 participants | Baumeister et al. 2026 (n=307). The primary outcome was quality of life, not symptoms. Open-label, exploratory alpha, low adherence. | Not cited as evidence of symptom reduction. |
| 2026 CBT meta-analysis, 14 RCTs | Liu et al. 2026. The abstract gives no total N or confidence intervals. Quality of life and self-evaluation did not improve significantly. | Partial-access. Null outcomes are kept in the wording. |
| NICE NG87 "reviewed July 2026" | Last reviewed 23 July 2026, with no change to the adapted recommendations. Published 14 March 2018, last updated 13 September 2019. | Dates recorded on SRC-GD-02. |
| NICE "environmental modifications" | These are defined under "Terms used in this guideline", not in one numbered recommendation. Recommendations 1.4.3, 1.4.12, 1.5.13 and 1.5.15 refer to them. | Locator recorded on CLM-GD-NICE-ENV. |
| NHS: online tests cannot diagnose ADHD | The NHS adult page does not say this. It links to a self-screening tool. | CLM-GD-NHS-ONLINE-TEST is **unverified** and is not asserted. The skills instead say that a chat conversation is not the specialist assessment NICE describes (CLM-GD-NHS-DIAGNOSIS). |
| AADPA CBT recommendation grade | The recommendations block came back empty. The page shows no date or version. | Partial-access. |
| Dopamine and body-doubling mechanism | None of the sources read tested or established a neurochemical mechanism. Consumer pages that mention dopamine present it as speculation or attribute it to a commercial service. | CLM-BD-MECHANISM. The search was targeted, not systematic. |

None of the report's 2026 citations were found to be fabricated. Every one that was searched for was located, though several have caveats.

## Decision: urgent-help guidance is generic (2026-10-19)

The product owner decided that the suite must work for someone anywhere in the world. It therefore gives **no phone numbers, named helplines, directories or national services**, and never asks for the user's country.

`crisis-resources.md` now holds generic guidance on finding help locally:
- local emergency services or the nearest emergency department;
- a crisis line where the user lives, found by searching for "crisis line" with their country's name;
- a doctor or urgent care service;
- someone they trust.

Consequences:
- The UK and US numbers that were verified earlier (SRC-GD-11 to SRC-GD-15) remain in the register only as a record of what was checked. They are not used at runtime.
- CLM-GD-MPH-OVERDOSE and CLM-GD-MPH-URGENT were reworded to "urgent medical advice" and "emergency help" in place of the NHS's UK-specific routes. The meaning is unchanged.
- `scripts/validate.py` fails any shipped text that contains a support-service number, a named helpline or directory, or a phone-number pattern.

The generic wording still needs clinical review.

## Items left out of runtime claims

- CLM-GD-NHS-ONLINE-TEST (unverified).
- Effect sizes for any study read only as an abstract. These may be listed in the register, but runtime replies should not quote them.
- The report's numerical trial-size suggestions (for example "60–100 users", "12 sessions"). These are planning hypotheses, not evidence. See `docs/evaluation-plan.md`.

## Review triggers

| Trigger | Action |
|---|---|
| A cited page's "next review due" date passes. The NHS urgent-help page was already overdue on the access date. | Re-check the page and update the `published` field |
| NICE updates NG87, or CADDRA releases its next edition (previewed July 2026) | Re-check the guidance claims |
| A body-doubling RCT or AI-agent evaluation is published | Re-assess the CLM-BD-* claims |
| Before any public release | Clinical reviewer checks every claim used at runtime and sets `clinician_reviewed` |
| Someone challenges a claim | Mark it `disputed` until it is resolved |

Responsible role: an **evidence maintainer** for the register, a **clinical reviewer** for health claims, and a **privacy/legal reviewer** for governance claims. No one has been assigned to these roles yet.
