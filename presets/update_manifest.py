#!/usr/bin/env python3
"""Rebuild presets/manifest.json from the preset JSON files beside this script."""
from __future__ import annotations
import json
import os
import re
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "manifest.json"


def natural_key(name: str):
    return [int(part) if part.isdigit() else part.casefold() for part in re.split(r"(\d+)", name)]


def display_name(path: Path) -> str:
    # The filename is the public catalog name. Portable preset documents may
    # contain an older internal `name` left over from before the file was renamed.
    return path.stem


def validate_preset(path: Path) -> None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"ERROR: invalid JSON: {path.name}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"ERROR: preset must contain a JSON object: {path.name}")


def existing_metadata() -> dict:
    if not MANIFEST.exists():
        return {}
    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def main() -> int:
    files = sorted(
        (p for p in HERE.iterdir()
         if p.is_file() and p.suffix.lower() == ".json" and p.name.lower() != "manifest.json" and not p.name.startswith(".")),
        key=lambda p: natural_key(p.name),
    )
    for path in files:
        validate_preset(path)

    old = existing_metadata()
    manifest = {
        "format": "huff-preset-manifest",
        "version": 1,
        "repository": old.get("repository", "schwwaaa/huff-web"),
        "branch": old.get("branch", "main"),
        "presets": [
            {"file": path.name, "name": display_name(path)}
            for path in files
        ],
    }

    rendered = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    previous = MANIFEST.read_text(encoding="utf-8") if MANIFEST.exists() else None
    if previous == rendered:
        print(f"manifest.json already matches {len(files)} preset files.")
        return 0

    fd, tmp_name = tempfile.mkstemp(prefix=".manifest-", suffix=".json", dir=HERE)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(rendered)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp_name, MANIFEST)
    finally:
        try:
            os.unlink(tmp_name)
        except FileNotFoundError:
            pass

    print(f"Updated manifest.json from {len(files)} preset files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
