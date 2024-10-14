#
# Makefile: Commands to simplify development and releases
#
# Usage:
#
#     make clean
#     make test
#     make (patch | minor | major)
#     make build upload
#

root_dir = $(realpath .)
venv_dir = $(root_dir)/.venv

python := $(venv_dir)/bin/python
flake8 := $(venv_dir)/bin/flake8
pytest := $(venv_dir)/bin/pytest
coverage := $(venv_dir)/bin/coverage
bumpversion := $(venv_dir)/bin/bump2version
twine := $(venv_dir)/bin/twine


commit_opts := --gpg-sign
upload_opts := --skip-existing --sign
pytest_opts :=

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of:"
	@echo ""
	@echo "  help                 to show this list"
	@echo "  clean-build          to clean the files and directories generated by previous builds"
	@echo "  clean-tests          to clean the directories created during testing"
	@echo "  clean-coverage       to clean the test coverage data and reports"
	@echo "  clean-venv           to clean the virtualenv"
	@echo "  clean                to clean everything"
	@echo
	@echo "  build                to build the package"
	@echo "  checks               to check the source code"
	@echo "  coverage             to measure the test coverage"
	@echo "  major                to update the version number for a major release, e.g. 2.1 to 3.0"
	@echo "  minor                to update the version number for a minor release, e.g. 2.1 to 2.2"
	@echo "  patch                to update the version number for a patch release, e.g. 2.1.1 to 2.1.2"
	@echo "  test                 to run the unit tests during development"
	@echo "  upload               to upload a release to PyPI repository"
	@echo "  venv                 to create the virtualenv and install dependencies"
	@echo

.PHONY: clean-build
clean-build:
	rm -rf build
	rm -rf src/*.egg-info

.PHONY: clean-tests
clean-tests:
	rm -rf .tox
	rm -rf .pytest_cache

.PHONY: clean-coverage
clean-coverage:
	rm -rf .coverage
	rm -rf reports/coverage

.PHONY: clean-venv
clean-venv:
	rm -rf $(venv_dir)

.PHONY: clean
clean: clean-build clean-tests

.PHONY: build
build: clean-build
	$(python) -m build

.PHONY: checks
checks:
	flake8 src tests
	black src tests
	isort src tests

.PHONY: coverage
coverage:
	pytest --cov=src --cov-config=.coveragerc --cov-report html

.PHONY: major
major:
	$(bumpversion) major

.PHONY: minor
minor:
	$(bumpversion) minor

.PHONY: patch
patch:
	$(bumpversion) patch

.PHONY: test
test:
	pytest $(pytest_opts)

.PHONY: upload
upload:
	$(twine) upload $(upload_opts) dist/*

venv:
	uv venv .venv
	uv pip sync requirements.txt

# include any local makefiles
-include *.mk
