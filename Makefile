# Every target goes through `$(PY) -m` so it behaves the same with an activated venv, without one,
# and in CI. Override with `make PY=python3.12 test` when you want a specific interpreter.
PY ?= python

# Easy buttons. The pair that matters is `fix` and `verify`: one makes things correct, one asks
# whether they are. Neither documentation nor formatting is smuggled into `test` - a command that
# rewrites your tree as a side effect of observing it is one you stop trusting.

.PHONY: help test lint fix verify docs-fix docs-check

help:
	@echo "make test        run the suite"
	@echo "make lint        ruff check + format check"
	@echo "make fix         apply formatting, code and documentation"
	@echo "make verify      everything CI runs"

test:
	$(PY) -m pytest -q

lint:
	$(PY) -m ruff check src tests
	$(PY) -m ruff format --check src tests

fix: docs-fix
	$(PY) -m ruff check --fix src tests
	$(PY) -m ruff format src tests

verify: lint docs-check test

# Documentation tooling lives outside this repo and needs no Python.
# See https://github.com/ewc3labs/ewc3-docs-tools
docs-fix:
	npx --yes github:ewc3labs/ewc3-docs-tools fix

docs-check:
	npx --yes github:ewc3labs/ewc3-docs-tools check
