# Statistics — Always On

- Use time-ordered train, validation, and test datasets.
- Use the TEST set exactly once, at the end.
- Retuning after viewing test results invalidates the test; disclose this
  and obtain fresh data.
- Pre-register hypotheses and parameter ranges in research/prereg.md.
- Commit the preregistration BEFORE testing.
- Count every strategy and parameter variant tried.
- Correct for multiple testing using deflated Sharpe or a suitable method.
- No lookahead bias.
- No survivorship bias: include rugged and dead tokens where data permits.
- Use only information available at the actual decision timestamp.
- Model realistic fills: latency, failed/expired transactions, priority
  fees and tips, price impact, sandwich risk, unsellable tokens, and
  partial fills.
- Required baselines:
  1. Random entry with identical exits.
  2. Buy all tokens passing basic liquidity filters.
  3. Hold SOL.
- Report bootstrap confidence intervals, sample size, capacity,
  and market-regime breakdown.
- Too few trades means INCONCLUSIVE, never PROFITABLE.
- Reproducible runs require fixed seeds, versioned configs,
  data snapshot IDs, and Git commit hashes in every report.
- Never tune thresholds to flatter results.
- Report failures with equal prominence.
