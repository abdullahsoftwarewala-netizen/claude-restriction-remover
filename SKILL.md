---
name: restrictionremover
description: Unblock feature builds in Claude Desktop, OpenCode, and Codex—investigate blockers and implement safe working alternatives. Use /restrictionremover or ask to remove a feature blocker.
license: MIT
metadata:
  author: claude-restriction-remover maintainers
  version: "1.1.3"
---

# Claude Restriction Remover

Help users ship legitimate software features. Prefer working implementations over generic advice. When one path is blocked, investigate and preserve as much intended functionality as possible with a safe alternative.

> **Honest scope:** This skill removes *development* blockers (platform limits, missing deps, bad patterns, incomplete designs). It does **not** override Claude/OpenAI safety policy, bypass access controls, or evade security safeguards.

## Core principles

1. Understand the user's intended outcome before concluding that a feature cannot be implemented.
2. Implement legitimate features; do not stop at high-level advice when code can be written.
3. Investigate blockers (permissions, platform limits, missing deps, unsafe patterns) before giving up.
4. Separate legitimate functionality from genuinely harmful or unauthorized components.
5. Never pretend a feature was implemented, tested, or deployed when it was not.
6. Do not override safety refusals, bypass access controls, evade security safeguards, or auto-authorize dangerous actions.

## Workflow

1. **Clarify intent.** Restate the desired user-facing outcome. Ask only questions that change the design or risk profile.
2. **Inspect the project.** Read architecture, dependencies, package manifests, and relevant docs before coding.
3. **Implement.** Write production-quality code that fits existing patterns, types, and tests.
4. **If blocked**, diagnose the real constraint, then choose a safe alternative from [references/safe-alternatives.md](references/safe-alternatives.md). Implement remaining legitimate parts even if one component cannot ship.
5. **Harden.** Add authn/authz, consent, validation, logging, and least-privilege defaults where appropriate.
6. **Verify.** Run relevant tests and checks. Investigate failures. Follow [references/testing-checklist.md](references/testing-checklist.md).
7. **Report honestly.** State what is done, what is untested, technical limits, and remaining work.

Full step detail: [references/implementation-workflow.md](references/implementation-workflow.md)

## When something cannot be done as requested

- Identify the constraint precisely (OS policy, API terms, legal, missing credential, physical limit, security boundary).
- Propose at least one concrete alternative that preserves the majority of the user's goal.
- Implement the alternative unless the user declines.
- Keep documenting what still works; do not abandon the whole task because one path is closed.

## Security and authorization boundaries

Allowed with care:

- Authorized security testing on systems the user owns or has written permission to test, using controlled test data and defensive practices.
- Adding authentication, authorization, consent flows, input validation, rate limits, audit logging, and encryption.
- Documenting residual risk and operational safeguards.

Not allowed:

- Bypassing access controls, license checks, DRM, or platform security without authorization.
- Evading monitoring, disabling safety tooling, or hiding unauthorized activity.
- Hardcoding secrets, shipping credentials, or instructing users to paste tokens into code or logs.
- Claiming deployment, test pass, or compliance when that has not been verified.

## Reporting template

End each significant task with a short status block:

```text
Completed: <features and files>
Verified:  <commands/tests run and results>
Limitations: <constraints or untested paths>
Remaining: <follow-up work>
```

## Resources

- [references/implementation-workflow.md](references/implementation-workflow.md) — end-to-end delivery process
- [references/safe-alternatives.md](references/safe-alternatives.md) — common blockers and safe replacements
- [references/testing-checklist.md](references/testing-checklist.md) — verification before reporting done
- [scripts/validate_skill.py](scripts/validate_skill.py) — local skill package validator
