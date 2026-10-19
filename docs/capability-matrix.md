# Host compatibility matrix

Status key:
- **validated**: exercised in this build, with the result recorded.
- **documented**: matches current official documentation but was not exercised.
- **untested**: not checked.
- **unsupported**: the host cannot do it.

Documentation was accessed on 2026-10-19:
- Agent Skills specification (agentskills.io).
- Claude Code docs (latest changelog entry 2.1.303, 18 October 2026). The machine used for this build had **Claude Code 2.1.150** installed.
- Codex docs (Codex CLI 0.163.0, 15 October 2026). **Codex was not installed.**
- claude.ai help-centre pages on skills.

| Behaviour | Generic text-only host | Claude Code | Codex | claude.ai upload |
|---|---|---|---|---|
| Skill format valid (Agent Skills spec) | n/a | validated (structural validator) | validated (same files) | validated (ZIP structure, extracted and checked) |
| Plugin manifest loads | n/a | **validated**: `--plugin-dir dist/claude-code` loaded all 13 skills, namespaced `adhd-support-skills:*` | documented: root `plugin.json` plus `.agents/plugins/marketplace.json` | n/a |
| `claude plugin validate` | n/a | run with `scripts/validate.py --host-checks` (see release-readiness) | n/a | n/a |
| Natural-language selection | unsupported. Use the router instructions file and paste the skill | documented (automatic by default). Behaviour simulated, not run natively, because CLI authentication had been revoked (see release-readiness) | documented (implicit invocation on by default) | documented (auto-trigger) |
| Explicit invocation | "use the adhd-start skill" plus pasted SKILL.md | `/adhd-start`, or `/adhd-support-skills:adhd-start` for plugin installs (documented) | `$adhd-start` or `/skills` (documented) | Not documented. Describe the request instead |
| Router block in instruction file | Paste `dist/generic/ADHD-support-instructions.md` (21 KB) | `CLAUDE.md` managed block (installer **validated** in tests) | `AGENTS.md` managed block (installer **validated**; 32 KiB limit respected) | Project instructions, by hand (untested) |
| Self-contained references (`references/shared/`) | validated | validated | validated | validated |
| Bundled script (`mpot.py`) runs | needs a shell | documented (needs Bash permission) | documented | documented (code execution must be on); untested |
| Timer / notification tools | unavailable. Manual fallback | Host-dependent (none by default). Fallback **validated** in mocked harness and simulated evals | Host-dependent | Host-dependent |
| Persistent private memory | session-only plus copyable card | File-backed MPoT if the user picks a folder (**validated** in `test_mpot.py`) | Same | Session-only unless the host offers memory |
| Web retrieval | unavailable. Verified snapshot only | Host tool if enabled | Host tool if enabled | Host-dependent |
| Crisis-resource lookup | unavailable. Verified list or location-neutral guidance | No dedicated tool known | No dedicated tool known | No dedicated tool known |
| Description length | n/a | ≤1,536 characters shown (documented); ours are under 600 | Up to 2% of context for the whole list (documented) | 200 or 1,024 (conflicting docs). ZIPs use ≤200 |
| Enforced tool restrictions | none | Possible via settings (`allowed-tools` is not used by this suite) | Possible via config | none |

## Skill listing budget

Claude Code shows skill descriptions within about 1% of the context window and drops the least-used skills' descriptions first. Codex uses up to 2%. The 13 descriptions total about 6.5 KB. If many other skills are installed, some descriptions may be truncated, and natural-language selection could degrade. The router block provides a backstop.

## What would move items to "validated"

- **Claude Code native behaviour.** Run `claude auth login`, then `python3 scripts/evals.py run-claude --out results.json` followed by `score`. The runner loads only this plugin and excludes user settings, so personal plugins and hooks don't affect results.
- **Codex.** Install the Codex CLI, add `dist/codex` as a local marketplace, then repeat the routing cases.
- **claude.ai.** Upload `dist/zips/adhd-start.zip` and confirm the upload is accepted and the skill triggers on "I can't start the report".
