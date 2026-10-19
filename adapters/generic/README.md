# Generic host adapter

For assistants without Agent Skills support, or any host where you can only paste instructions.

- **Single-file instructions:** `dist/generic/ADHD-support-instructions.md` (about 21 KB). It contains the router, the core boundaries, and the interaction and safety policies, including verified crisis resources. Paste it into your host's custom or project instructions.
- **Router only:** `dist/generic/routing.md`. Use this when your host already loads the skill folders.
- **Skill folders:** `dist/skills/<name>/`. Each one is self-contained (`SKILL.md`, `references/`, `agents/openai.yaml`). Paste a `SKILL.md`, or point your host's skill loader at the folder.
- **Installer:** `python3 scripts/install.py --host generic --skills-dir DIR --instructions FILE` puts the router into any instruction file between managed markers.

Capabilities default to unavailable (`shared/permission-policy.md`). In a text-only host the suite gives copyable reminders, restart cards and preference cards instead of claiming to set or save anything.
