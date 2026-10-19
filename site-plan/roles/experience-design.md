# Experience design: ADHD Support Skills consumer site

Lenses: product design + accessibility. Planning only; build depends on the ChatGPT test results.

## Top 3 recommendations

1. **One question, one route.** The host picker asks "Which app do you already use?" and every answer leads to exactly one recommended route. Terminal routes live on a separate "For developers" page. Untested routes say so in words.
2. **Install pages are short, numbered sections, each with "what you'll see" and "doesn't match?"**. They end in a scripted first try ("Type: I can't start my report"). Blocker: the paste route is the main consumer route, but the 21 KB file is longer than the reported ~8,000-character custom GPT limit. Don't ship that route until there's a short version that fits.
3. **A static, zero-tracking site with a scripted demo.** No AI calls, analytics, cookies, forms or accounts. The "Try it" demo replays the synthetic conversations in `examples/conversations.md` one message at a time, at the reader's pace. WCAG 2.2 AA is the floor, with W3C COGA patterns on top.

## Assumptions (unverified)

- A1. Visitors are adults who already use an AI assistant. Most will not use a terminal (this matches the brief).
- A2. Visitors arrive mostly from a shared link or a search, often on a phone, and may install later on a desktop.
- A3. The ChatGPT tests will decide which ChatGPT route (custom GPT, Project instructions or desktop plugin) is primary. Until then, every ChatGPT route is shown as "not yet tested".
- A4. Real screenshots of host apps are allowed. This needs legal/trademark sign-off, so it is still an open decision.

## Information architecture

Top navigation has 5 items in a fixed order on every page: **What it does · Try it · Install · Privacy · Help**.
The footer has: Evidence and limits · Urgent help · Accessibility statement · For developers · Project status (v0.1.0, unreleased, no reviews done yet).

| Page | Job | Notes |
|---|---|---|
| Home | Answer "what is it, is it for me, what next" in one screen | In-short box, 3 example requests, the "it won't" list, 2 buttons (Try it / Install) |
| What it does | The 13 skills in 5 plain groups | Get it out of your head · Start and keep going · Time and memory · Switching and restarting · Health information and appointments. Skill names are secondary |
| Try it | Scripted demo | See below |
| Install | Host picker → one route page per host | URL per host (`/install/chatgpt`), so a choice survives back/share with no storage |
| Privacy | Memory off by default, where data lives, real deletion, what the host keeps | Also states that the site collects nothing |
| Help | Organised by symptom, plus uninstall per host | Linked from every install step |
| Evidence and limits | Bounded claims, each traced to `evidence/claims.yaml` | Not medical, not clinically validated, body-doubling evidence is preliminary |
| Urgent help | Verified UK/US resources and location-neutral guidance | One link in the footer and in the header on mobile. Never a pop-up |

## Key user flows

| Stage | Visitor's question | Design answer | Exit if it fails |
|---|---|---|---|
| Land | "What is this?" | H1 plus a 2-sentence in-short box: "Free instructions that make the AI assistant you already use better at helping you start, choose and finish everyday tasks." | Back. No interstitial or pop-up |
| Understand | "What would it actually do?" | 3 real request chips ("I can't start the report") with the shape of the reply in one line each | Try it |
| Is this for me? | "Do I need a diagnosis? Is it medical?" | A "No diagnosis or disclosure needed" line, plus "It won't" listed as prominently as "It will". Says it's for adults | Evidence and limits |
| Choose my app | "Which one do I do?" | Host picker (below) | "Not sure" → paste route |
| Install | "Am I doing this right?" | Step sections (below) | A "Doesn't match?" panel on every step |
| First try | "Did it work?" | Copyable test phrase plus a description of the expected reply | Help: "It doesn't seem different" |
| Stuck / uninstall | "Get me out" | Uninstall page per host, as easy to find as install, no guilt copy. Says the host's own history is not erased | None. The flow ends cleanly |

## Host picker (avoiding choice overload)

- One question: **"Which app do you already use?"** Show 4 large options, each with a text label (logos only if A4 is approved): ChatGPT · Claude (website or app) · Something else · I don't use one yet. Claude Code and Codex go behind a 5th quiet link, "I use a coding tool".
- Use native radio buttons inside a `<fieldset>` with a `<legend>`, then one "Show me how" button. Nothing changes until the button is pressed (WCAG 3.2.2).
- Each answer gives **one** recommended route. Alternatives sit in a collapsed "Other ways" `<details>`, never side by side.
- Status is shown in words, not colour: "Tested by us", "Not yet tested by us" or "Works, with limits" (for example, the lighter paste version).
- "I don't use one yet" leads to a plain page that says what an AI assistant is. It does not recommend any vendor.
- Put a "Compare all routes" table on its own page for people who like to see everything. Never put it in the main path.

## Install step pattern

- **One page per route, with each step as its own `<section>` and H2.** I chose this over one step per screen because it keeps the back button, find-in-page, printing and screen-reader heading navigation working, and nothing is lost on reload. Aim for at most 5 steps. If a route needs more, split it.
- **Progress:** use the text "Step 2 of 4" in each H2, plus an ordered list of step names at the top, used as links. Progress is never shown only as a bar. Optional "I've done this" checkboxes are not saved.
- **One action per step.** Lead with a verb: "Copy the instructions", "Open Settings", "Paste and save".
- **Copy block:** a read-only text box plus a "Copy instructions" button. The visible label matches the accessible name, so voice commands like "click Copy instructions" work. On success, the button text changes to "Copied" and a polite live region announces it, with no toast that disappears on a timer. Fallback: "Select all" for when the clipboard is blocked. Show the character count next to it, because some hosts have limits.
- **Screenshot `<figure>`:** crop it to the relevant area and add a highlight outline that doesn't rely on colour alone (a thick outline plus a numbered marker). The alt text says what to look for, for example "Settings panel; the box labelled Instructions is near the top." The caption gives the date it was taken. Screenshots must stay legible at 400% zoom. Wide ones get "Open full size" links.
- **"What you'll see" callout** after each action: one sentence describing the confirmation, such as "A message saying Saved appears."
- **"Doesn't match?" `<details>`** on every step, covering 2–3 known mismatches (the button has moved, the setting is missing because of the plan, the text is too long) with a fix or a way out. Every panel ends with a link to Help.
- **First try (final step):** "Type: *I can't start my report*." Expected result: "A short reply with one small first step, not a long list." If you get a long generic answer instead, a link explains why and what to do next.

## "Try it" demo (no AI, no data)

- Offer 3 situations, picked from the repo's synthetic set: overdue paperwork, can't start writing, too much at once. Don't add more. The full list is on a separate page.
- The reader moves through it with a "Show next message" button. There's no typing animation and nothing advances on its own. "Show whole conversation" reveals everything at once. New messages go into a list, focus stays on the button, and one polite live-region announcement reads out each new message.
- **Controls demo:** at fixed points, offer 2 buttons such as "Say *less*" or "Say *no praise*". Each switches to a pre-written branch, showing that the reader stays in control.
- A permanent label above it reads: "Example written by us. Not a real person. Real replies will vary by app." No free-text input, so nothing can be typed, sent or stored.
- Every conversation is also a plain HTML transcript, so it works without JavaScript and with print and screen readers.
- The demo copy uses the repo's examples verbatim or with documented edits, so it can't drift into overclaiming.

## Page templates

1. **Home:** H1, in-short box, 3 request chips, "It will / It won't" pair, 2 buttons, urgent-help link.
2. **Content page** (What it does, Privacy, Evidence): in-short box, H2 every ≤150 words, an "On this page" list, "Last checked" date.
3. **Install route:** title + status label, what you need (1–3 bullets, including any plan or account the host requires), step list, step sections, first try, uninstall link.
4. **Help article:** symptom as the H1 ("The text is too long to paste"), the most likely fix first, then other fixes, then "Still stuck?"
5. **Demo:** situation picker, conversation, controls, transcript link.

## Core components

These are built on native elements first (`<details>`, `<fieldset>`, `<figure>`, `<ol>`). No custom widgets where a native one exists.
In-short box · Header with skip link · Host option (radio card) · Status label (text) · Step section · Copy block · Screenshot figure · What-you'll-see callout · Doesn't-match disclosure · Request chip (static text, not a button) · Will/Won't list · Controls list ("quiet", "pause", "stop", "less", "no praise", "not that") · Demo message · Theme switch (Light / Dark / Match device, using a radio group) · Urgent-help link · Last-checked date.

## Cognitive and access requirements

The floor is **WCAG 2.2 AA**, with extra attention to 2.4.11 Focus Not Obscured, 2.5.7 Dragging (none used), 2.5.8 Target Size (we use 44 px), 3.2.6 Consistent Help and 3.3.7 Redundant Entry (no forms anyway).
**COGA** (Making Content Usable) adds: a clear purpose for each page, a summary first, familiar design, one idea per paragraph, no reliance on memory, and help that's easy to find.

- **Language:** plain UK English with short sentences. Define jargon at first use ("plugin", "custom instructions", "body double"). No idioms, no "superpower", no pity. Content and evidence leads review the copy.
- **Layout:** text 18 px or larger, line-height 1.5, line length ≤70ch, left-aligned and not justified, generous spacing. Headings are frequent and in a true H1→H2→H3 order. Keep sections short.
- **Motion:** the site has no animation by default. Even so, honour `prefers-reduced-motion` with no smooth scroll. No autoplay audio or video, no carousels, no parallax. Any video starts only when the user chooses, with captions and a transcript.
- **Interruptions:** no pop-ups, modals, cookie banners (none are needed because there are no cookies), newsletter prompts, chat widgets, countdowns or session timeouts.
- **Themes:** light and dark, following the device setting with a manual switch. Both meet 4.5:1 for text and 3:1 for UI and focus indicators. No information is carried by colour alone.
- **Keyboard:** everything is reachable in a logical order, with a visible 2 px+ focus ring that isn't hidden by sticky headers. There's a skip link and no keyboard traps.
- **Screen readers:** use landmarks, unique page titles ("Install for ChatGPT, step by step – ADHD Support Skills"), meaningful link text, and alt text on every screenshot.
- **Voice control:** visible labels match accessible names, and there are no icon-only buttons.
- **Zoom and reflow:** works at 320 CSS px wide (400% zoom) with no horizontal scroll except for code. Supports 1.4.12 text spacing. Mobile and desktop layouts have the same content.

## Anti-dark-pattern rules

- No accounts, email gates, newsletters or "notify me".
- No analytics, fingerprinting, third-party fonts or scripts, or embedded social widgets. ADHD reading behaviour is special-category data.
- No urgency, scarcity, countdowns, streaks or "come back" nudges.
- No invented testimonials, user counts, star ratings, or "clinically proven / approved / reviewed" claims.
- "It won't" is shown as prominently as "It will", and untested routes are always labelled.
- Uninstall is as easy to find as install, with no confirmshaming ("Are you sure you want to give up?") and no exit survey.
- No pre-ticked choices. No defaults that turn on memory.
- No medical framing: no symptom checkers, quizzes, "Do you have ADHD?" or self-assessments.

## Launch design QA checklist

- [ ] Every claim on the site traces to `evidence/claims.yaml`, and no medical purpose is stated (MHRA test).
- [ ] Each route page has been walked end to end by someone who isn't technical, on the current host UI. Screenshots are dated within the last 60 days.
- [ ] Every step has one action, a "what you'll see" callout, a "doesn't match?" panel and a Help link.
- [ ] Copy buttons work with keyboard, voice ("click Copy instructions"), screen reader announcement, and with the clipboard blocked.
- [ ] The paste text fits the target host's limit (character count shown and checked against the host).
- [ ] The demo has no network calls, no free-text input, works without JavaScript, and shows its "example written by us" label.
- [ ] Zero cookies or storage, zero third-party requests (check the browser network panel). The privacy page says so.
- [ ] axe/Lighthouse report no errors, followed by manual checks: keyboard-only, NVDA + Firefox, VoiceOver iOS and macOS, Voice Control/Dragon, 400% zoom, text-spacing bookmarklet, Windows contrast themes.
- [ ] Contrast passes in both themes, including focus rings and status labels.
- [ ] Reduced motion is respected, nothing autoplays, and there are no pop-ups or timers.
- [ ] Headings and the reading order make sense with CSS off. Every page title is unique.
- [ ] Urgent-help resources have been checked against the product's verified UK/US list on the launch date.
- [ ] Uninstall is tested for each host, and the copy says host history isn't erased.
- [ ] A plain-language read-through: no "superpower", no shame, no hype, no "approved".
- [ ] The accessibility statement is published with a contact route that doesn't need an account.

## Risks

- **R1. Paste limit:** the 21 KB file is longer than the reported ~8,000-character custom GPT limit, which isn't yet confirmed. The easiest route may fail at step 3.
- **R2. Stale screenshots:** host UIs change without warning, which breaks "what you'll see". This needs an owner and a check cadence.
- **R3. Trademark:** host names, logos and screenshots may need permission (A4).
- **R4. Overclaiming through design:** testimonial-style demo bubbles or "proven" badges could imply a medical purpose.
- **R5. Hosting logs:** even a static host logs IP addresses alongside ADHD page paths. Choose a host with minimal or no logs.
- **R6. Plan gating:** some host features may need paid plans. This is unknown, and each route page must state it.

## Open decisions for the product owner

1. Build a short paste version under 8,000 characters, or drop the custom GPT route? This blocks the ChatGPT route.
2. Which routes to show at launch: only tested ones, or all of them with status labels?
3. A claude.ai starter set: 1 ZIP (`adhd-help`, which INSTALL.md suggests as a good first choice) or a small bundle? Uploading 13 ZIPs one by one is too many choices.
4. Real screenshots or neutral illustrations (R3)?
5. Who owns screenshot freshness and urgent-help checks after launch?
6. The hosting provider and its logging policy (R5).
