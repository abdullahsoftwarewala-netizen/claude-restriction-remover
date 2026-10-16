#!/usr/bin/env python3
"""Validate an Agent Skills / Claude Desktop skill package.

Checks SKILL.md frontmatter, metadata, naming, description length,
referenced files, secret patterns, and optional ZIP layout.

Usage:
  python validate_skill.py [path/to/skill-dir]
  python validate_skill.py --zip path/to/skill.zip
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - stdlib fallback
    yaml = None


NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME_LEN = 64
# Claude Desktop docs: description max 200 characters.
# Agent Skills spec allows 1024; we enforce the stricter product limit.
MAX_DESC_LEN_CLAUDE_DESKTOP = 200
MAX_DESC_LEN_AGENT_SKILLS = 1024

SECRET_PATTERNS = [
    (re.compile(r"ghp_[A-Za-z0-9]{20,}"), "GitHub personal access token (ghp_*)"),
    (re.compile(r"github_pat_[A-Za-z0-9_]{20,}"), "GitHub fine-grained PAT (github_pat_*)"),
    (re.compile(r"gho_[A-Za-z0-9]{20,}"), "GitHub OAuth token (gho_*)"),
    (re.compile(r"ghs_[A-Za-z0-9]{20,}"), "GitHub server token (ghs_*)"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key ID (AKIA*)"),
    (re.compile(r"sk-[A-Za-z0-9]{20,}"), "OpenAI-style secret key (sk-*)"),
    (re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"), "Slack token"),
    (re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"), "Private key block"),
    (re.compile(r"(?i)(?:api[_-]?key|secret|password|token)\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
     "Hardcoded credential assignment"),
]

TEXT_SUFFIXES = {
    ".md", ".py", ".txt", ".json", ".yml", ".yaml", ".sh", ".ps1",
    ".js", ".ts", ".toml", ".cfg", ".ini", ".env",
}


class Result:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.passed: list[str] = []

    def ok(self, msg: str) -> None:
        self.passed.append(msg)

    def err(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def parse_frontmatter(text: str) -> tuple[dict[str, Any] | None, str, list[str]]:
    """Return (meta, body, parse_errors). Frontmatter must start at first byte."""
    errors: list[str] = []
    if not text.startswith("---"):
        errors.append("SKILL.md must start with YAML frontmatter '---' at the first byte (no BOM, no leading whitespace).")
        return None, text, errors

    if text.startswith("﻿"):
        errors.append("SKILL.md begins with a UTF-8 BOM; remove it so frontmatter starts at byte 0.")
        text = text.lstrip("﻿")

    lines = text.splitlines(keepends=True)
    # first line should be exactly ---
    if lines[0].strip() != "---":
        errors.append("First line of SKILL.md must be exactly '---'.")
        return None, text, errors

    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() in ("---", "..."):
            end_idx = i
            break
    if end_idx is None:
        errors.append("YAML frontmatter closing '---' not found.")
        return None, text, errors

    yaml_text = "".join(lines[1:end_idx])
    body = "".join(lines[end_idx + 1 :])

    if yaml is not None:
        try:
            meta = yaml.safe_load(yaml_text)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"Invalid YAML frontmatter: {exc}")
            return None, body, errors
    else:
        meta = {}
        current_nested: str | None = None
        for raw in yaml_text.splitlines():
            if not raw.strip() or raw.lstrip().startswith("#"):
                continue
            if ":" not in raw:
                errors.append(f"Cannot parse frontmatter line (PyYAML unavailable and line not key:value): {raw!r}")
                continue
            indent = len(raw) - len(raw.lstrip(" "))
            key, _, value = raw.strip().partition(":")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if indent == 0:
                if value == "":
                    current_nested = key
                    meta[key] = {}
                else:
                    current_nested = None
                    meta[key] = value
            elif current_nested is not None and isinstance(meta.get(current_nested), dict):
                meta[current_nested][key] = value
            else:
                meta[key] = value

    if not isinstance(meta, dict):
        errors.append("YAML frontmatter must be a mapping of keys to values.")
        return None, body, errors

    return meta, body, errors


def validate_meta(meta: dict[str, Any], dir_name: str, result: Result, strict_desktop: bool) -> None:
    if "name" not in meta or not str(meta.get("name") or "").strip():
        result.err("Required frontmatter field 'name' is missing or empty.")
    else:
        name = str(meta["name"]).strip()
        if len(name) > MAX_NAME_LEN:
            result.err(f"'name' exceeds {MAX_NAME_LEN} characters ({len(name)}).")
        elif not NAME_PATTERN.match(name):
            result.err(
                f"'name' must be lowercase alphanumeric with single hyphens "
                f"(^[a-z0-9]+(-[a-z0-9]+)*$); got {name!r}."
            )
        else:
            result.ok(f"Valid name: {name}")
        if name != dir_name:
            result.err(f"'name' ({name!r}) must match the skill directory name ({dir_name!r}).")
        else:
            result.ok("Name matches directory name.")

    if "description" not in meta or not str(meta.get("description") or "").strip():
        result.err("Required frontmatter field 'description' is missing or empty.")
    else:
        desc = str(meta["description"]).strip()
        limit = MAX_DESC_LEN_CLAUDE_DESKTOP if strict_desktop else MAX_DESC_LEN_AGENT_SKILLS
        if len(desc) < 1:
            result.err("'description' must be non-empty.")
        elif len(desc) > limit:
            result.err(f"'description' is {len(desc)} characters; limit is {limit}.")
        else:
            result.ok(f"Valid description ({len(desc)} chars, limit {limit}).")

    if "license" in meta and meta["license"] is not None:
        result.ok(f"Optional license present: {meta['license']}")

    if "metadata" in meta and meta["metadata"] is not None and not isinstance(meta["metadata"], dict):
        result.err("'metadata' must be a key-value mapping.")


def check_referenced_files(body: str, skill_dir: Path, result: Result) -> None:
    # Markdown links and bare relative paths one level deep
    link_re = re.compile(r"\[[^\]]*\]\(([^)#\s]+)\)")
    refs = set(link_re.findall(body))
    for token in re.findall(r"(?<![(\w])(references/[\w./-]+|scripts/[\w./-]+|assets/[\w./-]+)", body):
        refs.add(token)

    for ref in sorted(refs):
        if ref.startswith(("http://", "https://", "mailto:")):
            continue
        target = (skill_dir / ref).resolve()
        try:
            target.relative_to(skill_dir.resolve())
        except ValueError:
            result.warn(f"Reference escapes skill directory: {ref}")
            continue
        if target.exists():
            result.ok(f"Referenced file exists: {ref}")
        else:
            result.err(f"Referenced file missing: {ref}")


def check_secrets_in_text(text: str, label: str, result: Result) -> None:
    for pattern, label_secret in SECRET_PATTERNS:
        if pattern.search(text):
            result.err(f"Possible secret in {label}: {label_secret}")


def check_structure(skill_dir: Path, result: Result) -> None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        result.err("SKILL.md not found in skill directory.")
        return
    try:
        raw = skill_md.read_bytes()
    except OSError as exc:
        result.err(f"Cannot read SKILL.md: {exc}")
        return

    if raw.startswith(b"\xef\xbb\xbf"):
        result.err("SKILL.md has a UTF-8 BOM; save as UTF-8 without BOM.")
        raw = raw[3:]

    try:
        text = raw.decode("utf-8")
        result.ok("SKILL.md is valid UTF-8.")
    except UnicodeDecodeError as exc:
        result.err(f"SKILL.md is not valid UTF-8: {exc}")
        return

    check_secrets_in_text(text, "SKILL.md", result)

    meta, body, fm_errors = parse_frontmatter(text)
    for e in fm_errors:
        result.err(e)
    if meta is None:
        return

    validate_meta(meta, skill_dir.name, result, strict_desktop=True)

    # Optional markdown sanity
    if not body.strip():
        result.warn("SKILL.md body after frontmatter is empty.")
    else:
        result.ok("SKILL.md has a Markdown body.")

    check_referenced_files(body, skill_dir, result)

    # Scan other text files for secrets
    for path in skill_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name != "SKILL.md":
            continue
        if path.name == "SKILL.md":
            continue
        if "dist" in path.parts or ".git" in path.parts:
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        check_secrets_in_text(content, str(path.relative_to(skill_dir)), result)


def check_zip(zip_path: Path, expected_root: str, result: Result) -> None:
    if not zip_path.is_file():
        result.err(f"ZIP not found: {zip_path}")
        return
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            names = zf.namelist()
            bad = zf.testzip()
            if bad is not None:
                result.err(f"ZIP is corrupt at member: {bad}")
                return
            result.ok(f"ZIP opens and passes CRC check ({len(names)} members).")

            expected_prefix = expected_root + "/"
            if not any(n == expected_root + "/SKILL.md" or n == expected_root + "/skill.md" for n in names):
                # Claude Desktop: skill folder as root of ZIP
                if any(n.endswith("SKILL.md") or n.endswith("skill.md") for n in names):
                    result.err(
                        "ZIP must contain the skill folder as its root "
                        f"(expected {expected_prefix}SKILL.md)."
                    )
                else:
                    result.err("ZIP does not contain SKILL.md.")
            else:
                result.ok(f"ZIP root structure OK: {expected_prefix}SKILL.md present.")

            for info in zf.infolist():
                if info.filename.startswith("/") or ".." in info.filename.split("/"):
                    result.err(f"Unsafe ZIP member path: {info.filename}")
    except zipfile.BadZipFile as exc:
        result.err(f"Invalid ZIP file: {exc}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a skill package.")
    parser.add_argument("path", nargs="?", default=".", help="Skill directory (default: .)")
    parser.add_argument("--zip", dest="zip_path", help="Also validate a distribution ZIP")
    args = parser.parse_args(argv)

    skill_dir = Path(args.path).resolve()
    if not skill_dir.is_dir():
        print(f"ERROR: not a directory: {skill_dir}", file=sys.stderr)
        return 2

    result = Result()
    print(f"Validating skill directory: {skill_dir}")
    check_structure(skill_dir, result)

    if args.zip_path:
        check_zip(Path(args.zip_path).resolve(), skill_dir.name, result)

    for msg in result.passed:
        print(f"  PASS  {msg}")
    for msg in result.warnings:
        print(f"  WARN  {msg}")
    for msg in result.errors:
        print(f"  ERROR {msg}")

    print()
    print(f"Summary: {len(result.passed)} passed, {len(result.warnings)} warnings, {len(result.errors)} errors")
    return 1 if result.errors else 0


if __name__ == "__main__":
    sys.exit(main())
