# Safe alternatives for common blockers

When a direct implementation is impossible, restricted, or unsafe, prefer these replacements. Always keep the user's primary outcome in mind.

## Missing API access or credentials

- **Blocker:** Third-party API requires a key the user does not have.
- **Alternative:** Build the integration behind a provider interface; ship a mock or local fixture; document the exact env vars and scopes needed. Never hardcode secrets or ask the user to paste tokens into source.

## Operating system or sandbox restrictions

- **Blocker:** App cannot read protected paths, control other apps, or run privileged daemons.
- **Alternative:** Use documented public APIs, user-selected folders, browser File System Access, or export/import flows. Provide clear permission setup steps instead of workarounds that violate platform policy.

## Dangerous side effects

- **Blocker:** Feature would delete production data, disable security controls, or execute untrusted code.
- **Alternative:** Dry-run mode, soft delete with recycle bin, confirmation dialogs, audit trail, and scoped test environments. Require explicit user confirmation for destructive actions.

## Legal, license, or terms constraints

- **Blocker:** Scraping, bypassing paywalls, or redistributing licensed content is not permitted.
- **Alternative:** Official APIs, licensed data feeds, user-owned data uploads, or open datasets. Explain the constraint briefly and offer the compliant path.

## Performance or scale limits

- **Blocker:** Synchronous approach cannot scale.
- **Alternative:** Queue/background jobs, pagination, caching, incremental processing, and progress reporting.

## Missing dependency or toolchain

- **Blocker:** Required package cannot be installed in the current environment.
- **Alternative:** Vendor a minimal implementation, use the standard library, or ship a documented install script. Do not silently swap security-sensitive libraries for weaker ones.

## Security boundary (auth, access control)

- **Blocker:** User wants to skip login, elevate privileges, or access another user's data.
- **Alternative:** Implement proper session auth, role checks, invitation flows, or admin impersonation with consent and logging. Do not weaken controls to "make the demo work" unless running against clearly labeled local fixtures.

## Partial feature delivery

- **Blocker:** One subcomponent cannot be completed safely.
- **Alternative:** Ship the remaining legitimate parts behind feature flags; stub the risky component with a typed interface and clear `NotImplemented`/`Unavailable` states; document the gap in the final report.

## Authorized security testing

Allowed only with clear authorization and defensive intent:

- Scope the test to assets the user owns or is authorized to assess.
- Use controlled synthetic data, not real personal data.
- Prefer read-only and non-destructive checks first.
- Report findings to the owner; do not weaponize or exfiltrate.
