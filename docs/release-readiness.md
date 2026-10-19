# Release readiness — 0.1.0 (local build, 2026-10-19)

**Verdict: complete locally. NOT ready for public release.** The implementation, packaging and structural validation are complete. Several public-release requirements are still outstanding:
- qualified clinical review;
- privacy and regulatory review;
- lived-experience usability research;
- a licence and owner decision;
- native-host behavioural runs.

No clinician, regulator, legal reviewer or user group has approved anything.

States used: **complete** · **failed** · **not run** · **awaiting qualified review** · **out of scope**.

## Implementation

| Item | State | Evidence / what would change it |
|---|---|---|
| 13 skills with valid SKILL.md, explicit and natural entry examples, workflow, stop conditions, fallback, examples, safeguards and evidence pointer | complete | `scripts/validate.py` → canonical skills ok |
| Router (`routing.md`) and registry, including the mechanism map | complete | Registry check ok. Every report mechanism mapped |
| Shared policies: interaction, safety, evidence, permission, memory, execution state | complete | `shared/` |
| Core safeguards embedded in every entry point | complete | Validator checks the block in every SKILL.md and every bundle |
| Self-contained standalone skills (no parent links) | complete | `check_dist`, plus ZIPs extracted into a clean folder and re-checked |
| MPoT: templates, operations, real deletion, concurrency, import safety | complete | `tests/memory/test_mpot.py`: 21 tests pass |
| Mocked capability harness (failure, ambiguity, cancellation, DST) | complete | `tests/behaviour/test_capability_harness.py`: 12 tests pass |
| Installer: dry run, idempotent update, managed block, ownership-bounded uninstall | complete | `tests/packaging/test_packaging.py`: 21 tests pass (including compact instructions) |
| Reproducible bundles plus manifest | complete | Reproducibility test; `dist/MANIFEST.json` |
| Synthetic example library (6 required scenarios, plus handoffs, overrides, stopping, safety) | complete | `examples/conversations.md` |

## Validation

| Item | State | Evidence / what would change it |
|---|---|---|
| Static and package validation | complete | `python3 scripts/validate.py --host-checks`: all checks passed, 54 unit tests OK |
| Compact instructions for ChatGPT-sized hosts (under 7,800 characters, safeguards checked) | complete (build and validation) | `check_compact` and 4 tests. **Behaviour in ChatGPT not run**: use the Study 0 log |
| `claude plugin validate` (marketplace and plugin manifest) | complete | Passed on Claude Code 2.1.150. `--strict` fails only on the deliberately unset `author` field |
| Claude Code plugin loads in isolation | complete | `claude -p --plugin-dir dist/claude-code --setting-sources project` listed all 13 namespaced skills, and no user plugins |
| Behavioural evaluation, simulated host (70 cases) | complete, with failures | Run 1: 67 pass, 3 fail, **0 severe**. 3 repaired; retest 4 of 5 pass. MEM-06 failed against a defective case sheet, which has been amended and **not re-graded**. See `tests/results/2026-10-19-simulated.md` |
| Behavioural evaluation, native Claude Code | not run | The CLI's login token was revoked (HTTP 401). Run `claude auth login`, then `python3 scripts/evals.py run-claude` |
| Behavioural evaluation, Codex | not run | Codex is not installed |
| claude.ai ZIP upload | not run | Upload one ZIP and confirm it is accepted and triggers |
| HLT-01 re-run after adding the common-side-effects claim | not run | Re-run that case |
| SAF-01, SAF-05 and S11 re-run after the switch to generic urgent-help guidance | not run | Earlier transcripts used the old country-based wording. Re-run them against the updated cases |
| Independent (non-author-model) behavioural review | not run | Have different reviewers, or a different model family, grade the transcripts |

### Release-blocking checks

None of these were observed in any transcript:
- an unsafe medication instruction;
- encouragement of imminent harm;
- a fabricated external success;
- an unauthorised disclosure;
- continued prompting after stop.

This is a bounded statement about 75 synthetic transcripts produced by a simulated host. It is not a guarantee.

## Evidence

| Item | State | Evidence / what would change it |
|---|---|---|
| Register of sources and claims, with categories and statuses | complete | 46 sources and 43 claims: 26 verified, 16 partial-access, 1 unverified (excluded from runtime) |
| Exported citation placeholders removed | complete | The validator scans for them |
| Claims checked against full text where marked verified | complete (by the build agent) | Every claim checked only against an abstract was downgraded to partial-access |
| Full-text checks of partial-access research claims | not run | Obtain the full texts. See `evidence/evidence-audit.md` |
| Clinician review of runtime claims, safety policy and medicine cases | **awaiting qualified review** | Clinical reviewer sets `clinician_reviewed` per item |
| Urgent-help guidance (generic, no numbers or named services) | **awaiting qualified review** | `evidence/crisis-resources.md`. The validator fails any shipped text with a support number, named helpline or directory |

## Governance and legal

| Item | State | Evidence / what would change it |
|---|---|---|
| Licence | **not decided** | No licence was authorised. Choose one before any public release. Research PDFs and the source reports are not redistributed |
| Owner / author in manifests | **not decided** | `OWNER-TO-BE-CONFIRMED` placeholder in the marketplace manifest. Author omitted |
| Data-protection assessment (UK GDPR / EU GDPR; DPIA screening) | **awaiting qualified review** | Privacy/legal reviewer |
| Medical-device qualification (intended purpose and claims) | **awaiting qualified review** | Regulatory reviewer. The product does not certify its own exemption |
| Accessibility review (screen reader, voice, cognitive) | not run | Accessibility reviewer plus users with access needs |

## Users and research

| Item | State | Evidence / what would change it |
|---|---|---|
| Lived-experience usability research with adults with ADHD | not run | `docs/evaluation-plan.md` §3, with a methodologist setting the design and sample size |
| Body-doubling presence comparison | not run | Plan in §3 |
| Clinical effectiveness research | out of scope | Needs separate protocol, ethics approval and expertise |
| Child or teen product | out of scope | Needs separate safeguarding, developmental and clinical review before any marketing |

## Known limitations

- SKILL.md text is guidance, not enforcement. Host safety systems, permissions and retention govern what actually happens.
- In a turn-based chat the agent cannot speak first. There are no check-ins without a real scheduler.
- Natural-language selection depends on the host's skill-listing budget. Many other installed skills may crowd out these descriptions.
- Urgent-help guidance is deliberately generic. It can't connect anyone to a specific service; it explains how to find one locally.
- The same model family wrote, simulated and graded the evaluations.
