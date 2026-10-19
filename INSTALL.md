# Installing ADHD Support Skills

Choose the route that matches the app you use. Nothing is installed globally unless you choose a personal install. No route turns on memory, reminders or telemetry.

The ready-made files are in `dist/`. If you have the source repository, rebuild them first with `python3 scripts/build.py dist`.

## No terminal: ChatGPT (custom GPT or Project)

1. Open `dist/generic/ADHD-support-instructions-compact.md` (about 6,500 characters) and copy all of it.
2. In ChatGPT, create a GPT (**Explore GPTs → Create → Configure**) and paste it into **Instructions**, or paste it into a Project's instructions.
3. Optional: upload the full `dist/generic/ADHD-support-instructions.md` and a few `dist/skills/*/SKILL.md` files as Knowledge, for deeper behaviour.

The compact file keeps the core safety rules verbatim, plus the urgent-safety, medicine, controls and tool-honesty essentials. It is built and checked automatically, but it is **not yet tested inside ChatGPT**; the ChatGPT menu names above may also differ on your plan. Use `site-plan/study-0-chatgpt-test-log.md` to test it.

## No terminal: any assistant (manual route)

1. Open `dist/generic/ADHD-support-instructions.md` and copy all of it.
2. Paste it into your assistant's custom instructions or project instructions. For example, a Claude Project's instructions, a ChatGPT custom GPT's instructions, or your app's "system prompt" field.
3. For deeper help with one thing, also paste that skill's `SKILL.md` from `dist/skills/<name>/`. For example, `dist/skills/adhd-start/SKILL.md` for getting started.

Then talk normally: "I can't start my report."

Without a skills feature, your assistant can't automatically load the detailed skill files, so pasted instructions are a lighter version. The safety rules and controls are included in the single file.

## No terminal: claude.ai (upload skills)

1. In claude.ai, go to **Customize → Skills → + → Upload a skill**. Code execution must be turned on.
2. Upload a ZIP from `dist/zips/`, for example `adhd-start.zip`. Each ZIP contains one skill folder.
3. Repeat for each skill you want. `adhd-help` is a good first choice.

Upload is **untested** in this build. The ZIP descriptions are kept to 200 characters or fewer to meet the stricter limit shown in the help centre.

## Claude Code

**Option A: plugin, for this session only (safe to try):**

```bash
claude --plugin-dir "dist/claude-code"
```

**Option B: plugin from GitHub** (needs access while the repository is private):

```
/plugin marketplace add afovea/adhd-support-skills
```

```
/plugin install adhd-support-skills@adhd-support-skills
```

**Option B2: plugin, installed from the local marketplace in a clone:**

```bash
claude plugin marketplace add ./dist/claude-code
```

```bash
claude plugin install adhd-support-skills@adhd-support-skills-local
```

Skills are then namespaced, for example `/adhd-support-skills:adhd-start`. A plugin can't add the router to your `CLAUDE.md`. If you want it, run the installer with `--router-only` (below).

**Option C: copy into one project, with the router (dry run first):**

```bash
python3 scripts/install.py --host claude-code --project /path/to/project --dry-run
```

```bash
python3 scripts/install.py --host claude-code --project /path/to/project
```

This copies the skills to `.claude/skills/` and adds the router between `<!-- adhd-support-skills:start -->` and `<!-- adhd-support-skills:end -->` in `CLAUDE.md`. The rest of the file is left untouched.

**Option D: personal install (every project, skills only):**

```bash
python3 scripts/install.py --host claude-code --personal
```

Add `--with-router` only if you want the router in `~/.claude/CLAUDE.md`, where it would apply to every project.

## Codex

```bash
python3 scripts/install.py --host codex --project /path/to/project
```

This puts the skills in `.agents/skills/` and the router in `AGENTS.md`. Use `--personal` to install into `~/.agents/skills`. Codex can also use `dist/codex` as a plugin and local marketplace (`codex plugin marketplace add ./dist/codex`). The plugin route is **untested**, because Codex wasn't available in the build environment. Invoke a skill with `$adhd-start`, or just ask in ordinary words.

## Other skill-aware hosts

```bash
python3 scripts/install.py --host generic --skills-dir /path/to/skills --instructions /path/to/instructions.md
```

## Update, check, remove

Run the same install command again to update. Files you've edited are kept and reported; add `--force` to replace them.

To check what's installed:

```bash
python3 scripts/install.py --host claude-code --project /path/to/project --verify
```

To remove it:

```bash
python3 scripts/install.py --host claude-code --project /path/to/project --uninstall
```

Uninstall removes only the files this tool installed and that you haven't changed, plus the managed router block. It never touches your other skills, the rest of your instruction file, or any My Point of Truth folder.

## Turning on memory (optional)

Memory is off by default. To keep preferences between sessions, ask the agent ("turn on memory"). Choose a private folder **outside** any project or repository, for example a folder in your home directory. The agent will explain what is stored. With a shell, the bundled tool does it:

```bash
python3 dist/skills/my-point-of-truth/scripts/mpot.py --store ~/Private/mpot init
```

To delete it all, ask "reset my memory", or delete the folder yourself.

## Troubleshooting

- **The skills don't seem to trigger.** Name one directly (`/adhd-start`), or install the router block. If you have many other skills installed, some descriptions may be cut from the listing.
- **The installer says a skill folder "was not installed by this tool".** You already have a skill with that name. Rename or remove it, then re-run.
- **"Built bundle not found".** Run `python3 scripts/build.py dist` in the source repository.
