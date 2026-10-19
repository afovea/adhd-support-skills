# Evaluation plan

There are five kinds of evaluation here. They answer different questions, and a pass at one level says nothing about the others.

| Level | Question | Status in this build |
|---|---|---|
| 1. Static / package validation | Are the skills, registry, evidence and bundles well-formed and self-contained? | **Run**: `scripts/validate.py` |
| 2. Model behavioural evaluation | Given these instructions, does a model behave as intended across realistic, adversarial and multi-turn cases? | **Partly run**: simulated host. Native host not run (CLI authentication revoked). See release-readiness |
| 3. Usability research | Do adults with ADHD find it helpful, low-pressure and accessible? | **Not run.** Planned below |
| 4. Clinical effectiveness research | Does use improve functional or clinical outcomes? | **Out of scope** for this build. Needs separate expertise and ethics approval |
| 5. Privacy / regulatory assessment | Is it lawful and correctly classified? | **Not run.** Awaiting qualified review |

## 1. Static validation (repeatable)

```bash
python3 scripts/validate.py --host-checks
```

This checks:
- frontmatter against the spec;
- the name and folder match;
- natural-language selection has not been disabled;
- the core-boundaries block is present and current;
- registry, skill, eval and claim cross-references;
- every skill has at least one multi-turn eval;
- evidence fields and statuses ("verified" cannot rest on an abstract);
- there are no citation placeholders;
- `dist/` is in sync with a fresh build;
- every bundle is self-contained, contains no private paths and no memory files, and that ZIPs work after extraction;
- the generic instructions are under 32 KiB.

Unit tests run as part of it (`tests/**/test_*.py`):
- MPoT scoping, consent, sensitivity guards, supersession, deletion cascade, stale-hash conflicts, concurrent writers and injection-safe import;
- the mocked tool harness: success, failure, ambiguous-then-exists, ambiguous-then-missing, unverifiable ambiguity, owned-only cancellation, cancellation failure, vague times, DST gap and overlap, travel zones;
- installer behaviour: dry run, idempotence, user edits kept, foreign skills untouched, ownership-bounded uninstall, the MPoT folder untouched, Codex layout, router-only, personal and generic modes;
- bundle reproducibility.

## 2. Model behavioural evaluation

There are 70 synthetic cases in `tests/{routing,behaviour,safety,memory}/cases.yaml`. Each case records:
- the user input (single- or multi-turn);
- prior context;
- capabilities and permissions;
- scripted tool results;
- the expected route;
- expected and forbidden behaviours, plus deterministic regex prohibitions where a phrase is unambiguous;
- whether the case is critical.

The cases cover every scenario in the build brief.

### Procedure

1. `python3 scripts/evals.py export --out DIR` writes **blind inputs** (no expectations) and separate grading sheets.
2. A host produces transcripts:
   - **Native:** `python3 scripts/evals.py run-claude --out transcripts.json`. This runs Claude Code with only this plugin loaded (`--plugin-dir dist/claude-code --setting-sources project`, tools limited to Skill and Read). Text-only, tool-free cases only.
   - **Simulated:** a separate agent sees only the skill names and descriptions (as a host would), reads a skill only when it decides to use it, and plays the assistant with scripted tool results. This is how tool cases (reminders, check-ins, memory) were exercised here.
3. A different agent grades each transcript against its sheet. Graders do not read the skill files.
4. `python3 scripts/evals.py score transcripts.json grades.json --out results.json` combines:
   - the grades;
   - the deterministic regex checks;
   - route agreement, which is reported separately, because a different but defensible skill choice is not a safety failure.

### Independent grading (required for safety and health cases)

Self-grading by the model family that produced the transcripts can't catch the errors that family shares. Safety (`SAF-*`) and health (`HLT-*`) results only count once graded independently: by a human, or by a different model family.

1. **Generate transcripts.** Record `host_model` on every case. `score` flags runs that don't.
2. **Make the grading pack:**

   ```bash
   python3 scripts/evals.py human-pack TRANSCRIPTS.json --suite safety --out PACK
   ```

   This writes `PACK/human-grading.md` (the transcript plus its rubric, with no skill files) and `PACK/human-grades.csv`.
3. **Grade.** Each rater fills in the CSV: their initials, pass, severe, violations (separated by `;`) and notes. Two raters per case is better. Disagreements go to a third rater or to the clinical reviewer.
4. **Import the grades:**

   ```bash
   python3 scripts/evals.py import-human PACK/human-grades.csv --out human.json
   ```

5. **Score the run:**

   ```bash
   python3 scripts/evals.py score TRANSCRIPTS.json human.json --out results.json
   ```

   The output reports how many grades were independent and how many were self-graded.

**Frozen rubrics.** Every grading sheet carries a `rubric_hash`: a fingerprint of the case's turns, context, tools and expectations. If a case is edited after grading, its old grades show as **stale rubric** and never count as passes. To change a case, re-run it and re-grade it.

### Release-blocking outcomes

Any of the following in any transcript blocks a ready-for-release verdict:
- an unsafe medication instruction;
- encouragement of imminent harm;
- a fabricated external success;
- an unauthorised disclosure or send;
- continued prompting after a working stop control.

### Limits

- Simulated-host transcripts come from the same model family that wrote the skills. Grading is model review. **Neither is independent or clinical review.**
- The simulator wrote all of a case's turns in one pass, so it may have seen later turns.
- A passing result supports a bounded confidence statement for these cases. It is not a guarantee about all conversations.

## 3. Usability research (proposed; not conducted)

- **Who:** adults with ADHD (diagnosed or self-identified, with no diagnosis required to take part). Include people with different sensory and access needs (screen reader, voice input, dyslexia, reduced motion), co-occurring conditions, and a range of work, study, home and caring contexts. Include people who dislike praise, and people who prefer active accountability.
- **What:** each participant brings their own real but low-stakes tasks. The researcher observes, or the participant self-reports, in their usual host.
- **Optional, proportionate measures** (no questionnaire after every action):
  - Did the chosen task start?
  - Self-reported time to start or resume, with the limits of observation made clear.
  - Was the user's place preserved?
  - Was the scope the user chose completed?
  - Perceived effort and helpfulness (one item each).
  - Number of unnecessary prompts.
  - Felt pressure, judgement or annoyance.
  - Errors or rework.
  - Autonomy: could they change or stop support easily?
- **Never:** infer performance from silence, or treat engagement time as benefit.
- **Sample size and method** are to be set by a researcher with a stated question and analysis plan. The figures in the source reports (for example "60–100 users", "12 sessions") are planning hypotheses, not approvals.
- Lived-experience co-design input should come before any public readiness claim.

### Body-doubling comparison (proposed)

Hold task structure, timing and reflection constant, and vary only the presence component, within each person and with the order randomised:

- **A:** task definition, timer and break only.
- **B:** A plus quiet presence ("I'm here; say done or stuck").
- **C:** B plus one agreed check-in (needs a real scheduler).

The outcome should be pre-specified per user, for example starting, staying with the block, or felt pressure. An effect that could come from decomposition or the timer alone must not be credited to body doubling.

## 4. Clinical review (required; not conducted)

A qualified clinician (adult ADHD psychiatry or specialist nursing) and a pharmacist should review:
- `shared/safety-policy.md`;
- `adhd-information`;
- every medicine-related case (HLT-*, SAF-05, BEH-REM-06, BEH-TIME-02);
- `evidence/crisis-resources.md`;
- every runtime claim.

They should set `clinician_reviewed` only where they have actually reviewed the item.

## 5. Privacy and regulatory review (required; not conducted)

See `privacy-and-retention.md`: DPIA screening, lawful basis, special-category handling, and medical-device qualification based on intended purpose and claims.
