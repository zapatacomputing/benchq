################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
include subtrees/z_quantum_actions/Makefile

# This project has a lower-than-average test coverage. Let's temporarily
# override the required coverage threshold to let us CI test runs finish, add
# tests, and eventually get back to the standard level.

github_actions-default:
	${PYTHON_EXE} -m venv ${VENV_NAME}
	"${VENV_NAME}/${VENV_BINDIR}/${PYTHON_EXE}" -m pip install --upgrade pip
	"${VENV_NAME}/${VENV_BINDIR}/${PYTHON_EXE}" -m pip install -e '.[dev, circuit-gen]'

# (no override)
style-fix:
	black src tests examples benchmarks
	isort --profile=black src tests examples benchmarks

test:
	$(PYTHON) -m pytest -W error tests

coverage:
	$(PYTHON) -m pytest -W error\
		--cov=src \
		--cov-fail-under=$(MIN_COVERAGE) tests \
		--no-cov-on-fail \
		--cov-report xml \
		&& echo Code coverage Passed the $(MIN_COVERAGE)% mark!
