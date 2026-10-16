[![Release](https://img.shields.io/github/v/release/abdullahsoftwarewala-netizen/claude-restriction-remover?filter=v*&label=release&color=0A84FF)](https://github.com/abdullahsoftwarewala-netizen/claude-restriction-remover/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Claude Desktop](https://img.shields.io/badge/Claude%20Desktop-skill%20ZIP-0A84FF?logo=claude&logoColor=white)](https://github.com/abdullahsoftwarewala-netizen/claude-restriction-remover/releases/latest)
[![OpenCode](https://img.shields.io/badge/OpenCode-compatible-111111?logo=opencode&logoColor=white)](https://dev.opencode.ai/v2/docs/skills/)
[![Codex](https://img.shields.io/badge/OpenAI%20Codex-compatible-10A37F?logo=openai&logoColor=white)](https://www.mintlify.com/openai/codex/features/skills)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-SKILL.md-6C5CE7)](https://agentskills.io)

# Claude Restriction Remover

**When your AI coding agent hits a wall, this skill finds the working path — and ships the code.**

Claude, OpenCode, and Codex often refuse or stall on legitimate features because of a *technical* blocker: missing permission, sandbox limit, bad API design, incomplete architecture, or an unsafe pattern that can be redesigned safely. **Claude Restriction Remover** teaches the agent to diagnose the real constraint, keep the user’s goal, and implement a safe, production-ready alternative — instead of abandoning the whole task.

> It does **not** bypass Claude/OpenAI safety policy, DRM, or access controls. It removes *development* restrictions, not *security* restrictions.

[Download ZIP](https://github.com/abdullahsoftwarewala-netizen/claude-restriction-remover/releases/download/v1.1.0/claude-restriction-remover.zip) · [Latest release](https://github.com/abdullahsoftwarewala-netizen/claude-restriction-remover/releases) · [Report an issue](https://github.com/abdullahsoftwarewala-netizen/claude-restriction-remover/issues)

---

## Why

| Without the skill | With this skill |
|---|---|
| “I can’t implement that” | Diagnoses *why*, then ships a safe alternative |
| Generic advice, no code | Implements the feature in your real project |
| One blocked component kills the whole task | Ships every legitimate part; stubs only the risky piece |
| No verification | Runs tests and reports **Completed / Verified / Limitations / Remaining** |

## What the agent will do

1. **Understand the outcome** before declaring anything impossible  
2. **Inspect** architecture, dependencies, and docs  
3. **Implement** legitimate features with production-quality code  
4. **Investigate blockers** and apply safe alternatives from the bundled playbook  
5. **Harden** with auth, validation, consent, and logging where appropriate  
6. **Verify** with real tests — never fake a green build  
7. **Report** honestly what shipped and what did not  

Full playbook lives in [`SKILL.md`](SKILL.md) and [`references/`](references/).

---

## Install

### A. Claude Desktop (recommended)

Claude Desktop only accepts skill uploads through the UI — there is no CLI install into your account.

1. Open [claude.ai](https://claude.ai) (or the Claude Desktop app) and sign in.
2. Confirm **Code execution and file creation** is on:  
   [Settings → Capabilities](https://claude.ai/settings/capabilities)
3. Open **[Customize → Skills](https://claude.ai/customize/skills)**.
4. Click **+** → **+ Create skill** → **Upload a skill**.
5. Upload the release ZIP:  
   **[claude-restriction-remover.zip](https://github.com/abdullahsoftwarewala-netizen/claude-restriction-remover/releases/download/v1.1.0/claude-restriction-remover.zip)**  
   The ZIP root is the folder `claude-restriction-remover/` containing `SKILL.md` (required packaging shape).
6. Toggle the skill **ON** in the skills list.
7. **Test availability** in a new chat:

   ```text
   Use claude-restriction-remover to add rate limiting to this Express endpoint
   without breaking existing tests.
   ```

   If Claude loads the skill, you will see it referenced in the model’s tool/skill activity. If not, re-check the toggle and that code execution is enabled.

**Team/Enterprise:** owners can provision the skill org-wide under [Organization settings → Plugins & skills](https://claude.ai/admin-settings/skills).

### B. OpenCode

OpenCode discovers `SKILL.md` under global and project skill roots ([docs](https://dev.opencode.ai/v2/docs/skills/)).

**Global (all projects)**

```bash
# Linux / macOS
mkdir -p ~/.config/opencode/skills
unzip claude-restriction-remover.zip -d ~/.config/opencode/skills/
# Expected: ~/.config/opencode/skills/claude-restriction-remover/SKILL.md

# Windows (PowerShell)
New-Item -ItemType Directory -Force "$env:USERPROFILE\.config\opencode\skills"
Expand-Archive .\claude-restriction-remover.zip -DestinationPath "$env:USERPROFILE\.config\opencode\skills" -Force
# Expected: %USERPROFILE%\.config\opencode\skills\claude-restriction-remover\SKILL.md
```

**Project-only**

```bash
mkdir -p .opencode/skills
unzip claude-restriction-remover.zip -d .opencode/skills/
# Expected: .opencode/skills/claude-restriction-remover/SKILL.md
```

**Compatibility paths** (also scanned by OpenCode):

- `~/.claude/skills/claude-restriction-remover/SKILL.md`
- `.claude/skills/claude-restriction-remover/SKILL.md`

Restart OpenCode (new session). Invoke:

```text
@claude-restriction-remover add WebSocket auth to this chat feature
```

Or mention the skill naturally; OpenCode advertises it when the description matches.

### C. OpenAI Codex (CLI)

Codex stores skills in `$CODEX_HOME/skills/` (usually `~/.codex/skills/`) and project `.codex/skills/` ([skills docs](https://www.mintlify.com/openai/codex/features/skills)).

**Manual install**

```bash
# Linux / macOS
mkdir -p ~/.codex/skills
unzip claude-restriction-remover.zip -d ~/.codex/skills/
# Expected: ~/.codex/skills/claude-restriction-remover/SKILL.md

# Windows (PowerShell)
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills"
Expand-Archive .\claude-restriction-remover.zip -DestinationPath "$env:USERPROFILE\.codex\skills" -Force
```

**Via Codex skill-installer** (inside a Codex session):

```text
/use skill-installer
Install the skill from github.com/abdullahsoftwarewala-netizen/claude-restriction-remover
```

Then **restart Codex**. Invoke:

```text
/use claude-restriction-remover
Implement file upload with virus-scan hook; if the AV API is unavailable, use a safe local validation path.
```

### D. Claude Code / manual (any Agent Skills host)

```bash
git clone https://github.com/abdullahsoftwarewala-netizen/claude-restriction-remover.git
# Claude Code project skills:
mkdir -p .claude/skills
cp -r claude-restriction-remover .claude/skills/claude-restriction-remover
# Or validate the ZIP yourself:
python claude-restriction-remover/scripts/validate_skill.py claude-restriction-remover \
  --zip claude-restriction-remover/dist/claude-restriction-remover.zip
```

---

## How to use it

Once enabled, talk to the agent like a senior engineer — not like a magic prompt:

| Say this | The skill does this |
|---|---|
| “Add SSO, but our IdP only supports SAML and the app is OIDC-only.” | Maps a safe bridge (e.g. proxy / library) and implements it with tests |
| “This feature needs admin on macOS; App Store build forbids it.” | Detects the sandbox limit and ships a user-consented alternative |
| “Rate-limit login without breaking the existing auth middleware.” | Extends the current stack; keeps every legitimate path working |
| “If one integration can’t ship, still finish the rest of the dashboard.” | Ships the rest; stubs only the blocked integration with a typed interface |

**Good prompt pattern**

```text
Use claude-restriction-remover.
Goal: <user-visible outcome>
Constraints: <platform, permissions, offline, compliance>
If blocked: diagnose, propose a safe alternative, implement it, run tests,
then report Completed / Verified / Limitations / Remaining.
```

**Example test prompts (after install)**

1. Claude Desktop: `Use claude-restriction-remover to implement dark-mode toggle that persists, but localStorage is blocked in our iframe — find a safe alternative.`  
2. OpenCode: `@claude-restriction-remover add CSV export; the server has no filesystem write permission — keep the feature working in-browser.`  
3. Codex: `/use claude-restriction-remover` then ask for a feature that needs a tool your CI sandbox disallows.

---

## Package layout

```text
claude-restriction-remover/
├── SKILL.md                          # Agent entrypoint (YAML + instructions)
├── README.md
├── LICENSE
├── CHANGELOG.md
├── .gitignore
├── references/
│   ├── implementation-workflow.md
│   ├── safe-alternatives.md
│   └── testing-checklist.md
├── scripts/
│   └── validate_skill.py
└── dist/
    └── claude-restriction-remover.zip
```

## Validate before you trust a copy

```bash
python scripts/validate_skill.py . --zip dist/claude-restriction-remover.zip
```

Checks: frontmatter at byte 0, `name`/`description`, directory-name match, description length (≤200 for Claude Desktop), referenced files, ZIP root shape, secret patterns.

## Limits (read this)

- Cannot and will not override model safety training or product policy  
- Cannot grant OS permissions, API keys, or enterprise IdP access for you  
- Cannot claim tests passed if the environment could not run them  

## License

MIT — see [LICENSE](LICENSE).

---

**Star the repo** if this unblocked a real feature for you:  
https://github.com/abdullahsoftwarewala-netizen/claude-restriction-remover
