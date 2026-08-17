# Third-party components

Every component we depend on, link, vendor, subprocess, or translate code from — recorded when it is
introduced, not at release time.

**Nothing here yet.** The skeleton has no runtime dependencies. `pytest` and `ruff` are development
tools that are neither redistributed nor linked, and are listed for completeness rather than because
they carry an obligation.

| Component | Upstream | Version | License | Integration | Modified | Attribution | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| pytest | https://github.com/pytest-dev/pytest | dev | MIT | dev tool, not redistributed | no | none | compatible |
| ruff | https://github.com/astral-sh/ruff | dev | MIT | dev tool, not redistributed | no | none | compatible |

## When you add a dependency

Add the row in the same change. A dependency that is in `pyproject.toml` and not in this table is
how a project finds out at release time that it cannot ship.

**Integration mode matters as much as the license.** A GPL library called as a subprocess and one
linked into the process are different obligations, and "we only import it" is not a mode — say which.

## The rule

**Unknown licensing status is not "probably okay."** It is unknown, and unknown components are not
redistributed until resolved. See [docs/licensing.md](docs/licensing.md).
