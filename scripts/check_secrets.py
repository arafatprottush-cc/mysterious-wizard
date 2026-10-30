#!/usr/bin/env python3
"""Heuristically scan tracked, untracked, or staged files for common secrets."""

import re
import subprocess
import sys
from pathlib import Path

MAX_BYTES = 2_000_000
ROOT = Path(__file__).resolve().parents[1]
PATTERNS = [
    re.compile(rb"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(
        rb"""(?i)\b(?:api[_-]?key|secret|password|access[_-]?token)\b"""
        rb"""\s*[:=]\s*['"][^'"\r\n]{12,}['"]"""
    ),
    re.compile(rb"\b\d{8,12}:[A-Za-z0-9_-]{30,}\b"),
    re.compile(rb"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(rb"\bgh[pousr]_[A-Za-z0-9_]{30,}\b"),
    re.compile(rb"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
]
SCANNER_PATH = Path("scripts/check_secrets.py")


def _git_file_names(staged: bool) -> list[str]:
    command = (
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMRT", "-z"]
        if staged
        else ["git", "ls-files", "-co", "--exclude-standard", "-z"]
    )
    result = subprocess.run(command, cwd=ROOT, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError("Could not list repository files.")
    return [
        name.decode("utf-8", errors="surrogateescape")
        for name in result.stdout.split(b"\0")
        if name
    ]


def _file_size(name: str, staged: bool) -> int:
    if staged:
        result = subprocess.run(
            ["git", "cat-file", "-s", f":{name}"],
            cwd=ROOT,
            capture_output=True,
            check=False,
        )
        if result.returncode:
            raise RuntimeError("Could not inspect a staged file.")
        try:
            return int(result.stdout)
        except ValueError as error:
            raise RuntimeError("Could not inspect a staged file.") from error
    return (ROOT / name).stat().st_size


def _read_file(name: str, staged: bool) -> bytes:
    if staged:
        result = subprocess.run(
            ["git", "show", f":{name}"],
            cwd=ROOT,
            capture_output=True,
            check=False,
        )
        if result.returncode:
            raise RuntimeError("Could not read a staged file.")
        return result.stdout
    return (ROOT / name).read_bytes()


def contains_secret(content: bytes) -> bool:
    return any(pattern.search(content) for pattern in PATTERNS)


def main() -> int:
    staged = "--staged" in sys.argv
    try:
        names = _git_file_names(staged)
        findings: list[tuple[str, str]] = []
        for name in names:
            path = Path(name)
            if path == SCANNER_PATH or path.is_absolute() or ".." in path.parts:
                continue
            if not staged and not (ROOT / path).is_file():
                continue

            try:
                if _file_size(name, staged) > MAX_BYTES:
                    print(f"ERROR: File exceeds scanner size limit: {name}")
                    return 2
                content = _read_file(name, staged)
            except OSError:
                print(f"ERROR: Could not read {name}.")
                return 2
            if len(content) > MAX_BYTES:
                print(f"ERROR: File exceeds scanner size limit: {name}")
                return 2
            if b"\0" in content:
                continue
            if contains_secret(content):
                findings.append((name, "potential secret pattern"))
    except RuntimeError as error:
        print(f"ERROR: {error}")
        return 2

    if findings:
        print("POTENTIAL SECRET DETECTED. Values are deliberately not displayed:")
        for name, reason in findings:
            print(f"  {name}: {reason}")
        return 1

    print("Secret scan passed (heuristic patterns only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
