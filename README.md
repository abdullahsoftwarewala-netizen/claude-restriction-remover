# safe-feature-builder

A reusable **Claude Desktop** and **OpenCode** skill for implementing legitimate software features, investigating blockers, and developing safe, functional alternatives.

## What it does

When enabled, this skill guides Claude to:

1. Understand the user's intended outcome before declaring a feature impossible.
2. Inspect the existing project, architecture, dependencies, and docs.
3. Implement legitimate features with production-quality code—not generic advice alone.
4. Diagnose technical blockers and implement practical safe alternatives.
5. Preserve as much intended functionality as possible when one path is closed.
6. Apply authentication, authorization, consent, validation, and logging where appropriate.
7. Run relevant tests and report completed work, limitations, and remaining tasks honestly.

## What it does not do

- It does not override safety refusals or bypass access controls.
- It does not evade security safeguards or auto-authorize dangerous actions.
- It does not claim features were implemented or tested when they were not.

Its purpose is to find the **best legitimate implementation**, not to abandon an entire task unnecessarily.

## Repository layout

```text
safe-feature-builder/
├── SKILL.md                          # Skill entrypoint (YAML frontmatter + instructions)
├── README.md
├── LICENSE
├── CHANGELOG.md
├── .gitignore
├── references/
│   ├── implementation-workflow.md    # End-to-end delivery process
│   ├── safe-alternatives.md          # Common blockers and safe replacements
│   └── testing-checklist.md          # Verification before reporting done
├── scripts/
│   └── validate_skill.py             # Local skill package validator
└── dist/
    └── safe-feature-builder.zip      # Claude Desktop upload package
```

## Install in Claude Desktop

1. Enable **Code execution and file creation** in [Settings > Capabilities](https://claude.ai/settings/capabilities).
2. Open [Customize > Skills](https://claude.ai/customize/skills).
3. Click **+**, then **+ Create skill** → **Upload a skill**.
4. Upload `dist/safe-feature-builder.zip` from a release or local build.
5. Toggle the skill **on**.
6. Test with a prompt such as: `Use safe-feature-builder to add rate limiting to this API endpoint.`

The ZIP contains the skill folder as its root (`safe-feature-builder/SKILL.md`), matching Claude Desktop's documented packaging requirements.

## Install in OpenCode

Global (all projects):

```bash
# Linux / macOS
mkdir -p ~/.config/opencode/skills
# Extract so that this path exists:
# ~/.config/opencode/skills/safe-feature-builder/SKILL.md

# Windows (PowerShell)
New-Item -ItemType Directory -Force "$env:USERPROFILE\.config\opencode\skills"
# Extract so that this path exists:
# %USERPROFILE%\.config\opencode\skills\safe-feature-builder\SKILL.md
```

Project-local:

```bash
# From your project root
mkdir -p .opencode/skills
# Extract the release ZIP into .opencode/skills/ so that:
# .opencode/skills/safe-feature-builder/SKILL.md exists
```

Restart OpenCode (or start a new session). The skill is advertised as `safe-feature-builder` when relevant. Load it explicitly with `@safe-feature-builder` or by mentioning the skill name in a prompt.

OpenCode also discovers skills under `~/.claude/skills` and project `.claude/skills` for compatibility.

## Validate locally

Requires Python 3.10+.

```bash
python scripts/validate_skill.py .
# or
python scripts/validate_skill.py --zip dist/safe-feature-builder.zip
```

The validator checks YAML frontmatter, required metadata, naming rules, description length, referenced files, ZIP layout, and scans for common secret patterns.

## Build the distribution ZIP

From the repository root:

```bash
python scripts/validate_skill.py .
```

Then re-create the ZIP with the skill directory as the archive root:

```powershell
# PowerShell example (Windows)
Compress-Archive -Path safe-feature-builder -DestinationPath dist\safe-feature-builder.zip -Force
```

```bash
# Bash example (run from parent directory of the skill folder)
zip -r safe-feature-builder/dist/safe-feature-builder.zip safe-feature-builder \
  -x "safe-feature-builder/dist/*" "safe-feature-builder/.git/*"
```

## License

MIT — see [LICENSE](LICENSE).

## Changelog

See [CHANGELOG.md](CHANGELOG.md).
