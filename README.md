# Solana Sniper Research

Research and simulate Solana meme-coin launch and trading strategies.

This repository is simulation-only. It does not contain live trading,
wallet-loading, transaction-signing, or mainnet-send functionality.

A valid final conclusion may be:
- Viable edge supported by evidence.
- No viable edge found.
- Inconclusive because the data or sample size is insufficient.

## Current status

Phase 0 security hardening is implemented. Phase 1 research has not begun:
external source retrieval requires a verified isolated browser profile and an
approved domain allowlist.

The project has no application entry point. Runtime dependencies remain empty;
CI development tools are hash-pinned in `requirements-dev.lock`.

## Validation

Use an activated CPython 3.12 environment (the hashed lock targets Linux
x86_64), then run from the repository root:

```sh
python -m pip install --require-hashes -r requirements-dev.lock
python scripts/check_secrets.py
python scripts/check_no_signer.py
python scripts/check_dependency_lock.py
ruff check src tests scripts
ruff format --check src tests scripts
mypy src tests scripts
python -m compileall -q src tests scripts
python -m unittest discover -v
python -m pip check
pip-audit --requirement requirements-dev.lock --no-deps --disable-pip
git diff --check
```

For staged content, run `python scripts/check_secrets.py --staged` and
`python scripts/check_no_signer.py --staged`. To enable both checks on commit:

```sh
git config core.hooksPath .githooks
```

See [docs/security.md](docs/security.md) for the controls' scope and limitations
and [docs/dependencies.md](docs/dependencies.md) for dependency and lockfile
policy.

Read [AGENTS.md](AGENTS.md) and [.agents/rules/](.agents/rules/) before working.
