# Technical and trust plan: consumer website

Workstream: technical architecture, security and trust. Planning only; building waits on the ChatGPT tests.

## Top 3 recommendations

1. **Plain static site, no JavaScript framework, no backend, no cookies, no third-party requests.** Generate it with a small stdlib Python script in the repo (the repo is already Python). That leaves nothing to breach, no health data to hold, and almost no supply chain.
2. **The site never hand-copies a download or the paste-in instructions.** CI builds `dist/`, checks every file against `dist/MANIFEST.json`, publishes an immutable versioned release with signed provenance, and renders the downloads page *from that release*. A tampered paste-in text is a prompt injection straight into a user's assistant, so it gets the same integrity control as the ZIPs.
3. **Publishing downloads is gated.** No public download links until the licence and named owner are decided, and the privacy, MHRA intended-purpose and clinician crisis reviews are signed off. Until then the site is a private preview, or launches with no downloads.

## What exists today (verified 2026-10-19)

- `dist/MANIFEST.json` lists package `0.1.0`, 13 skills and 470 files, each with a sha256 and a byte count. This covers `zips/*.zip`, `generic/ADHD-support-instructions.md` (21,487 bytes), `generic/routing.md` and `install.py`. I re-hashed all 470 files and none mismatched.
- ZIPs use a fixed timestamp (`scripts/build.py`, `ZIP_DATE`), and a reproducibility test exists.
- `install.py` makes no network calls.
- Gaps:
  - The manifest records no source commit or build time, and is not signed.
  - The repo has one commit, no git remote and no CI.
  - There is no licence.
  - `marketplace.json` owner is `OWNER-TO-BE-CONFIRMED`.

## Stack and hosting

**Recommended:** hand-written semantic HTML and one CSS file, plus about 20 lines of same-origin JS for "copy instructions". Optional: a `scripts/build_site.py` (stdlib only) that renders the release page from the manifest.
- Use a system font stack. No web fonts, icon fonts or CDNs.
- The pages still work with JS off; copy then falls back to a selectable text block and a download link.

**Why:** the site's job is to explain and to link. Accounts, a CMS or a database would add special-category data risk, plus patching, with no MVP benefit. A static site also suits users who find heavy pages hard: it is fast, has no motion, and works with reader mode. *Rejected for MVP:* Next.js/Astro (an npm supply chain for a 6–8 page site), Squarespace/Wix-type builders (third-party trackers and fonts by default; headers can't be controlled), and any form backend.

| Host | Custom headers (CSP etc.) | Releases tie-in | Logs / analytics | Trade-off |
|---|---|---|---|---|
| GitHub Pages | **No** (meta CSP only; no HSTS control, no Permissions-Policy) | Native | GitHub keeps logs; no aggregate counts offered | Simplest, but can't meet the header plan. Fine for a preview |
| Cloudflare Pages | Yes (`_headers`) | Via CI | Edge aggregate counts; its JS beacon is optional, so don't enable it | Free tier; US provider (transfer basis needed) |
| Netlify | Yes (`_headers`) | Via CI | Paid server-side aggregate analytics, no JS | Simple; US provider |
| UK/EU VPS + Caddy/nginx | Full | Via CI | Own logs, own retention | Data stays in the UK/EU, but you own patching and uptime |

**Recommendation:** Cloudflare Pages or Netlify for the site, with GitHub Releases (or the host itself) storing the files. *Assumption:* plan pricing and features are unverified; check them at build time. Whichever is chosen, confirm the international transfer basis (UK Extension to the DPF or IDTA) in the DPIA.

## Downloads: build, verify, sync

1. Push a tag `vX.Y.Z` to start CI, which runs:
   - `scripts/build.py`;
   - `scripts/validate.py --host-checks` and the tests;
   - a second clean build that must produce byte-identical output (reproducibility).
2. CI writes `SHA256SUMS` from `MANIFEST.json`. Add `source_commit` and `built_from_tag` to the manifest (a small change to build.py).
3. CI publishes an **immutable** release containing the ZIPs, `ADHD-support-instructions.md`, `routing.md`, `install.py`, `MANIFEST.json` and `SHA256SUMS`. Turn on GitHub immutable releases if they are available. Never re-upload over a published tag; a fix means a new patch version.
4. Provenance: GitHub artifact attestations (Sigstore-backed, SLSA build provenance) on each file. Users can check with `gh attestation verify <file> --repo <owner>/<repo>`. Optionally sign `SHA256SUMS` with cosign or minisign.
5. The site build fetches the release manifest, rejects any file whose hash differs, and renders version, size, sha256 and date per file. The paste-in text on the page is read from the same verified file, never pasted into a template by hand. **If the site shows a hash that isn't in the release, CI fails.**
6. "Latest" is one redirect (`/download/latest`) to the current version. Old versions stay listed and marked "superseded", and are withdrawn if a safety fix lands.

Honest limit: non-technical users will not check hashes. Their real protection is one canonical domain, HTTPS and HSTS, files only ever linked from that domain, and an "official sources" page. Hashes and attestations serve verifiers, press, reviewers and fork-watchers.

**Paste-in length:** the full file is 21 KB, and the custom GPT limit is about 8,000 characters (unconfirmed). Any shortened variant must be a **build artefact** that passes the validator, including the safeguards-block check. Never trim it in the site's own content.

## Data minimisation

- **No cookies, localStorage or fingerprinting.** That means no consent banner is needed (PECR). Any cookie added later needs a fresh review.
- **Analytics: none at launch.** If counts are needed:
  - use host-side aggregate request counts, or release download counts (aggregate, no identity);
  - no JS analytics, including "privacy-friendly" ones, without a DPIA update.
  - Reason: per-visitor data on who read the medication or crisis pages is a health inference.
- **Server logs:** shortest retention the host allows (aim ≤ 30 days), IP truncation if offered, never joined with anything, no access for marketing.
- **No third-party embeds:** no Google Fonts, YouTube/Vimeo (even nocookie), social widgets, chat widgets, maps or CDN scripts. Demo videos are self-hosted MP4/WebM with captions and a transcript, and never autoplay.
- **Outbound links** (NHS, NICE, crisis lines) use `Referrer-Policy: no-referrer`, so the destination can't see which ADHD page sent the visitor.
- **Contact:**
  - a role mailbox (e.g. `hello@`), with a page note and auto-reply: "Please don't send health details. We can't give medical advice. If you're in crisis: [verified UK/US resources + location-neutral line]."
  - No contact form, since that needs a backend.
  - If GitHub Issues is offered, label it **public**.
  - Security reports go to `/.well-known/security.txt` (RFC 9116).
- **Mailing list:** none for MVP. Adding one is a new processing activity.

## Security headers and hygiene

Starting header set (via `_headers`):

```
Content-Security-Policy: default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self'; media-src 'self'; font-src 'self'; connect-src 'self'; form-action 'none'; frame-ancestors 'none'; base-uri 'none'; upgrade-insecure-requests
Strict-Transport-Security: max-age=63072000; includeSubDomains   (add "; preload" after 4+ stable weeks)
Referrer-Policy: no-referrer
Permissions-Policy: camera=(), microphone=(), geolocation=(), browsing-topics=(), interest-cohort=()
X-Content-Type-Options: nosniff
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Resource-Policy: same-origin
```

- No inline script or style, so no `unsafe-inline`.
- Serve `.md` as `text/plain; charset=utf-8`.
- No source maps.
- `rel="noopener noreferrer"` on external links.
- Add an `observatory`/`curl -sI` header check to CI.

Hygiene:
- No npm. If an SSG is adopted later: lockfile, Dependabot, review of `postinstall` scripts.
- Pin GitHub Actions to commit SHAs and set least-privilege `permissions:`.
- Deploy with OIDC, not long-lived tokens.
- Branch protection, with two-person review for copy changes, because claims are regulated content.
- Accounts: hardware-key 2FA on GitHub, the registrar and DNS. Registrar lock, DNSSEC, and a CAA record.

## Privacy notice outline

1. Who we are: controller name and contact (**owner not decided**).
2. Short version: no cookies, no accounts, no tracking. The site doesn't know who you are.
3. What the host's servers log, why (security and operation), retention, and lawful basis (legitimate interests; LIA to be written).
4. Email to us: what we keep, for how long, and a request not to send health information.
5. Downloads: we can't see what you do with the files. The skills store nothing unless you turn memory on, in your own folder (link to `privacy-and-retention.md`).
6. **Your AI assistant is separate:** its provider's privacy terms apply to everything you type.
7. Processors and international transfers (host, email provider).
8. Your rights, how to complain to the ICO, and the date the notice changes.

## Pre-launch compliance and review checklist

| # | Item | Owner | State |
|---|---|---|---|
| 1 | DPIA screening (health context means a full DPIA is likely), including host transfers | Privacy/legal | awaiting |
| 2 | UK GDPR special-category risk from inferences: logs, analytics, referrers, email | Privacy/legal | awaiting |
| 3 | MHRA SaMD intended-purpose review of **all site copy** (the copy decides status, and a disclaimer can't fix it) | Regulatory | awaiting |
| 4 | ASA/CAP (UK) and FTC (US) claims review. Every claim traces to `evidence/claims.yaml`. **Flag for legal** | Legal | awaiting |
| 5 | Accessibility statement (WCAG 2.2 AA target, known issues, contact) plus a test with assistive technology and users with ADHD | Accessibility | not run |
| 6 | Licence chosen and owner named, in the site, manifests and release. **Blocks downloads** | Product owner | not decided |
| 7 | Clinician review of safeguarding and crisis content on the site (and its consistency with the product's UK/US resources) | Clinician | awaiting |
| 8 | Adult-only positioning; no child-targeted copy | Product/legal | to check |
| 9 | Headers, CSP, `security.txt` and provenance verified on the live domain | Engineering | not run |

## Threat model

| Threat | Actor / route | Impact | Control | Residual |
|---|---|---|---|---|
| **Tampered downloads or paste-in text** | Compromised CI, host or account; MITM | High: altered instructions steer users' assistants, e.g. unsafe medicine advice or exfiltration prompts | Reproducible build, hash gate, immutable releases, attestations, 2FA/OIDC, HSTS | Medium: an insider with release rights |
| **Impersonation and fake copies** | Lookalike domains, GPT-store "ADHD Support" GPTs, re-uploaded ZIPs, forks | High: users trust edited safety text | "Official sources" page; published hashes; state plainly whether an official GPT exists (**owner decision**); optional defensive domains; takedown route | High: can't be fully prevented |
| **Prompt injection in pasted instructions** | Modified text passed around, or a user pastes untrusted content alongside | Medium–High | Copy comes from the verified file only; visible version line; the instructions already treat content as data | Medium: instructions aren't enforcement (`privacy-and-retention.md`) |
| **Defacement / content swap** | Stolen GitHub, host or DNS credentials | High: false medical claims or crisis numbers break regulatory status and safety | Branch protection, two-person review, hardware 2FA, registrar lock, DNSSEC, CAA, uptime and content-hash monitor | Low–Medium |
| **Privacy leak via third parties** | An embed, font or analytics script added later | Medium: health inference | CSP blocks it by default; CI header check; any exception needs DPIA sign-off | Low |

Incident path: take the site to a static "paused" page, revoke the release, publish an advisory with the bad hashes, notify the ICO within 72 hours if personal data was affected. Write the runbook before launch.

## Estimated build effort (estimates, one engineer, excluding copy and design)

| Work | Estimate |
|---|---|
| Static site, 6–8 pages, CSS, copy button, fallbacks | 2–4 days |
| CI: build, validate, reproducibility, release, attestations, site-sync gate | 2–4 days |
| Hosting, DNS, headers, `security.txt`, monitoring | 0.5–1.5 days |
| Drafting the privacy notice and accessibility statement (before legal review) | 1–2 days |
| Accessibility and cross-browser testing and fixes | 2–4 days |
| **Total engineering** | **about 1.5–3 weeks** |

External reviews (legal, MHRA, clinician, accessibility users) are not estimated; their lead time will probably dominate.

## Assumptions, open decisions, risks

- **Assumptions:** UK-first audience, with US visitors; a single site owner; the GitHub repo will be public (unconfirmed, as there is no remote yet); host pricing and features unverified.
- **Decisions for the product owner:**
  - licence and named controller;
  - host choice (US edge host versus UK/EU VPS);
  - whether any analytics are wanted;
  - whether an official custom GPT will be published;
  - contact mailbox owner and response time;
  - whether to launch with no downloads until reviews clear.
- **Risks:**
  - Copy drifts into medical claims after launch (process risk; mitigated by the review gate on copy PRs).
  - The 8,000-character variant drops safeguards.
  - Fake copies outrank the official site.
  - Host logs are an unavoidable minimum of processing.
