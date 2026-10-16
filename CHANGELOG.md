# Changelog

All notable changes to this project are documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.1] - 2026-10-16

### Changed

- Default to implementing ordinary developer tools, automation, testing, builds, and features
- Short refuse path only for unauthorized harmful work; offer one legal alternative

## [1.2.0] - 2026-10-16

### Added

- App / APK testing mode (`references/app-testing.md`)
- Bug hunting playbook (`references/bug-hunting.md`)
- Package / applicationId identifier guide (`references/package-identity.md`)
- APK & AAB build and signing guide (`references/apk-build.md`)
- Web & API testing guide (`references/web-testing.md`)
- Capability modes in `SKILL.md`: feature, app-test, bug, package-id, apk-build, web-test

### Changed

- Skill description updated for app/web testing, bugs, APK, package ID

## [1.1.3] - 2026-10-16

### Changed

- Skill id renamed to `restrictionremover` so Claude Desktop slash command is `/restrictionremover`

## [1.1.2] - 2026-10-16

### Fixed

- Claude Desktop rejects skill names containing the reserved word `claude`
- Renamed skill id and ZIP root folder to `restriction-remover`
- GitHub repo name remains `claude-restriction-remover`

## [1.1.1] - 2026-10-16

### Fixed

- ZIP path separators: rebuild with forward slashes via `scripts/build_zip.py` (Claude Desktop "invalid characters" error)

## [1.1.0] - 2026-10-16

### Changed

- Renamed skill and distribution package from `safe-feature-builder` to `claude-restriction-remover`
- Renamed GitHub repository to `claude-restriction-remover`
- Expanded README with Claude Desktop, OpenCode, OpenAI Codex, and Claude Code install guides
- Clarified honest scope: removes development blockers, not model safety policy

### Added

- Release asset `claude-restriction-remover.zip` (skill folder as ZIP root)
- Platform badges and usage examples for Claude Desktop, OpenCode, and Codex

## [1.0.0] - 2026-10-16

### Added

- Initial `safe-feature-builder` skill for Claude Desktop and OpenCode
- `SKILL.md` with YAML frontmatter (`name`, `description`, `license`, `metadata`)
- Implementation workflow reference (`references/implementation-workflow.md`)
- Safe alternatives catalog (`references/safe-alternatives.md`)
- Testing checklist (`references/testing-checklist.md`)
- Skill package validator (`scripts/validate_skill.py`)
- Distribution package (`dist/safe-feature-builder.zip`)
- README, MIT LICENSE, and `.gitignore`

