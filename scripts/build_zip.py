#!/usr/bin/env python3
"""Build dist/<skill>.zip with forward-slash paths for Claude Desktop upload.

Usage:
  python scripts/build_zip.py
  python scripts/build_zip.py --out /tmp/custom.zip
"""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

# Skill root folder name inside the ZIP (must match SKILL.md `name`)
SKILL_NAME = "claude-restriction-remover"
INCLUDE_FILES = {
    "SKILL.md",
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    ".gitignore",
}
INCLUDE_DIRS = {
    "references",
    "scripts",
}


def build(skill_root: Path, out_path: Path) -> None:
    skill_md = skill_root / "SKILL.md"
    if not skill_md.is_file():
        raise SystemExit(f"Missing {skill_md}")

    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise SystemExit("SKILL.md must start with YAML frontmatter at byte 0")
    if "name:" not in text.split("---")[1]:
        raise SystemExit("Frontmatter missing name")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists():
        out_path.unlink()

    files: list[Path] = []
    for name in sorted(INCLUDE_FILES):
        p = skill_root / name
        if p.is_file():
            files.append(p)
    for dname in sorted(INCLUDE_DIRS):
        d = skill_root / dname
        if d.is_dir():
            for p in sorted(d.rglob("*")):
                if p.is_file():
                    files.append(p)

    with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            rel = path.relative_to(skill_root).as_posix()  # forward slashes
            arc = f"{SKILL_NAME}/{rel}"
            if "\\" in arc:
                raise RuntimeError(f"backslash in archive path: {arc}")
            zf.writestr(arc, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED)

    with zipfile.ZipFile(out_path) as zf:
        if zf.testzip() is not None:
            raise SystemExit("ZIP CRC check failed")
        names = zf.namelist()
        required = f"{SKILL_NAME}/SKILL.md"
        if required not in names:
            raise SystemExit(f"ZIP missing {required}")
        for n in names:
            if "\\" in n or n.startswith("/"):
                raise SystemExit(f"Invalid ZIP path: {n!r}")

    print(f"Built: {out_path} ({out_path.stat().st_size} bytes)")
    with zipfile.ZipFile(out_path) as zf:
        for n in zf.namelist():
            print(f"  {n}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parents[1]),
        help="Skill directory (default: repo root)",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Output ZIP path (default: dist/<skill>.zip)",
    )
    args = parser.parse_args()
    root = Path(args.root).resolve()
    out = Path(args.out).resolve() if args.out else root / "dist" / f"{SKILL_NAME}.zip"
    build(root, out)


if __name__ == "__main__":
    main()
