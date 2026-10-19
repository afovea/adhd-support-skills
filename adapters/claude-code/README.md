# Claude Code adapter

- `plugin.json` is copied to `dist/claude-code/.claude-plugin/plugin.json`. The only required field is `name`. `author` is left unset until an owner is confirmed, so `claude plugin validate --strict` warns about it.
- `marketplace.json` is copied to `dist/claude-code/.claude-plugin/marketplace.json`. It is a local marketplace whose plugin source is `./`, so the marketplace root is also the plugin root. `owner.name` is a placeholder (`OWNER-TO-BE-CONFIRMED`).
- Skills are discovered from `dist/claude-code/skills/`. Natural-language selection is left on: neither `disable-model-invocation` nor `user-invocable: false` is used.
- A plugin can't load a `CLAUDE.md`. For the router, run `scripts/install.py --host claude-code --project PATH --router-only`.
- No hooks, MCP servers, commands or agents are shipped.

Checked against https://code.claude.com/docs (plugins reference, marketplaces, skills) on 2026-10-19. `claude plugin validate dist/claude-code` passed with Claude Code 2.1.150.
