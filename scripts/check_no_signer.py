#!/usr/bin/env python3
"""Heuristically reject Python code capable of signing or sending transactions."""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCANNER_PATHS = {
    Path("scripts/check_no_signer.py"),
    Path("scripts/check_secrets.py"),
}
PATTERNS = [
    re.compile(r"\b(?:keypair|versionedtransaction|signers?)\b", re.IGNORECASE),
    re.compile(
        r"\b(?:private[_ -]?key|secret[_ -]?key|seed[_ -]?phrase|mnemonic)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:sign_transaction|sign_all_transactions|partial_sign)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:sendtransaction|send_transaction|send_raw_transaction|"
        r"send_and_confirm_transaction|request_airdrop)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\.\s*sign\s*\(", re.IGNORECASE),
    re.compile(r"\b(?:solders|solana)\s*\.\s*keypair\b", re.IGNORECASE),
]


def _git_file_names(staged: bool) -> list[str]:
    command = (
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"]
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


def contains_forbidden_code(content: str) -> bool:
    return any(pattern.search(content) for pattern in PATTERNS)


def main() -> int:
    staged = "--staged" in sys.argv
    try:
        names = _git_file_names(staged)
        violations: list[tuple[str, int]] = []
        for name in names:
            path = Path(name)
            if (
                path.suffix != ".py"
                or path in SCANNER_PATHS
                or path.is_absolute()
                or ".." in path.parts
            ):
                continue
            if not staged and not (ROOT / path).is_file():
                continue

            try:
                content = _read_file(name, staged).decode("utf-8", errors="strict")
            except (OSError, UnicodeDecodeError):
                print(f"ERROR: Could not read Python source {name}.")
                return 2
            for number, line in enumerate(content.splitlines(), 1):
                if contains_forbidden_code(line):
                    violations.append((name, number))
    except RuntimeError as error:
        print(f"ERROR: {error}")
        return 2

    if violations:
        print("FORBIDDEN SIGNING OR TRANSACTION-SENDING PATTERN DETECTED:")
        for name, number in violations:
            print(f"  {name}:{number}")
        return 1

    print("No known signing or transaction-sending patterns found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
