#!/usr/bin/env python3
"""Basic secret scanner for staged files or the repository."""
import re
import subprocess
import sys
from pathlib import Path

PATTERNS = [
    re.compile(r"-----BEGIN (?:OPENSSH |RSA |EC )?PRIVATE KEY-----"),
    re.compile(
        r"""(?i)\b(?:api[_-]?key|secret|password|access[_-]?token)\b"""
        r"""\s*[:=]\s*['"][^'"\n]{12,}['"]"""
    ),
    re.compile(r"\b\d{8,12}:[A-Za-z0-9_-]{30,}\b"),
]

SKIP = {
    "scripts/check_secrets.py",
    ".git",
}

def main():
    staged = "--staged" in sys.argv

    command = (
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"]
        if staged
        else ["git", "ls-files", "-co", "--exclude-standard"]
    )

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode:
        print("ERROR: Could not list files.")
        return 2

    findings = []
    for name in result.stdout.splitlines():
        if name in SKIP or name.startswith(".git/"):
            continue

        path = Path(name)
        if not path.is_file() or path.stat().st_size > 2_000_000:
            continue

        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        for number, line in enumerate(content.splitlines(), 1):
            if any(pattern.search(line) for pattern in PATTERNS):
                findings.append((name, number))

    if findings:
        print("POTENTIAL SECRET DETECTED. Values are deliberately not displayed:")
        for name, number in findings:
            print(f"  {name}:{number}")
        return 1

    print("Secret scan passed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
