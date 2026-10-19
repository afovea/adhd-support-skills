# Content strategy: ADHD Support Skills consumer site

Workstream: content. Sources: brief.md, README.md, INSTALL.md, examples/conversations.md, evidence/runtime-evidence.md, evidence/crisis-resources.md, docs/capability-matrix.md.

## Top 3 recommendations

1. **Lead with the user's own words, not the feature list.** Headlines are things people actually say ("I can't start the report"). "Skill", "plugin" and "router" never appear in headlines or first-level navigation.
2. **One honest evidence pattern, used everywhere:** "These ideas show up in ADHD guidance and in what adults with ADHD say helps. No one has tested this software." Every health phrase on the site comes from the guardrail table below, with its claim ID.
3. **Don't promise ChatGPT until there is a short version.** Custom GPT instructions are probably limited to about 8,000 characters (unconfirmed). The full file is 21 KB. The ChatGPT install page is blocked until a short version of the instructions exists and has been tested.

## Assumptions (labelled)

- A1. Visitors are adults who use an AI assistant at least a little. Most have never used a terminal.
- A2. The site runs no AI itself. Prompts are there to copy, not to run on the site.
- A3. The site collects nothing: no analytics, cookies or forms. If that changes, the privacy copy has to change too.
- A4. The product name stays "ADHD Support Skills" for now. Body copy calls it "the ADHD support instructions" or just "it".
- A5. Reading-level target: plain English, around a UK reading age of 9 to 11. Sentences of 15 words or fewer. One action per step.

## 1. Voice and tone

Calm, direct, adult, honest, brief. It sounds like a friend who's good at admin, not a coach or a clinic.

| Principle | Do | Don't |
|---|---|---|
| Concrete over clever | "One small step to start. Then it gets out of the way." | "Unlock your productivity potential." |
| No hype, no pity | "Some days starting is the hardest part." | "Struggling with ADHD? You're not broken!" / "Your ADHD superpower" |
| No shame, no pressure | "Missed a week? Start again from the small version." | "Don't break your streak!" |
| Honest limits, said once, plainly | "It can't set a timer in a chat window. It will tell you that." | "Never forget anything again." |
| Choice without overload | Two options at most, with a default. | Grids of 13 skills on the home page. |
| Respect autonomy | "You don't need a diagnosis, and you don't need to explain yourself." | "Take our quiz to see if you have ADHD." |
| Short by default | Put the detail behind "More detail". | Walls of text, or carousels. |

Style rules: UK English. Sentence case. No exclamation marks. Never "just" in front of a hard step ("just install it"). No autoplaying or decorative animation. Write "you", not "users" or "sufferers".

## 2. Messaging hierarchy

**Value proposition (pick one):**
- V1 (recommended): **"Help with the doing part of everyday life, inside the AI assistant you already use."**
- V2: **"Stuck on starting? Say it in your own words."**
- V3: **"Small, calm steps for getting things done. No diagnosis needed."**

**Supporting points (in this order):**
1. Ask in ordinary words. "I can't start the report" is enough.
2. One small next step at a time, or the full plan if you ask for it.
3. You're in control: "quiet", "pause", "stop" and "less" work at any time.
4. Honest about what it can and can't do. It never pretends to set a timer or send a message.
5. Private by default. Memory is off unless you turn it on.

**Proof points (honest only):**
- Behaviour you can see: the example conversations (synthetic and labelled as such).
- What it refuses to do: the "What it won't do" list, taken from README.
- Evidence with its limits shown: see the guardrail table. **No usage numbers, testimonials or reviews exist. Don't make any up.**
- Free to use (product fact). "Open source" is **not** allowed until there's a licence.

## 3. Page-by-page outline (MVP)

| Page | Headline / sub-headline | Key blocks |
|---|---|---|
| **Home** | "Help with the doing part of everyday life" / "Ask your AI assistant in your own words. Get one small next step. No diagnosis needed." | (1) Three "You say → What happens" pairs from README. (2) One example conversation (#1 overdue paperwork). (3) The "Words that work any time" control card. (4) "What it won't do" (5 bullets). (5) A single "Get it" button leading to the install chooser. (6) The not-medical-care line and the evidence one-liner. |
| **What it helps with** | "Pick the thing that's hard right now" / "Each one starts small. You can always ask for more." | 12 plain-language cards: Get it out of my head · Choose what's next · Get started · Quiet company · See the time · Remember later · Get back to it · Switch tasks · Flexible routines · Too much right now · ADHD health information · My saved preferences. Each card has one line, one "Try saying" prompt, and one honest limit. No skill IDs. |
| **Get it (chooser)** | "Which app do you use?" / "Pick one. You can change later." | Four route cards, with the easiest first. Each card shows the steps, the time it takes, and its status: "Tested" or "Not yet tested". |
| **Route pages** (×4) | e.g. "Add it to Claude" / "About 5 minutes. No technical skills needed." | Numbered steps (section 5), a "Check it worked" prompt, "Something's not right?", and how to remove it. |
| **Your control and privacy** | "You're in charge" / "Say a word to change how it behaves. Your data stays where you put it." | The controls table. Memory: off by default; you choose a private folder; deletion is real; it can't erase your app's own history. What this site collects: nothing (A3). |
| **Evidence, honestly** | "What we know, and what we don't" / "Some ideas here appear in ADHD guidance. No one has tested this software." | Three short sections: Backed by guidance · Early or uncertain · Not tested. Links to sources. "Not reviewed by a clinician yet." |
| **Safety** (also in the footer) | "Not medical care" / "What to do if you need more than this" | See section 7. |

Not in the MVP: blog, comparison pages, anything for children or parents (needs a separate review), sign-up, newsletter.

## 4. Claims guardrail table

Every page that mentions evidence must also carry the line "None of this research tested this software."

| Status | Wording | Trace / reason |
|---|---|---|
| Allowed | "Breaking tasks into smaller steps, timers, visual reminders and routines appear in ADHD practice guidance." | CLM-GD-CADDRA-SCAFFOLD |
| Allowed | "UK guidance (NICE) mentions changes like shorter periods of focus and written instructions." | CLM-GD-NICE-ENV |
| Allowed | "Adults with ADHD describe using schedules, to-do lists and reminders." | CLM-RS-LIVED |
| Allowed | "Body doubling means having someone else around while you do a task, in person or online." | CLM-BD-DEFINITION |
| Allowed | "Research on body doubling is early. ADHD organisations say proof that it works is lacking." | CLM-BD-EARLY |
| Allowed | "No study we found has tested an AI body double." | CLM-BD-NO-AI |
| Allowed | "No brain mechanism, such as dopamine, has been shown." | CLM-BD-MECHANISM |
| Allowed | "In the UK, only a specialist can diagnose ADHD. A GP can refer you." | CLM-GD-NHS-DIAGNOSIS |
| Allowed | "Research on digital tools for adults with ADHD is mostly at an early stage." | CLM-RS-DIGITAL-REVIEW |
| Needs care | "In one survey, most people said they were more likely to finish tasks with someone there." | CLM-BD-SURVEY. Only if you also say "self-report, no comparison group". Never "studies show". |
| Needs care | "If-then plans" / "when X, do Y" | CLM-RS-IMPL-INTENTIONS is general-population and abstract-only. Describe the feature; cite no effect size. |
| Needs care | "Helps you start / remember / switch" | Allowed as a description of what it does. Not allowed as a health outcome ("improves focus"). |
| Needs care | "Free" | Product fact, but there's no licence yet. Don't add "forever" or "open source". |
| Needs care | "Private" | Say "memory is off by default". Don't say "your data never leaves your device", because the host app keeps its own history. |
| Never | "Proven", "clinically tested/validated", "evidence-based app", "reviewed by clinicians", "approved" | Not done (brief; release-readiness). |
| Never | "Treats / manages / reduces ADHD symptoms", "therapy", "coaching", "CBT" | Medical intended purpose (CLM-GD-MHRA-SAMD). CBT claims are abstract-only and are not about AI. |
| Never | "Dopamine", "rewires your brain", "superpower", "for kids" | CLM-BD-MECHANISM. Tone rule. Adult-only release. |
| Never | "Find out if you have ADHD", "screening", "quiz" | It doesn't diagnose. CLM-GD-NHS-ONLINE-TEST is excluded. |
| Never | "Never forget again", "it will remind you" (without "if your app supports it") | It doesn't fake reminders. Capabilities depend on the host. |
| Never | "Works in ChatGPT" (without a status) | That route is untested. |

## 5. Installation, in plain language

Pattern for every route: **what you need → numbered steps (one action each) → "Check it worked" → "Remove it"**. Name buttons exactly as the app shows them, and re-check those names when the site is built (app wording changes). Don't use "simply" or "just". Show a status tag on every route.

**ChatGPT** (status: blocked; needs the short version):
> You need: a ChatGPT account that can make your own GPT (plan requirement unconfirmed).
> 1. Copy the short instructions (Copy button). 2. In ChatGPT, open "GPTs", then "Create". 3. Choose "Configure". 4. Paste into the "Instructions" box. 5. Name it, for example "My ADHD helper". Save it as "Only me".
> Check it worked: type "I can't start my report." You should get one small step.

**Claude app** (status: not yet tested):
> You need: a Claude account, with "code execution" switched on in settings.
> 1. Download "Get started" (one small file). 2. In Claude, open Customise, then Skills. 3. Press +, then "Upload a skill". 4. Pick the file you downloaded. 5. Add more helpers the same way, if you want them.
> Check it worked: "I can't start my report."
> Fallback: paste the instructions into a Claude Project. (The size limit is unknown. Test it.)

**Claude Code** (status: tested; for people who use a terminal):
> "This one is for people who are comfortable typing commands." Show the single command in a copy box. Put the other options behind "More options". There's no public install command until release, so the page has to wait for that.

**Any assistant** (status: works anywhere, lighter version):
> 1. Copy the instructions. 2. Find your assistant's "custom instructions" or "project instructions" box. 3. Paste and save. 4. Talk normally.
> Say plainly: "This is a lighter version. The safety rules and controls are included."

Install error and help copy: "It isn't responding the way the examples show." → "Try naming it: 'Use the ADHD support instructions to help me start.' Still stuck? Check you saved the instructions."

## 6. Microcopy

**Try these** (a chip shows the short label; the copied text is the full prompt):

| Chip | Copied prompt |
|---|---|
| Can't start | "I know what I need to do but I can't start the report." |
| Too much in my head | "Everything is in my head: [your list]. Help me sort it." |
| What first? | "I have five things and don't know what to do first." |
| Keep me company | "Body double me while I tidy. Stay quiet unless I say stuck." |
| I have 40 minutes | "I have forty minutes. Help me plan it with a stopping point." |
| Where was I? | "Where was I?" |
| Doctor's appointment | "Help me get ready for a GP appointment about ADHD." |

Copy button: "Copy" → "Copied". Announce it to screen readers ("Prompt copied"). Section intro: "Copy one, paste it into your assistant." Under the chips: "Examples are made up. They show how it's meant to reply."

**Controls card**, titled "Words that work any time":
- **quiet**: "No more prompts from it."
- **pause**: "Hold everything for now."
- **stop**: "End here. No guilt trip."
- **less**: "Shorter replies."
- **more detail**: "The full plan."
- **no praise**: "Just the facts."
- **not that**: "Try something else."

Note under the card: "Quiet and stop also cancel any check-ins it set, if your app allows check-ins."

## 7. Not medical care, and crisis content

Keep it proportionate: no red banners, no pop-ups, no alarm icons. Use the same quiet style as other notes.

- **Footer, every page:** "Not medical care. It doesn't diagnose or advise on medicine. Need help now? →" The link goes to Safety.
- **Home, next to the evidence line:** "This isn't a medical service and hasn't been clinically tested. For health decisions, talk to your GP, prescriber or pharmacist."
- **The "ADHD health information" card and the Evidence page:** the same line again.
- **Safety page:** first the location-neutral text from crisis-resources.md ("If you're in immediate danger, call your local emergency number..."). Then Find A Helpline. Then the verified UK list (999, NHS 111 mental health option, Samaritans 116 123) and the US 988 line. Show a "checked on" date. Don't add other countries' numbers.
- **Before launch:** re-check every number. The NHS page's review date is overdue.

## 8. Glossary: avoid or explain

| Term | On the site |
|---|---|
| Skill | Avoid in headlines. Use "helper" or "a kind of help". Explain once on install pages: "a set of instructions your assistant can follow". |
| Plugin | "Add-on". Only use the word "plugin" on the Claude Code page. |
| Router | Never show it. Say "It works out what kind of help you need." |
| MPoT / My Point of Truth | Say "your saved preferences" first, with the name second: "My Point of Truth (your saved preferences)". Never "MPoT". |
| Body double | Explain on first use: "someone (or something) keeping you company while you work". |
| Custom GPT / system prompt / project instructions | Say "the instructions box in your app", then the app's own label in brackets. |
| ZIP, terminal, CLI, host, session, namespaced | Avoid. If unavoidable: "file", "a window where you type commands", "app", "conversation". |
| ADHD | Fine to use. Always pair it with "no diagnosis needed". |

## Open decisions for the product owner

1. Which value proposition: V1, V2 or V3?
2. Product name: keep "Skills" in the name, or use a consumer name?
3. Who will write and test the short (under 8,000 characters) instructions, and when?
4. Will the site use any analytics at all? (Recommendation: none. Health inferences are special-category data, CLM-GD-ICO-SPECIAL.)
5. Licence and named owner, before using "free" or "open source" prominently.
6. Clinical and legal review of the Safety and Evidence pages before launch.

## Risks

- **Overclaiming through tone, even without wrong words.** For example "Finally, help that works." This affects regulatory status (CLM-GD-MHRA-SAMD). Mitigation: a claims check on every page before publishing.
- **Install pages go stale** as app labels change. Mitigation: a "checked on" date per route.
- **Untested routes fail for first-time users**, and trust drops. Mitigation: show status tags, plus the "Check it worked" step.
- **Example conversations get read as testimonials.** Mitigation: label them "Made-up example".

Validation: test comprehension with 5 or more non-technical adults (including people who find dense text hard). Tasks: "install it with route X", "what happens if you say stop", "is this medical care?"
