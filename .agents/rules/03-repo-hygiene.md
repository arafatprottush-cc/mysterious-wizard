# Repo Hygiene — Always On

- Use conventional commit messages.
- CI must run lint, type checking, tests, secret scanning,
  dependency auditing, and the no-signer check.
- Maintain DECISIONS.md.
- Put assumptions and open questions at the top of every artifact.
- Each phase ends with its required artifact files and a /phase-gate check.
- Stop after a phase gate and wait for my approval before proceeding.
- Preserve existing user changes.
- Never use destructive Git commands or force-push.
- Do not commit secrets, generated datasets, or unreviewed artifacts.
- Do not edit files outside this workspace.
