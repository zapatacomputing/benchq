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
	black src tests examples benchmarks benchmarks
	isort --profile=black src tests examples benchmarks

pyright:
	$(PYTHON) -m pyright src --pythonpath $(PYTHON)

style: flake8p mypy pyright black isort
	@echo This project passes style!

test:
	$(PYTHON) -m pytest tests

coverage:
	$(PYTHON) -m pytest \
		--cov=src \
		--cov-fail-under=$(MIN_COVERAGE) tests \
		--no-cov-on-fail \
		--cov-report xml \
		&& echo Code coverage Passed the $(MIN_COVERAGE)% mark!
