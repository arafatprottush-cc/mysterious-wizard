#!/usr/bin/env python3
"""Verify exact direct pins and SHA-256 hashes in the development lock."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIN_PATTERN = re.compile(
    r"(?P<name>[A-Za-z0-9][A-Za-z0-9._-]*)==(?P<version>[A-Za-z0-9.+!-]+)"
    r"(?:\s+--hash=sha256:(?P<digest>[A-Fa-f0-9]{64}))?"
)


def _normalize_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def _read_pins(path: Path, require_hashes: bool) -> dict[str, tuple[str, str | None]]:
    pins: dict[str, tuple[str, str | None]] = {}
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        requirement = line.partition("#")[0].strip()
        if not requirement or requirement == "--require-hashes":
            continue
        match = PIN_PATTERN.fullmatch(requirement)
        if match is None or (require_hashes and match.group("digest") is None):
            raise ValueError(f"Invalid pinned requirement in {path.name}:{number}.")
        name = _normalize_name(match.group("name"))
        if name in pins:
            raise ValueError(f"Duplicate package in {path.name}:{number}.")
        pins[name] = (match.group("version"), match.group("digest"))
    return pins


def main() -> int:
    try:
        direct = _read_pins(ROOT / "requirements-dev.in", require_hashes=False)
        locked = _read_pins(ROOT / "requirements-dev.lock", require_hashes=True)
    except (OSError, ValueError) as error:
        print(f"Dependency lock validation failed: {error}")
        return 1

    mismatches = [
        name
        for name, (version, _) in direct.items()
        if name not in locked or locked[name][0] != version
    ]
    if mismatches:
        print("Direct dependency pins do not match the lock:")
        for name in mismatches:
            print(f"  {name}")
        return 1

    print(f"Dependency lock passed: {len(locked)} pinned, hashed packages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
