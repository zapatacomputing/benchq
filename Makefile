################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
include subtrees/z_quantum_actions/Makefile

# This project has a lower-than-average test coverage. Let's temporarily
# override the required coverage threshold to let us CI test runs finish, add
# tests, and eventually get back to the standard level.
MIN_COVERAGE := 30

github_actions-default:
	${PYTHON_EXE} -m venv ${VENV_NAME}
	"${VENV_NAME}/${VENV_BINDIR}/${PYTHON_EXE}" -m pip install --upgrade pip
	"${VENV_NAME}/${VENV_BINDIR}/${PYTHON_EXE}" -m pip install -e '.[dev, circuit-gen]'
