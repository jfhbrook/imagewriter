set dotenv-load := true

# By default, run checks and tests, then format and lint
default:
  @just generate
  @just format
  @just check
  @just test
  @just lint

#
# Development tooling - linting, formatting, etc
#

# Generate format type for Pandoc
generate:
  uv run ./scripts/generate-pandoc-formats.py

# Format with black and isort
format:
  uv run black ./src ./tests
  uv run isort ./src ./tests

# Lint with flake8
lint:
  uv run flake8 ./src ./tests
  uv run validate-pyproject ./pyproject.toml

# Check type annotations with pyright
check:
  uv run npx pyright@latest

# Run tests with pytest
test:
  uv run pytest -vvv ./tests
  @just _clean-test

# Update snapshots
snap:
  uv run pytest --snapshot-update ./tests
  @just _clean-test

_clean-test:
  rm -f pytest_runner-*.egg
  rm -rf tests/__pycache__

#
# Shell and console
#

shell:
  uv run bash

console:
  uv run jupyter lab

#
# Documentation
#

# Live generate docs and host on a development webserver
docs:
  uv run mkdocs serve

# Build the documentation
build-docs:
  uv run mkdocs build

#
# Package publishing
#

# Build the package
build:
  uv build

_clean-build:
  rm -rf dist

# Tag the release in git
tag:
  uv run git tag -a "$(python3 -c 'import toml; print(toml.load(open("pyproject.toml", "r"))["project"]["version"])')" -m "Release $(python3 -c 'import toml; print(toml.load(open("pyproject.toml", "r"))["project"]["version"])')"

publish: build
  uv publish

# Clean up loose files
clean: _clean-test
  rm -rf imagewriter.egg-info
  rm -f imagewriter/*.pyc
  rm -rf imagewriter/__pycache__

enable_cups_web:
  cupsctl WebInterface=yes

disable_cups_web:
  cupsctl WebInterface=no

open_cups_web:
  open http://localhost:631
