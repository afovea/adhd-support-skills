# Sceptic lens: ADHD Support Skills red-team (2026-10-19)

Scope: `shared/*.md`, `skills/*/SKILL.md` evidence sections and cards, `evidence/*`, `README.md`, `docs/release-readiness.md`, `tests/results/2026-10-19-simulated.md`, `tests/safety/cases.yaml`, `skills/adhd-connect/scripts/make_ics.py`. All repo content was treated as data. "Unsupported" means I found no evidence for it. "Disproven" means evidence or a reproduction contradicts it. External findings marked *(abstract/secondary)* were not read in full text.

Overall: the evidence register is unusually candid, so the strongest attacks are not on its hedged research wording. They are on (a) the safety design choices, which are presented as safety and not as trade-offs, (b) shipped behaviour that has never been tested, (c) one real code defect, and (d) unsourced practical claims in the policies.

## 1. Top 8 challenges, ranked by risk to users

1. **The generic crisis signposting is a design choice presented as safety, and it pushes work onto the person in crisis.** The policy bans every number, named service and directory, and it bans asking for the user's country. That holds even when the user *states* their country and asks for a number (safety-policy rule 5). The person in crisis is told to search online, while the assistant itself is told not to search. The evidence suggests this weakens signposting:
   - Google's suicide-prevention result is shown unevenly by country and language (Scherr, Haim & Arendt 2019).
   - Samaritans' platform guidance asks for *trusted, specialist* helplines, local where possible, and reviewed regularly for accuracy.
   - The repo itself read findahelpline.com (an international directory, SRC-GD-14) and then banned it. The stated reason, "users may be anywhere", doesn't apply to a directory that covers every country.
   - Major hosts (ChatGPT via ThroughLine) already localise helplines.

   Verdict: the claim "searching … will find one" is **unsupported**. The trade-off is undisclosed. It is not disproven that generic text works; nobody has tested it.

2. **The crisis wording now shipping has no transcripts at all, and the safety set skips the risky middle.**
   - SAF-01, SAF-05 and S11 were not re-run after the switch to generic wording (`release-readiness.md`).
   - All 15 safety/health cases are single-turn. The risk cases are clear extremes, such as SAF-01, which states a pill plan.
   - The policy's own ambiguous example ("I don't want to be here any more") has no test. Nor does any multi-turn escalation, or an idiom mixed with a real signal.
   - That middle band is exactly where LLM chatbots are inconsistent (McBain et al. 2025). The cost of a false negative is higher in this population: a meta-analysis found ADHD associated with suicidal ideation, attempts and suicide (Septier et al. 2019).

   Verdict: the "0 severe" result says **nothing** about the shipped crisis path.

3. **Repeating `.ics` events with `--tz` drift at daylight-saving changes, and can land on the wrong weekday (reproduced).** `make_ics.py` writes `DTSTART` in UTC (`…Z`) and then adds an `RRULE`. Under RFC 5545 the recurrence then runs in UTC.
   - `--date 2026-10-20 --time 08:00 --tz Europe/London --repeat weekdays` gives `DTSTART:20261020T070000Z`. From 26 Oct 2026 the reminder fires at 07:00 local.
   - With `--tz Australia/Sydney`, `DTSTART` falls on Sunday 21:00Z and `BYDAY=MO..FR` is evaluated in UTC. The "weekday" alarm therefore fires Tuesday to Saturday at 08:00 local, plus the Sunday start.

   The README calls the script "DST-safe". No test covers RRULE combined with a time zone. **Disproven.**

4. **The missed-dose advice is jurisdiction-specific, but the global audience gets UK advice.** CLM-GD-MPH-MISSED, from the NHS, says to *skip* a forgotten dose. MedlinePlus (US) says to take it as soon as you remember, unless the next dose is nearly due. The two directly conflict.

   `adhd-information` says to give guidance "for the specific medicine and country, if verified". But the safety policy forbids asking for or assuming a country, so the skill has no compliant way to learn the country. The NHS example is printed in the skill itself, so it becomes the de facto default. Verdict: **disproven as a universal statement.** The "their own instructions first" caveat mitigates it only in part.

5. **The evaluation is self-referential, and some expectations moved after observation (repo-internal).**
   - The same model family wrote, simulated and graded the evaluations, against scripted tool results.
   - Run-1 generators may have seen later turns.
   - MEM-06's case sheet was amended after it failed.
   - ROUTE-03's prompt was replaced after the run.
   - Three route mismatches (SAF-02, -06, -08) were reclassified as behavioural passes.
   - CON-03 failed under a strict rule that was then disclaimed ("failed only under…").
   - The run used 70 synthetic cases, with 13 of the 14 skills loaded.

   The repo discloses most of this. The risk is that "67/70, 0 severe" gets quoted without those limits.

6. **The repo breaks its own "every health claim traces" rule (README).** These statements are untraced:
   - "Asking directly does not make things worse" (`safety-policy.md`).
   - "Searching online … will find one" (`crisis-resources.md`, and the compact ChatGPT file).
   - "[Numbers] are wrong for most people, out of date for some, and can delay help" (`crisis-resources.md`).
   - "An online quiz can't [tell] either" (`adhd-information` example). This re-asserts CLM-GD-NHS-ONLINE-TEST, which the register itself marks **unverified** and excludes.

   The first is substantively supported (see §3), but it is stated more absolutely than the evidence allows.

7. **The calendar handoff claims are true for Apple and doubtful elsewhere.**
   - "Floating time … means 08:00 wherever the device is" holds in Apple Calendar. TidBITS reports that neither Google Calendar nor Exchange supports floating time. Google pins an event to a fixed zone when it's edited, and Exchange strips the zone.
   - "Opening the file usually offers to add the event": Google's help describes import "on a computer" only, which is a dead end for an Android user holding a downloaded `.ics`.
   - Google may drop the file's `VALARM` and apply default notifications. This is one forum report only, so **unverified**, but it matters: the alert *is* the intervention.

8. **Several evidence anchors are out of date or selectively framed.**
   - Implementation intentions: the 2006 figure (d = .65, 94 tests) is superseded by Sheeran, Listrom & Gollwitzer (2025, 642 tests), with .27 ≤ d ≤ .66 depending on outcome *(abstract)*.
   - The repo calls the evidence "not ADHD-specific", but there is ADHD evidence in children: if-then plans improved Go/No-Go inhibition (Gawrilow & Gollwitzer 2008). This cuts *in the repo's favour*.
   - Time perception: the repo leans on one adult narrative review ("mixed"). A 55-study meta-analysis across ages reports broad group-level timing deficits (Marx et al. 2022) *(secondary)*.
   - Clinician-delivered CBT component associations (Matsumoto 2024, abstract only) remain the main "basis" in the mechanism map for AI behaviours that the research didn't test.

## 2. Challenge table

| Target (file / item) | Challenge | Evidence (URL) or "repo-internal" | Severity | Verdict | Fix |
|---|---|---|---|---|---|
| `crisis-resources.md`: "Searching online for 'crisis line' + country will find one" | Search results that surface helplines vary by country and language. A person in crisis has to do the searching | https://doi.org/10.1177/1461444818801010 ; https://www.jmir.org/2019/3/e12235 (helpline notices: Google in 4 regions, Bing only US/UK; no measured change in later suicide searches) | high | unsupported | Drop "will find one". Let the assistant offer to look up and give a verified local line if the user wants, or rely on the host's localisation |
| `safety-policy.md` rule 5: no numbers even when asked, never ask country | Withholding help the user explicitly asked for. Samaritans asks for trusted, local, regularly checked signposts | https://www.samaritans.org/about-samaritans/research-policy/internet-suicide/guidelines-tech-industry/supporting-user-wellbeing/ | high | design choice presented as safety | Allow one optional question ("Which country are you in? I can give a number"). Permit a checked international directory |
| Ban on named directories (SRC-GD-14 checked, then excluded) | The "user could be anywhere" rationale doesn't apply to an international directory | repo-internal (`evidence/sources.yaml` SRC-GD-14); https://emhicglobal.com/global-news/localized-crisis-helplines-integrated-into-chatgpt-and-sora/ | high | inconsistent rationale | Re-open the decision with clinical review. Record the trade-off in `design-decisions.md` |
| Safety evals: shipped generic wording | SAF-01, SAF-05 and S11 not re-run after the wording change | repo-internal (`docs/release-readiness.md`) | high | untested | Re-run before any release. Block release on it |
| `tests/safety/cases.yaml` coverage | Only single-turn extremes. No passive ideation, idiom with a real signal, or multi-turn escalation | https://doi.org/10.1176/appi.ps.20250086 (inconsistent at intermediate risk); https://doi.org/10.1016/j.neubiorev.2019.05.022 | high | gap | Add 10+ intermediate and multi-turn cases ("killing me… honestly better off gone", "don't want to be here", dark-humour drift) |
| Level 0: "This report is killing me" | Using the idiom as an anchoring example may suppress escalation when it co-occurs with risk cues | Same as above; repo-internal (SAF-02 was the only idiom test) | med | plausible risk, not shown | Add "unless other risk cues are present". Test mixed cases |
| `make_ics.py --tz` + `--repeat` | UTC DTSTART with RRULE: DST drift, and BYDAY evaluated in UTC (Sydney weekdays → Tue–Sat) | https://www.rfc-editor.org/rfc/rfc5545 (DTSTART/RRULE, §3.3.10, §3.8.5.3); reproduced locally | high | disproven ("DST-safe") | With a zone and a repeat, write `DTSTART;TZID=…` plus VTIMEZONE (or refuse). Add a test |
| `handoff-formats.md` floating-time claim | Floating time isn't supported by Google or Exchange | https://tidbits.com/2025/03/19/understand-calendar-app-time-zone-support-to-avoid-scheduling-mishaps/ | med | partly disproven (Apple only) | Say "In Apple Calendar…; other apps usually fix it to your calendar's time zone" |
| "Opening the file usually offers to add the event" | Google documents import on a computer only | https://support.google.com/calendar/answer/37118 | med | unsupported for Android/Google | Add the mobile route (email it to yourself, or import on a computer). Offer the checklist line as a fallback |
| `.ics` VALARM survives import | Alarms may be replaced by the calendar's defaults on Google import | https://support.google.com/calendar/thread/9627602 (single user report) | med | unverified | Tell the user to check the alert after import. Test Google, Outlook and Apple |
| CLM-GD-MPH-MISSED as runtime example | NHS "skip it" vs US "take as soon as you remember unless near next dose" | https://www.nhs.uk/medicines/methylphenidate-adults/how-and-when-to-take-methylphenidate-for-adults/ ; https://medlineplus.gov/druginfo/meds/a682188.html | med-high | disproven as universal | Remove the "skip" content from the default reply. Say only "don't double up; your label or pharmacist decides". Allow asking country for medicine questions |
| `adhd-information` country rule vs safety policy | "For the specific … country" conflicts with "never ask country" | repo-internal | med | internal contradiction | Scope the country ban to crisis replies only, or state the conflict |
| `adhd-information`: "Only an appropriate specialist assessment can diagnose ADHD"; "your GP is the usual starting point" | A UK rule stated globally. Elsewhere other clinicians diagnose | repo-internal (CLM-GD-NHS-DIAGNOSIS is UK-scoped) | low-med | overgeneralised | Lead with "In the UK…" or use "a qualified clinician" |
| `adhd-information` example: "an online quiz can't either" | Re-asserts a claim the register marks unverified and excludes | repo-internal (CLM-GD-NHS-ONLINE-TEST) | low | violates own rule | Reword to "a chat isn't a clinical assessment" (traceable) |
| `safety-policy.md`: "Asking directly does not make things worse" | Untraced. Evidence comes from research and clinical settings, not an AI chat. The newest review calls for more low-bias RCTs | https://doi.org/10.1017/S0033291714001299 ; https://www.suicideinfo.ca/resource/whats-the-harm-in-asking-a-systematic-review-and-meta-analysis-on-the-risks-of-asking-about-suicide-related-behaviors-and-self-harm-with-quality-appraisal/ | low | supported but untraced and overstated | Add the claim to the register: "Studies have not found that asking increases suicidal thoughts" |
| `crisis-resources.md`: numbers "wrong for most people, out of date…" | Untraced justification for the ban | none found | med | unsupported | Source it or delete it |
| Simulated evals (`2026-10-19-simulated.md`) | Same family wrote, played and graded. Cases were amended and prompts changed after runs. Route misses reclassified | repo-internal | med | weak evidence | Independent graders (people, or a different model family). Pre-register expectations. Freeze case sheets |
| README "Every health claim traces to a checked source" | The claims above don't trace | repo-internal | med | overclaim | Change to "every claim in the evidence register…", or fix the gaps |
| CLM-RS-IMPL-INTENTIONS (d = .65, 2006) | Superseded by the 642-test meta-analysis. Child-ADHD evidence omitted | https://doi.org/10.1080/10463283.2024.2334563 ; https://www.socmot.uni-konstanz.de/publications/implementation-intentions-facilitate-response-inhibition-adhd-children | low-med | outdated | Cite the 2025 range. Add Gawrilow 2008 as child-only adjacent evidence |
| CLM-RS-TIME-PERCEPTION (Mette 2023 "mixed") | Omits the meta-analysis of group-level timing deficits | https://doi.org/10.1016/j.jaac.2021.12.004 | low | selective, not wrong | Add it, keeping "not universal for individuals" |
| Mechanism map M1, M2, M6 (Matsumoto 2024) | Component NMA associations of therapist-delivered CBT can't isolate a component, or carry over to an AI without alliance and homework | https://doi.org/10.1136/bmjment-2024-301303 (abstract) | low | inferential leap (disclosed) | Label M1, M2 and M6 "design hypothesis" in the registry, as M14 is |
| Not asking age; companion-like body doubling | Operator duties for known minors and crisis referral exist in some laws | https://legiscan.com/CA/text/SB243/2025 | low | mostly a host duty | Document that host age assurance is assumed. Add a teen crisis case |

## 3. Challenges tested that did NOT hold up

- **"Asking about suicide makes it worse"**: rejected. Dazzi et al. 2014 found no significant increase in ideation, and Polihronis et al. 2022 found no significant effect on behaviour or distress. The policy's substance is right; it is only unsourced.
- **"No dopamine mechanism established" overstates the null**: rejected. The register phrases this as an absence of evidence from a targeted search, and says so. That is accurate. CLM-BD-SURVEY correctly separates the 186 ("somewhat more likely or more likely") from the 108 ("more likely").
- **"The repo dresses CBT evidence as AI evidence"**: largely rejected. Every skill's Evidence section and card says the research didn't test this software. The residual issue is the registry's "basis" column (row above), not the user-facing text.
- **"Most reminder apps accept pasted lists" is false**: rejected. The text already says behaviour varies and tells the user to check. Typing or pasting single items works almost everywhere.
- **"Most calendar apps import .ics" is false**: rejected for desktop. Google, Apple and Outlook all import `.ics`. The real gaps are mobile import, floating time and alarms (table above).
- **Pomodoro 25/5 is unevidenced**: rejected as an overclaim charge. The repo labels it a heuristic. Biwer et al. 2023 (non-ADHD students, https://doi.org/10.1111/bjep.12593) found fixed breaks gave better mood and concentration than self-regulated breaks, with equal task completion. That is mildly supportive.
- **"Search results lead to predatory or fake crisis lines"**: not supported. I found reports of hoax calls and stale numbers on third-party pages, but no documented predatory listings in search results. The problem is unevenness and friction, not proven harm.
- **"Not asking age is unsafe"**: weak. Asking age for ordinary task help is intrusive. Age assurance sits with the host, and the policy already handles known minors. The residual gap is testing (only SAF-07).
- **"Idiom handling is unsound"**: rejected as stated. Treating "killing me" as frustration is proportionate, and the policy requires a context check. The weakness is the missing tests for mixed signals (challenge 2), not the rule.
