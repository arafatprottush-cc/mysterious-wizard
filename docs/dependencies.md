# Dependency and Lockfile Policy

## Assumptions and open questions

- Runtime dependencies remain empty; the three approved developer tools are
  limited to linting, type checking, and vulnerability auditing.
- The lock targets the Python 3.12 Linux environment used by CI.
- External source research is still blocked pending browser-profile and domain
  allowlist verification.

## Current inventory

| Package | Pin | Purpose | License | Source and release evidence |
|---|---:|---|---|---|
| Ruff | 0.16.0 | Python linting | MIT | [PyPI metadata](https://pypi.org/pypi/ruff/0.16.0/json); [official release](https://github.com/astral-sh/ruff/releases/tag/0.16.0), released 2026-07-23 |
| mypy | 2.3.0 | Static type checking | MIT | [PyPI metadata](https://pypi.org/pypi/mypy/2.3.0/json); [official repository](https://github.com/python/mypy), PyPI upload 2026-07-13 |
| pip-audit | 2.10.0 | Dependency vulnerability audit | Apache-2.0 | [PyPI metadata](https://pypi.org/pypi/pip-audit/2.10.0/json); [official release](https://github.com/pypa/pip-audit/releases/tag/v2.10.0), released 2025-12-01 |

Metadata and release information were checked on 2026-10-30. PyPI records
`ruff`'s and `mypy`'s license expression as MIT and `pip-audit`'s license
classifier as Apache Software License. The pinned releases predate the
14-day minimum preference.

PyPI's files for these releases were marked without provenance attestations.
The links above match the official repository URLs listed by PyPI, and release
notes/licenses were reviewed there. The lock pins hashes for retrieved
distributions; hashes detect artifact changes but do not replace publisher
provenance.

The project has no application/runtime dependencies (`pyproject.toml` has an
empty dependency list). `requirements.txt` remains a placeholder for runtime
packages. `requirements-dev.in` records approved direct tool pins, and
`requirements-dev.lock` records the full resolved development environment with
hashes. CI installs only from that lock and audits it with `pip-audit`.
The audit uses `--no-deps --disable-pip` because the lock enumerates every
direct and transitive resolved package as an exact hash-pinned entry; it does
not perform a second resolver pass.

The following transitive distributions were resolved for CPython 3.12 on Linux
x86_64, downloaded without execution, SHA-256 checked against PyPI metadata, and
reviewed for bundled license metadata on 2026-10-30:

| Package | Version | Purpose | License |
|---|---:|---|---|
| ast-serialize | 0.13.1 | Mypy AST serialization | MIT |
| boolean.py | 5.0 | License-expression boolean operations | BSD-2-Clause |
| CacheControl | 0.14.4 | HTTP response caching | Apache-2.0 |
| certifi | 2026.10.23 | TLS root certificates for HTTP requests | MPL-2.0 |
| charset-normalizer | 3.5.2 | HTTP response character-set detection | MIT |
| cyclonedx-python-lib | 11.12.0 | CycloneDX SBOM support in pip-audit | Apache-2.0 |
| defusedxml | 0.7.1 | Hardened XML parsing | PSF |
| filelock | 4.2.4 | Cache file coordination | MIT |
| idna | 3.20 | Internationalized domain handling | BSD-3-Clause |
| librt | 0.16.0 | Mypy runtime support | MIT |
| license-expression | 30.4.4 | License-expression parsing | Apache-2.0 |
| markdown-it-py | 4.2.0 | Rich terminal output markup | MIT |
| mdurl | 0.1.2 | Markdown URL utilities | MIT |
| msgpack | 1.2.4 | HTTP cache serialization | Apache-2.0 |
| mypy_extensions | 1.1.0 | Mypy typing extensions | MIT |
| packageurl-python | 0.17.6 | Package URL identifiers for SBOMs | MIT |
| packaging | 26.3 | Version and requirement parsing | Apache-2.0 OR BSD-2-Clause |
| pathspec | 1.1.1 | Mypy path matching | MPL-2.0 |
| pip | 26.2.2 | Required by pip-api | MIT |
| pip-api | 0.0.35 | Installed-package metadata for pip-audit | Apache-2.0 |
| pip-requirements-parser | 32.0.1 | Requirements-file parsing | MIT |
| platformdirs | 4.14.0 | Cache and configuration paths | MIT |
| Pygments | 2.21.0 | Terminal syntax highlighting | BSD-2-Clause |
| pyparsing | 3.3.3 | Requirements syntax parsing | MIT |
| py-serializable | 2.1.0 | CycloneDX object serialization | Apache-2.0 |
| requests | 2.34.2 | HTTP client for vulnerability lookups | Apache-2.0 |
| rich | 15.0.0 | Human-readable audit output | MIT |
| sortedcontainers | 2.4.0 | CycloneDX data structures | Apache-2.0 |
| tomli | 2.5.0 | TOML parsing | MIT |
| tomli_w | 1.2.0 | TOML serialization | MIT |
| typing_extensions | 4.16.0 | Backported typing definitions | PSF-2.0 |
| urllib3 | 2.8.0 | HTTP transport used by requests | MIT |

The direct tools meet the 14-day age preference. The resolved graph includes
some newer transitive releases (including certifi, filelock, msgpack,
platformdirs, and pip); these are pinned and included in the vulnerability
audit rather than silently treated as risk-free.

## Update process

1. Obtain approval before adding or changing any dependency.
2. Review official package ownership, source, release history, install/build
   behavior, license, and relevant security advisories.
3. Prefer a release at least 14 days old; pin direct and transitive versions.
4. Regenerate the lock for the CI Python/platform and commit it with the input
   constraints.
5. Run the locked dependency audit and document its date and limitations.
6. Document package purpose, license, source, and removal criteria here.
