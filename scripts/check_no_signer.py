#!/usr/bin/env python3
"""Reject known transaction-signing/mainnet-send APIs in Python source."""
import re
from pathlib import Path

PATTERNS = [
    re.compile(r"\bKeypair\s*\.\s*(?:from_secret_key|from_bytes)\b"),
    re.compile(r"\bVersionedTransaction\b"),
    re.compile(r"\bsendTransaction\b"),
    re.compile(r"\bsign_transaction\b"),
    re.compile(r"\bsolders\.keypair\b"),
    re.compile(r"\bsolana\.keypair\b"),
    re.compile(r"\bTransaction\.sign\b"),
]

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIRS = [ROOT / "src", ROOT / "tests"]

def main():
    violations = []

    for directory in SOURCE_DIRS:
        if not directory.exists():
            continue

        for path in directory.rglob("*.py"):
            text = path.read_text(encoding="utf-8", errors="ignore")
            for number, line in enumerate(text.splitlines(), 1):
                if any(pattern.search(line) for pattern in PATTERNS):
                    violations.append((path.relative_to(ROOT), number))

    if violations:
        print("FORBIDDEN SIGNING/TRANSACTION API PATTERN DETECTED:")
        for path, number in violations:
            print(f"  {path}:{number}")
        return 1

    print("No known signer or mainnet-send patterns found.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
