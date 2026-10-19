# Codex adapter

- `plugin.json` is copied to `dist/codex/plugin.json`. Codex docs currently prefer a root `plugin.json`, with `.codex-plugin/plugin.json` only as a fallback.
- `marketplace.json` is copied to `dist/codex/.agents/plugins/marketplace.json`. It is a local marketplace: the source path is `./`, `policy.installation` is AVAILABLE, and `category` is Productivity.
- Each skill has `agents/openai.yaml` with `interface.display_name`, `short_description` and `default_prompt`. `policy.allow_implicit_invocation` is deliberately absent, so it keeps its default of true and implicit selection stays on.
- Project route: `scripts/install.py --host codex --project PATH` copies the skills to `.agents/skills/` and adds the router to `AGENTS.md`. The single-file instructions are under the 32 KiB `project_doc_max_bytes` default.

Checked against the Codex docs (learn.chatgpt.com, redirected from developers.openai.com/codex) on 2026-10-19, for Codex CLI 0.163.0. **Not exercised:** Codex was not installed in the build environment.
