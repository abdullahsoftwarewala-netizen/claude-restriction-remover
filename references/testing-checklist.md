# Testing checklist

Run what the project supports. Mark anything skipped as untested in the final report.

## Before claiming a feature works

- [ ] Feature builds or type-checks without new errors
- [ ] Relevant unit or integration tests pass
- [ ] New behavior has tests or a documented manual test script
- [ ] Lint/format checks pass if configured
- [ ] No secrets, tokens, or personal data committed
- [ ] Error paths return safe messages (no stack traces to end users, no leaked internals)
- [ ] Auth/permission checks cover the new surface
- [ ] Destructive actions require confirmation or are dry-run first

## Commands to try (adapt to the project)

```bash
# JavaScript / TypeScript
npm test
npm run build
npm run lint

# Python
pytest
python -m compileall .

# Go
go test ./...
go build ./...

# Rust
cargo test
cargo build
```

If a command is unavailable, say so. Do not invent results.

## Manual verification

- Happy path through the real UI or CLI entry point
- Empty and invalid inputs
- Unauthorized user or missing credential path
- Concurrent or repeated submission (idempotency where relevant)
- Cleanup of test artifacts

## Report integrity

- Only list tests that were actually run
- Separate "passed", "failed", and "not run"
- Note environment limits (no network, missing runtime, Windows/macOS/Linux differences)
