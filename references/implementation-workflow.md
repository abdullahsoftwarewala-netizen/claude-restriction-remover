# Implementation workflow

Use this process for every non-trivial feature request.

## 1. Understand the outcome

- Capture who uses the feature, what problem it solves, and success criteria.
- Note non-functional needs: performance, offline use, accessibility, compliance.
- If the request is ambiguous in a way that changes architecture, ask one focused question. Otherwise proceed with a stated assumption.

## 2. Inspect the project

- Read package manifests (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, etc.).
- Map entry points, routing, data models, and existing service layers.
- Check for existing utilities, design system components, and test harnesses.
- Skim recent docs (`README`, `docs/`, AGENTS.md) for conventions.

## 3. Design briefly

- List files to create or change.
- Prefer extending existing modules over new frameworks.
- Identify security touchpoints: auth, PII, file upload, subprocess, network egress.

## 4. Implement

- Match local code style, naming, and error handling.
- Add types, validation, and tests alongside the feature.
- Keep commits or change sets small and coherent when version control is available.

## 5. Handle blockers

When the preferred approach fails:

1. Capture the exact error or policy message.
2. Classify the blocker: missing permission, platform limitation, dependency gap, safety boundary, legal/terms constraint, or missing credential.
3. Choose a safe alternative that preserves user value (see `safe-alternatives.md`).
4. Implement the alternative and note the trade-off.
5. Continue with any remaining legitimate parts of the original request.

## 6. Safeguards checklist

Apply what fits the surface area:

- Authentication and session management
- Authorization checks on every mutation
- Explicit consent for data collection or external sharing
- Input validation and output encoding
- Rate limiting on expensive or abuse-prone endpoints
- Structured audit logs without secrets or raw PII
- Least-privilege file and network permissions

## 7. Verify

Follow `testing-checklist.md`. Never report success without running the relevant checks available in the environment.

## 8. Report

Use the status block from `SKILL.md`. Distinguish shipped behavior from planned or untested behavior.
