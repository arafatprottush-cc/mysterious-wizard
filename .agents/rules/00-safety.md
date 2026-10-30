# Safety — Always On, Non-Negotiable

1. SIMULATION ONLY.
   Never write transaction-signing, wallet-loading, or mainnet-send code.
   CI must fail if signer, keypair, or sendTransaction patterns appear.
   Live code is only allowed after Phase 7 and my written approval,
   in a separate repository.

2. SECRETS.
   Never request, print, log, or commit private keys, seed phrases,
   passwords, or API tokens.
   Never write secrets into rules, AGENTS.md, or workflows.
   If a secret appears anywhere, stop and tell me.
   Set up .gitignore, pre-commit secret scanning, and CI secret scanning
   before the first commit.

3. NO UNVETTED CODE.
   Read third-party repositories as reference only.
   Never clone-and-run, install from, or copy code out of them.
   Stars and forks mean nothing.
   Flag obfuscated code, install scripts, and unfamiliar domains.

4. SANDBOX.
   Work in an isolated container/VM with no access to personal files,
   wallets, or logged-in browser profiles.
   Report the active Antigravity terminal and permission policy.
   Verify available options in Settings.
   Recommend the most restrictive working option.
   Never use a mode that skips confirmations.

5. BROWSER.
   Use a separate browser profile with no logins and no wallet extensions.
   Use a domain allowlist.
   Ask before visiting anything outside it.

6. DEPENDENCIES.
   Use a lockfile and pinned versions.
   Prefer releases at least 14 days old.
   Run dependency audits.
   Justify each dependency in docs/dependencies.md.
   Ask before adding dependencies.

7. PROTOCOL FACTS.
   Never hardcode protocol facts from memory.
   Source facts from current official documentation or on-chain data.
   Record source URL and retrieval date in docs/protocol_facts.md.

8. DATA.
   Respect provider terms of service and rate limits.
   Record license, cost, limitations, and availability for every source.

9. BUDGET.
   No paid services, API keys, or RPC plans without asking me first.
   Free-tier only by default.

10. SIMULATOR KILL SWITCHES.
    Include per-trade, hourly, and daily loss caps;
    maximum positions and exposure;
    halt on feed failure, abnormal slippage, or repeated failed fills.

11. LEGAL AND TAX.
    Before any proposed live phase, remind me to check my jurisdiction's
    applicable rules.
    Keep tax-ready trade logs from the start.

12. UNSURE = STOP AND ASK.
    Do not weaken safeguards to make a test pass.
    Do not edit global config (~/.gemini/GEMINI.md)
    or anything outside this workspace.
