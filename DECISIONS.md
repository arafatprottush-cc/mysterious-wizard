# DECISIONS

## Assumptions
- Research and simulation only.
- Python is the default stack.
- Free-tier data sources only.
- No live trading code.
- Capital, drawdown limits, daily loss limit, per-trade loss limit,
  paper-trading duration, and jurisdiction are not yet specified.
- The project currently has no runtime dependencies.

## Open Questions
- Which free historical Solana launch datasets are sufficiently complete?
- Which data providers permit the intended research use?
- What paper-trading duration should be used?
- What risk limits should the simulator use?
- What external domains will be allowlisted for Phase 1 research?
- Can a separate logged-out browser profile without wallet extensions be
  verified before external source retrieval?

## Decision Log
- Original Phase 0 skeleton: compared with `old-origin/main`; every tracked
  file is present and identical, so no recovery was needed.
- Baseline secret and no-signing scanners: passed before changes.
- CI tools: Ruff 0.16.0, mypy 2.3.0, and pip-audit 2.10.0 are approved,
  provenance/license-reviewed, and hash-locked as development-only
  dependencies; runtime dependencies remain empty.
- Phase 1 external research: blocked until browser isolation and an explicit
  domain allowlist are verified. No Solana protocol or strategy sources were
  accessed.
