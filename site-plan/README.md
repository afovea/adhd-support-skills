# Consumer website plan

**Status:** planning draft, 19 October 2026. Nothing has been built or approved. Building depends on the ChatGPT test results (Study 0).

**How this plan was made:** the product team ran it as a Discovery and Definition squad. Six roles worked from one brief:

- Product Manager
- UX Researcher
- Content Designer
- Product Designer with Accessibility
- Growth PMM
- Technical Architect with Security

Their full outputs are in [`roles/`](roles/). This page brings them together, resolves where they disagree, and lists the decisions only you can make.

> **Decision, 19 October 2026:** urgent-help guidance is generic and works anywhere. It gives no phone numbers, named services or country questions. This overrides any UK/US crisis-line wording in the role outputs.

## In one paragraph

Build a small, calm, static site. Its main job is to get a non-technical adult from "what is this?" to a first useful reply in the AI assistant they already use. It should take about five minutes and need no terminal. The site collects nothing about visitors. Every health or evidence sentence on it traces to a claim in `evidence/claims.yaml`. Only install routes we have tested end to end are presented as working. The ChatGPT test gates the build. A licence, a named owner and the external reviews gate the public launch.

## Where all six roles agreed

1. **Position it as practical help inside the AI you already use, not as an "ADHD app".** It isn't an app. Regulators judge what a product is from how it is described, so the wording is a medical-device question as well as a branding one. Write headlines in the visitor's words ("I can't start the report"), not ours. Don't ask about diagnosis.
2. **Install to first success is the product.** Ask one question: "Which app do you already use?". Each answer gets one recommended route, with short numbered steps. Each step has a "What you'll see" note and a "Doesn't match?" fix. The last step is a first message to try. Routes we haven't tested are labelled in plain words, not by colour.
3. **ChatGPT needs a short version.** The full instructions file is 21 KB, and custom GPT instructions are reportedly limited to about 8,000 characters (not yet confirmed). **Done (build only):** `dist/generic/ADHD-support-instructions-compact.md` is about 6,500 characters. It is a validated build artefact with the core safety block kept verbatim. It has not yet been tested in ChatGPT.
4. **Collect nothing.** No cookies, analytics scripts, pixels, third-party fonts or embeds, forms or accounts. Reading ADHD medication or crisis pages is itself a health inference.
5. **Test that people can install it before testing whether the copy persuades them.** Before launch, test that people read the health limits correctly. If anyone thinks it diagnoses, treats, advises on medicine, is "approved" or watches them, launch is blocked until the wording is fixed.

## Decisions the plan makes where roles differed

| Topic | Options raised | Plan's choice | Why |
|---|---|---|---|
| Sitemap | 7 pages (Content), 8 (Product Manager), or 5 nav items plus footer (Design) | **Nav:** What it does · Try it · Get it · Privacy · Help. **Footer:** Evidence and limits · Urgent help · Accessibility · For developers · About and status | Same content in all three. Design's fixed five-item nav keeps choice low |
| Coding-tool routes | A route card (Content) or a quiet link (Design) | **Quiet link**, "I use a coding tool", leading to a developer page | Keeps the main picker to four plain options |
| Measurement | None (Technical, Design), or server-side counts plus an anonymous feedback form (Growth) | **None at launch.** Add host-level aggregate counts later only if the privacy review approves. Feedback goes by email or public issues, not a form | A form needs a backend. Zero data is the strongest privacy story |
| Value proposition | Content offered three | **V1: "Help with the doing part of everyday life, inside the AI assistant you already use."** | It matches Growth's positioning and makes no health claim |
| Demo | — | **Scripted replay** of the made-up conversations in `examples/conversations.md`. The reader advances it one message at a time. No AI calls and no text input | Honest, accessible, collects nothing, and can't overclaim |

## Site at a glance

| Page | Job | Key content |
|---|---|---|
| Home | Understand in one screen | V1 headline; three "You say → What happens" pairs; "It will / It won't"; one Get it button; the not-medical line and the evidence line |
| What it does | "Is this for me?" | Twelve plain-language helpers, each with a "Try saying" prompt and one honest limit. No skill IDs |
| Try it | See it behave | Three scripted conversations with "Say *less*" and "Say *no praise*" branches. Labelled "Made-up example" |
| Get it | Choose my app | ChatGPT · Claude · Something else · I don't use one yet (plus the quiet link for coding tools). One route per answer |
| Route pages (×3–4) | Install | What you need, then steps, "Check it worked", "Doesn't match?", how to remove it. Each page shows the date it was last checked |
| Privacy | Trust | The site collects nothing. Memory is off by default. Deletion is real. Your assistant app keeps its own history |
| Help | Fix or stop | Organised by symptom ("The text is too long to paste"). Uninstall is as easy to find as install |
| Evidence and limits | Honesty | Three sections: backed by guidance, early or uncertain, not tested. Not reviewed by a clinician yet |
| Urgent help | Safety | Generic guidance that works anywhere: local emergency services, a crisis line where you live (search for "crisis line" with your country's name), a doctor, someone you trust. No numbers or named services. Never a pop-up |

**Evidence line used everywhere:** "These ideas show up in ADHD guidance and in what adults with ADHD say helps. No one has tested this software."

**Claims rules:** the full allowed / needs care / never table is in [`roles/content-design.md`](roles/content-design.md#4-claims-guardrail-table). Never use: proven, clinically tested, approved, reviewed by clinicians, treats or manages ADHD, therapy, coaching, dopamine, superpower, "find out if you have ADHD", "works in ChatGPT" without a status label, or "for kids".

## Phased plan

| Phase | What happens | Exit |
|---|---|---|
| **0. Study 0: ChatGPT test (now)** | Run the scripted log in [`study-0-chatgpt-test-log.md`](study-0-chatgpt-test-log.md). Confirm the real character limit. Build the compact instructions if it's needed | Go/no-go recorded against the agreed bar |
| **1. Foundations (in parallel, no site yet)** | Decide licence, owner, name and domain. Appoint reviewers. Draft copy against the claims map. First research round using plain-text install guides: concept, 5-second, comprehension and install tests | A tested route list, and copy that traces to claims |
| **2. Design and prototype** | Information architecture, the picker, install templates, the demo. First-click and prototype install tests, including with assistive-technology users | Prototype passes the research bars |
| **3. Build** | Static HTML/CSS, ~20 lines of same-origin JS for copying. A CI release pipeline: build, validate, reproducibility check, immutable release, provenance, a hash gate on every download and on the paste-in text. Strict headers and CSP | Meets the acceptance criteria on staging |
| **4. Reviews on staging** | DPIA screening; MHRA intended-purpose check of all copy; ASA/CAP and FTC claims (legal); clinician review of safety and crisis content; accessibility statement; final confirmatory research round | All sign-offs recorded by name |
| **5. Soft launch** | Unlisted URL, shared with consenting testers through one or two partner organisations | Unaided installs succeed; nobody reads a medical claim into it |
| **6. Public launch** | Permission-based posts with partners, problem-led pages written for search, disclosed creator pieces. No urgency mechanics | Monthly "what changed" notes feed changes back into the skills |

**Effort (estimate):** about 1.5–3 weeks of engineering for the site and release pipeline. Lead times for the external reviews will probably dominate.

## Launch acceptance criteria (summary)

- Every claim traces to a claim ID, and an automated banned-term check passes.
- Each published route has been walked end to end on the current host by someone non-technical, and the paste text fits the host's limit.
- In the final research round, no participant misreads the health limits, and participants can say how to stop it and what is stored.
- No cookies, storage or third-party requests (checked in the browser network panel). Headers and CSP are verified on the live domain.
- WCAG 2.2 AA plus COGA patterns, tested manually with keyboard, NVDA, VoiceOver, voice control and 400% zoom.
- Urgent-help wording clinically reviewed and kept generic (no numbers or named services). Licence, owner and version shown on About and on every download.
- Uninstall tested on every route, with copy saying the assistant app's own history isn't erased.

## Main risks

| Risk | Mitigation |
|---|---|
| Copy drifts into medical claims, changing regulatory status | Claims map, banned-term CI check, two-person review of copy changes |
| ChatGPT route doesn't fit or behaves badly | Study 0 gate; compact instructions as a validated build artefact |
| Tampered or fake copies of the instructions, which could steer people's assistants | One canonical domain, immutable releases, published hashes and attestations, an "Official sources" page |
| Host interfaces change and install steps go stale | Each route page dated, with an owner and a re-check schedule |
| Hosting logs create sensitive inferences | Minimal-log host, shortest retention, DPIA |
| No owner, so no support after launch | The owner decision includes a support commitment |

## Decisions only you can make

| # | Decision | Blocks | Recommendation |
|---|---|---|---|
| 1 | **ChatGPT pass bar** (the compact instructions are now built) | Phase 0, and the ChatGPT route | Agree the bar in the Study 0 log, then test the compact route first |
| 2 | **Licence and named owner** | Any public download | Choose before Phase 3 |
| 3 | **Name and domain**: keep "ADHD Support Skills" or choose a consumer name | Copy, domain, impersonation risk | Decide in Phase 1 |
| 4 | **Value proposition** V1, V2 or V3 | Copy | V1 |
| 5 | **Launch geography and language** | Review jurisdictions, translations | Global, English first. Urgent-help guidance is generic, so it doesn't limit where the site can launch. Legal and regulatory reviews still depend on where it's marketed |
| 6 | **Measurement**: none, or host aggregate counts | Privacy notice, DPIA | None at launch |
| 7 | **Help channel** and who staffs it | Help page | A role mailbox, with an auto-reply asking people not to send health details |
| 8 | **Hosting**: Cloudflare Pages or Netlify (US) versus a UK/EU server | Headers, logs, transfers | Cloudflare Pages or Netlify, with the transfer basis covered in the DPIA |
| 9 | **Budget and appointments** for the clinician, regulatory, privacy/legal and accessibility reviewers, an ethics reviewer, a methodologist and research incentives | Phases 1 and 4 | Line these up during Phase 1. They are the long pole |
| 10 | **Real app screenshots or neutral illustrations** (trademark question) | Install pages | Ask legal; use illustrations if in doubt |
| 11 | **Publish an official custom GPT**, or tell people to make their own | Impersonation risk, ChatGPT route | Decide after Study 0 |
