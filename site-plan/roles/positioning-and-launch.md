# Growth: positioning and launch for the consumer site

Role: Growth Product Marketing Manager. Planning only; nothing here is built or approved.

## Top 3 recommendations

1. **Position it as "practical help inside the AI you already use", not an "ADHD app".** Lead with plain problems ("I can't start", "I lost my place") rather than diagnosis. Every claim must trace to `evidence/claims.yaml`.
2. **Grow only through permission.** That means charity and community partnerships, disclosed creator partnerships and honest-intent SEO. No paid targeting, no pixels, no retargeting.
3. **Gate the public launch.** It waits on the ChatGPT test results, a licence and owner, and legal, privacy and regulatory review. Soft-launch with recruited testers first. Measure with aggregate server-side counts plus opt-in feedback tagged to a specific skill.

## Assumptions (labelled)

- A1. The product stays free. There's no ad budget and no revenue goal. Success means people who'd benefit install it and keep it. *Unconfirmed.*
- A2. The site launches in English for UK and US adults first. This matches the verified crisis resources.
- A3. Most visitors will use the paste-in instructions or a desktop-app plugin, not a terminal (brief).
- A4. The product has no telemetry (`docs/privacy-and-retention.md`). So the site can never see what happens inside someone's assistant.

## 1. Positioning

**Category frame:** "Practical help with the doing side of everyday tasks, inside the AI assistant you already use."

Why not "ADHD app":

| Reason | Detail |
|---|---|
| It isn't an app | No account, no new place to check, no data sent to us. It's a set of instructions the assistant follows. Calling it an app sets wrong expectations about reminders, sync and notifications. |
| Regulatory status follows the words | MHRA: intended purpose comes from what the maker says. "ADHD app" or "manage your ADHD" moves towards a medical purpose. "Help getting started on the report" doesn't. A disclaimer doesn't fix overclaiming. |
| It works without a label | It needs no diagnosis or disclosure. Problem-led copy lets people in without asking them to identify. That matters for people who are waiting for assessment, unsure, or private. |
| Lower switching cost | "Add to what you already use" is one step. Choice overload and new-tool fatigue are real for this audience (brief: tone). |

**Positioning statement (draft):** For adults who already use an AI assistant and find starting, choosing, or getting back on track hard, ADHD Support Skills adds calm, practical help to that assistant. It's free and quiet. You stay in control ("stop", "less", "no praise"). It won't watch you, diagnose you, or pretend to set reminders it can't.

**Message hierarchy:**
1. What it helps with: get it out of your head, pick what's next, start, get back after interruption.
2. How it behaves: quiet, honest, you're in control, no streaks or shame.
3. How to add it: pick your assistant, then follow one route.
4. Limits, shown on the same page: not medical, not clinically tested, memory off by default, cannot erase the host's history.

**Proof we can use:** behaviour (the controls, and the "won't" list), demo conversations adapted from `examples/conversations.md`, and bounded evidence lines such as CLM-GD-CADDRA-SCAFFOLD ("consistent with guidance", never "proven"). **Proof we can't use:** "clinically reviewed", effectiveness claims, user numbers, testimonials before we have them, or anything about dopamine (CLM-BD-MECHANISM).

## 2. How it differs (fairly, no competitors named)

| Alternative | What it does well (be honest) | Where this suite differs |
|---|---|---|
| To-do and reminder apps | Store lists durably. Reminders really fire. They sync across devices. | Helps with choosing and starting, not storage. It won't fake a reminder or timer, so if your assistant can't set one, it says so. **It complements a to-do app rather than replacing it.** |
| Coaching apps and human ADHD coaching | A human relationship, accountability over time, sometimes credentialed people. | No human, no programme, not coaching. It's in-the-moment help, available whenever your assistant is. We shouldn't imply it substitutes for a coach or for clinical care. |
| Body-doubling services (human sessions) | Real people present. Some ADHD organisations run them (CLM-BD-PRACTICE). | It offers quiet AI company as one option. No study has evaluated an autonomous AI body double (CLM-BD-NO-AI), and the evidence on body doubling is early (CLM-BD-EARLY). Say "some people like company while they work", nothing stronger. |

Rule: name no competitor. Never claim to be "better than" or "instead of" another option.

## 3. Audience segments and entry points

| Segment | What they're likely to search for or ask | Entry point on the site |
|---|---|---|
| S1. Adults with an ADHD diagnosis who already use ChatGPT or Claude | "ADHD prompts ChatGPT", "help starting tasks ADHD" | Problem pages (start, overwhelm, interruptions), then the install chooser |
| S2. Adults waiting for assessment or self-identifying | "can't start tasks", "always losing my place" | The same problem pages; no diagnosis asked. Link to NHS assessment information (CLM-GD-NHS-DIAGNOSIS). Never imply the tool is a substitute. |
| S3. People who struggle with starting but don't identify with ADHD | "how to start when overwhelmed" | Problem pages, with ADHD mentioned as context, not as a gate |
| S4. Supporters (partners, workplace neurodiversity networks, coaches) | "tools to suggest to someone with ADHD" | A "Share this" page written for adults to choose for themselves. No covert installs or monitoring framing. |
| Excluded for v0.1 | Children and parents choosing for children | No child-specific marketing (brief). Clinicians as a channel wait until clinical review. |

Activation moment (hypothesis): the visitor pastes or installs it, asks one real request, and gets one small next step. The site should get people there in one route with one choice: "Which assistant do you use?"

## 4. Ethical acquisition channels

| Channel | How to do it right | Never |
|---|---|---|
| ADHD charities and organisations | Approach through their partnerships contact. Offer a free resource they can review first. Accept that they may say no or ask for changes. Credit them only with written agreement. | Imply endorsement, use logos without permission, or ask them to make claims we can't. |
| Community spaces (forums, subreddits, Discord servers, peer groups) | Ask the moderators first. Post once, transparently, as the maker. Answer questions and accept criticism. | Astroturf, use sock-puppet accounts, mass-post, DM members, or scrape member lists. |
| SEO for honest intent | Problem-led pages that are useful even without installing ("five ways to restart after an interruption"), plus clear install guides per assistant. Evidence pages state their limits. | Target "ADHD test", "ADHD cure" or medicine queries for acquisition. Write fear headlines or thin AI-generated pages. |
| Creator partnerships | Creators with lived experience try it first and say what didn't work too. Clear paid or gifted disclosure. We share the claims list and they don't go beyond it. | Scripted testimonials, "changed my life" claims, undisclosed gifting, or child-focused creators. |
| Paid ads | **Not recommended for v0.1.** Health-adjacent targeting conflicts with the guardrails, and platforms' own health-ad policies would need review. | Interest or "health condition" targeting, or lookalikes. |

## 5. Growth guardrails (specific to this audience)

- **No fear or urgency.** No countdowns, "limited spots", "you're falling behind" or loss framing. Urgency is a known pressure point here.
- **No "cure", "fix your ADHD", "superpower" or "hack your brain" language.** No pity framing either.
- **No targeting or segmentation by inferred health status.** Reading ADHD content may itself be a health inference (CLM-GD-ICO-SPECIAL).
- **No retargeting pixels, third-party trackers, session recording or fingerprinting.** No social embeds that load trackers.
- **No dark patterns.** No email gate before install instructions. Unsubscribe in one click if a mailing list ever exists. No streaks, badges or "don't break the chain".
- **Accessible by default.** Short pages, one primary action per page, no autoplay or motion that's required to follow the page.
- **Claims gate.** Every product or evidence sentence on the site maps to a claim ID. A reviewer checks the copy against the list before each publish.

## 6. Privacy-light measurement plan

**Default: collect nothing about individuals.** Where counting is needed:

| What | How | Decision it informs |
|---|---|---|
| Page views per page, per day | Aggregate server-side counts. No cookies, no stored IPs, short raw-log retention (period to be set by the privacy reviewer) | Which problem pages and install guides people reach |
| Install-route interest | Count downloads of each ZIP and each "copy instructions" action as an aggregate counter with no identifier | Which routes to invest in. Whether the paste-in limit matters |
| Partner referral | A campaign tag on partner links (identifies the link, never the person) | Which partnerships are worth repeating |
| Did it help? | An optional, anonymous one-question form ("Did this help? Which part?"), plus tester interviews | Which skills to improve |

Cookieless analytics tools are an option if hosted in the UK or EU and configured without identifiers. That's still a privacy-review decision.

**What this can't tell you (say so in reports):**
- whether an install worked or the assistant followed the instructions;
- whether anyone used it a second time, so there's no retention or activation rate;
- who the visitors are (diagnosis, age, country beyond rough levels);
- unique people, since counts include repeat visits and bots;
- whether it helps anyone. Only research can answer that (`docs/evaluation-plan.md`), and the site must not imply otherwise.

## 7. Launch sequence

**Gate 0 (before anything is public):**
- The ChatGPT tests pass.
- Licence and owner are decided.
- Privacy/DPIA, regulatory (intended purpose) and legal copy reviews are done.
- The roughly 8,000-character custom GPT limit is confirmed, with a version that fits it.
- Crisis resources are re-verified.
- An accessibility pass is done.

**Phase 1, soft launch (unlisted site):**
- Recruit adult testers through one or two partner organisations, with informed consent. Cohort size and payment are to be set with a methodologist.
- Test the comprehension of the home page, the install success per route, and whether the "won't" list reads as reassuring or offputting.
- Exit criteria: testers can install unaided on their main route, and no tester reads a medical claim into the copy.

**Phase 2, public launch:**
- Coordinated, permissioned posts with partners.
- Publish the problem pages and install guides.
- Run a small number of disclosed creator pieces.
- No launch-day urgency mechanics.

**Phase 3, steady state:**
- Publish a monthly "what changed" note.
- Review the partners that are working.
- Refresh the SEO pages when the claims' review dates come up.

## 8. Feedback loop into the skills

1. **Capture.** Use the anonymous form, tester interviews and partner feedback. Warn people not to paste health details or transcripts. Accept redacted excerpts only if they choose to share them.
2. **Tag.** Tag each item to a skill (e.g. `start`, `body-double`), the router, or the install route.
3. **Act.** Change the `SKILL.md` or routing, then re-run the behavioural evals before release.
4. **Close the loop.** Publish a public changelog line: "You told us X, so we changed Y." That's the honest retention lever we have, with no tracking involved.

## Legal review needed (content not asserted here)

- **UK ASA/CAP:** rules on health claims, substantiation, and labelling of influencer and affiliate content.
- **US FTC:** endorsement and testimonial guidance (including disclosure for gifted or paid creators) and health-claim substantiation.
- Also: platform health-ad policies, MHRA intended purpose wording, and UK GDPR/PECR for any analytics or cookies.

## Open decisions for the product owner

- Who is the named owner and contact for partners? (None exists yet.)
- Will testers be paid, and how many will there be?
- Will there be a mailing list at all? (The recommendation is none at launch.)
- Is a US launch in scope at the same time as the UK?
- What domain and hosting will we use? (This affects log handling.)

## Risks

| Risk | Mitigation |
|---|---|
| Copy drifts into medical claims as the site grows | Claims gate and legal review per publish |
| Community backlash at being "marketed to" in safe spaces | Permission first, maker transparency, and posting once |
| Install fails on ChatGPT for non-technical users | Gate 0, plus route-level counts and tester exit criteria |
| A creator overclaims | Written brief with the claims list, plus the right to request edits |
| Aggregate counts are mistaken for "impact" | Every report includes the "what this can't tell you" list |
