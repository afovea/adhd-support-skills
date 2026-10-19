# Product framing: ADHD Support Skills consumer website

Workstream: product framing. Planning draft, 2026-10-19. Sources: the site brief, `README.md`, `INSTALL.md`, `docs/release-readiness.md`, `docs/capability-matrix.md`, `docs/privacy-and-retention.md`, `docs/evaluation-plan.md`.

## Top 3 recommendations

1. **Agree the ChatGPT go/no-go bar before anyone runs the test, and build nothing until it is met.** Include "the instructions fit and work within ChatGPT's real limits". The full file is 21 KB, and a custom GPT allows about 8,000 characters (unconfirmed).
2. **Make the MVP an install-to-first-success site, not a brochure.** Success means a non-technical adult picks their app, sets it up without a terminal, and gets one useful reply. Everything else is secondary.
3. **Collect nothing by default, and measure through consented usability sessions.** The only other measure is cookieless aggregate counts, approved by the privacy reviewer. Every claim on the site must trace to `evidence/claims.yaml`, and the regulatory reviewer must sign off the intended-purpose wording before launch.

## Problem statement

Adults who struggle with the *doing* side of everyday tasks already use general AI assistants. They have no simple, trustworthy way to:
- find out whether this suite would help them;
- set it up without technical skills;
- understand what it will and won't do with their data.

Today the only route in is a developer repository with terminal commands. As a result, the people most likely to benefit are the least able to get started. They also have no safe, bounded explanation that avoids hype, shame or medical claims.

**Evidence and confidence.** The problem is inferred from the product owner's ask and the install docs, which say non-technical people will mostly paste instructions or use desktop plugins. It has not been validated with users (no usability research has been run). **Confidence: low to medium.**

## Target audiences

| Priority | Audience | What they need from the site |
|---|---|---|
| **Primary** | Adults (18+) who find starting, prioritising or switching tasks hard, already use ChatGPT or Claude apps, and are non-technical. Diagnosis is not required and not asked. | Plain explanation, a quick "is this for me?" check, a no-terminal setup, a first thing to say |
| Secondary | Supporters: partners, coaches, peer-support groups, workplace neurodiversity networks who recommend tools | Something trustworthy to share; clear limits and privacy |
| Secondary | Technical users (Claude Code, Codex) | A short pointer to the repo and `INSTALL.md`, not a separate site journey |
| Out of scope | Children and teens; parents buying for children; clinicians prescribing tools | Needs a separate review (see non-goals) |

Assumption: most primary users will arrive on mobile, from a recommendation, and then set up on a desktop or in an app. **Unknown**; to be tested in discovery.

## Jobs the site must do

| Job | The visitor's question | The site succeeds when they… |
|---|---|---|
| Understand | "What is this, in one breath?" | can say what it does in their own words after one screen |
| Decide | "Is it for me, and is it safe?" | know it needs no diagnosis, isn't medical, collects nothing, and that they can stop it at any time |
| Install | "How do I set it up in *my* app?" | choose their app in one click and finish setup with no terminal |
| First success | "Did it work?" | send a starter phrase (for example "I can't start the report") and recognise a correct reply |
| Get help or stop | "It's not working / I don't want this" | fix the common problem, or remove it and know what the host app still keeps |

## Outcomes and success measures

Outcome: more of the primary audience reach a first useful reply safely, and nobody is misled about what the product is.

| Measure | How it is collected (privacy-compatible) | Target (assumption; to be set after discovery) |
|---|---|---|
| Setup completion without help | Moderated usability sessions, with consent and no recording unless agreed | At least 4 of 5 participants per route |
| Time to first useful reply | Same sessions, timed | Median of 5 minutes or less (assumption) |
| Comprehension of limits | In-session questions: "Is this medical advice?", "What does it store?" | At least 4 of 5 answer correctly |
| Trust and pressure | Short post-session rating: felt calm, not pushed | No participant reports feeling pressured or shamed |
| Route demand | Cookieless, aggregate download or copy counts per route, with no IP retention (if the privacy review approves) | Directional only, never a target |
| Problem signals | Categorised help requests through a no-account channel (for example a public issue form or email), counted by category | Top issue categories fall after each content fix |
| Safety | Count of claims on the site not traceable to `claims.yaml` | Zero at launch and every release |

Not measured: page views, time on page, scroll depth, return visits, sign-ups, social shares. These are vanity metrics, and on ADHD content they imply sensitive inferences.

## MVP scope: sitemap (8 pages)

| # | Page | Purpose | Job |
|---|---|---|---|
| 1 | Home | One-line promise, three concrete examples, "Get started" | Understand |
| 2 | What it helps with | The everyday problems it helps with, in plain words, with short sample exchanges from `examples/conversations.md`, plus what it won't do | Understand, Decide |
| 3 | Is it for me? | Fit check: no diagnosis needed, adults, which apps, what it isn't | Decide |
| 4 | Get started | "Which app do you use?", then one route each: ChatGPT, Claude app, other assistant. Technical users get a link to the repo | Install |
| 5 | Your first try | Three starter phrases, what a good reply looks like, and the controls ("quiet", "pause", "stop", "less", "no praise") | First success |
| 6 | Privacy and safety | Collects nothing; memory off by default; what the host app keeps; not a medical device; crisis resources (verified UK and US, plus location-neutral guidance) | Decide |
| 7 | Help, update and remove | Top problems, how to stop or remove it, who to contact | Get help or stop |
| 8 | About and evidence | Owner, licence, version, what the evidence does and does not show, review status stated honestly | Decide |

**Later, only if evidence justifies it:**
- per-skill pages;
- video walkthroughs;
- translations;
- non-UK/US crisis coverage;
- a supporter or "share this" kit;
- a claude.ai upload route (once tested);
- a Codex or ChatGPT desktop plugin route (once tested).

## Non-goals

- No accounts, newsletter, cookies, analytics tracking, chat widget or embedded assistant on the site.
- No medical, diagnostic, treatment or effectiveness claims. No "clinically", "proven" or "dopamine" language. No "superpower" framing.
- No child or teen marketing, and no school or parent channel.
- No testimonials or user stories until there is a consented, reviewed process for them.
- No hosting of research PDFs or source reports (they are not redistributable).
- No routes the team hasn't tested published as working. Untested routes are either hidden or labelled "untested".

## Dependencies and gates

| Gate | Blocks | Owner |
|---|---|---|
| **G1 ChatGPT test results meet the agreed bar.** The bar covers: the instructions fit within ChatGPT's limits (a ChatGPT-sized instruction set may be needed); routing works; controls work; no release-blocking failures. | **Go/no-go for the whole build** | Product owner (PO) |
| G2 Licence chosen and owner named (currently `OWNER-TO-BE-CONFIRMED`) | Publishing any download or copy-paste file | PO |
| G3 Regulatory review of intended purpose and site claims | Public launch | Regulatory reviewer (not yet appointed) |
| G4 Privacy review: data-protection screening of the site, hosting logs and help channel | Public launch, and any counting | Privacy/legal reviewer |
| G5 Clinical review of runtime claims and crisis resources | Evidence and safety pages | Clinical reviewer |
| G6 Accessibility review (screen reader, voice, cognitive) | Public launch | Accessibility reviewer |
| D1 Each published install route verified end-to-end on a real host | That route's page | Engineering |
| D2 Each site claim mapped to a claim ID in `claims.yaml` | Copy sign-off | Content and evidence lead |

## Phased plan

| Phase | Work | Exit |
|---|---|---|
| 0. Gate | Define the ChatGPT pass bar; run the tests; decide go/no-go | G1 decision recorded |
| 1. Discovery | Run 5–8 interviews or route walk-throughs with primary-audience adults; confirm which apps they use; record the real ChatGPT limits | Prioritised route list and confirmed audience |
| 2. Content and routes | Write copy to the claims map; design the "pick your app" flow; prototype the 8 pages | Copy traced to claims, and the prototype tested with 5 users |
| 3. Build | Static site: no cookies, no third-party scripts, reduced-motion safe | Meets acceptance criteria in staging |
| 4. Review | G2–G6 run in parallel on the staging site | All sign-offs recorded |
| 5. Soft launch | Unlisted URL shared with supporter groups; help channel open | No severe issues for 2 weeks (assumption) |
| 6. Launch | Public URL; release notes | — |

**MVP launch acceptance criteria**
- G1–G6 and D1–D2 are closed, each with a named sign-off.
- Every claim traces to a claim ID. No banned terms appear (an automated check is run).
- At least 4 of 5 usability participants complete setup and first try on each published route without help.
- At least 4 of 5 correctly state that it is not medical advice and that the site and suite collect nothing.
- The site sets no cookies and loads no third-party trackers (verified with browser dev tools). Hosting logs follow the privacy reviewer's retention rule.
- WCAG 2.2 AA is met, plus the cognitive checks: one main action per page, short paragraphs, no autoplay, and respect for reduced-motion settings.
- Crisis resources are re-verified within 30 days of launch. Licence, owner and version are visible on About and on every download.
- Remove and stop instructions are tested on every published route.

## Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Site copy implies a medical purpose, which would make the product a medical device | High: regulatory exposure | Claims map, banned-term check, regulatory sign-off (G3) |
| The ChatGPT route doesn't fit or degrades badly in practice | High: the primary route fails | The G1 bar includes fit; a trimmed instruction set is a product dependency, not a site fix |
| Hosting or CDN logs create sensitive inferences | Medium–high | Static hosting with minimal logs, a short retention period, and G4 review |
| Users expect real timers or reminders | Medium: disappointment, loss of trust | Say plainly on page 5 what the app can and cannot do |
| Host apps change their UI or limits, so instructions go stale | Medium | Date-stamp each route, review it each release, and assign a route owner |
| Untested routes are presented as working | Medium | Publish only verified routes (D1) |
| No owner means no-one fixes problems after launch | High | G2 includes a support commitment |

## Open decisions for the product owner

1. What exactly is the ChatGPT test, and what pass bar decides go or no-go? (Not yet defined.)
2. Who is the named owner, and which licence will you use?
3. Does the site launch UK-only, or UK and US? This affects the crisis resources and the review jurisdictions.
4. Is any counting acceptable at all, or is it strictly zero (usability research only)?
5. Which help channel will you use? It must work without an account if possible, and someone must staff it.
6. Will the site have its own name and domain, or sit under the repository's? (Unknown.)
7. Is there a budget for the clinical, regulatory, privacy and accessibility reviewers? Currently none is appointed.
