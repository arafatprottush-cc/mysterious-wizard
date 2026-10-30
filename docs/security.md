# Repository Security Policy

## Assumptions and open questions

- The project is simulation-only; no wallet, key material, signer, or live
  transaction functionality is permitted.
- The scanner checks are defense-in-depth heuristics, not security proofs.
- External research source allowlist and browser-profile verification remain
  outstanding before Phase 1 source retrieval.

## Controls

- `.gitignore` excludes common local credentials, key files, database files,
  generated Python files, and private/raw data directories.
- `scripts/check_secrets.py` scans tracked and non-ignored untracked files, or
  the Git index when invoked with `--staged`. The pre-commit hook uses staged
  content, so an unsafe staged version is checked even when the working copy
  differs.
- `scripts/check_no_signer.py` checks Python files in the repository and can
  inspect staged Python content with `--staged`. The two scanner
  implementations are excluded because they necessarily contain patterns
  used to detect unsafe code.
- CI runs both checks with read-only repository permissions.
- Install the local hook with:

  ```sh
  git config core.hooksPath .githooks
  ```

## Scanner limitations

The secret scanner uses a finite list of regular expressions. It can miss
unknown formats, encoded or split credentials, values loaded at runtime, secrets
embedded in binary files, and files over its configured 2 MB limit (which fail
the scan rather than being silently accepted). It deliberately skips NUL-byte
files and does not query secret-provider services. It can also flag harmless
text that resembles a credential. It does not scan Git history or ignored files.

The no-signing scanner is a Python source heuristic. It can miss obfuscated
calls, aliases, dynamic imports, generated/native code, other languages, and
unsafe behavior hidden in a dependency. Its pattern list can also produce false
positives. Passing it does not guarantee that the repository or a future
program is safe to sign or send transactions.

Neither scanner replaces review, least-privilege CI, dependency auditing,
secret rotation, or monitoring. Do not place real credentials in this
repository, including test fixtures.
