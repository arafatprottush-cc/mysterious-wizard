# Solana Sniper Research Repo

Purpose: research and SIMULATE meme coin sniping strategies. Verdict may be
"no viable edge found." No live trading code exists in this repo.

Facts about this repo:
- Stack: Python.
- Data: free-tier providers only unless explicitly approved.
- Capital: not specified; do not assume an amount.
- No application entry point exists yet.
- Tests: `python -m unittest discover -v`.
- Lint: `ruff check src tests scripts`; formatting: `ruff format --check src tests scripts`.
- Type check: `mypy src tests scripts`.
- Install reviewed CI tools with `python -m pip install --require-hashes -r requirements-dev.lock`.
- All protocol facts (program IDs, fees, curve parameters) live in
  docs/protocol_facts.md with source URL and retrieval date.
- Never hardcode protocol facts from memory.

Read .agents/rules/ before every task.
If any rule conflicts with a request, STOP and tell me.
