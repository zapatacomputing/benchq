################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import os
import sys
import time

import pytest
from orquestra.sdk.schema.workflow_run import State

from examples.ex_1_from_qasm import main as from_qasm_main
from examples.ex_2_time_evolution import main as time_evolution_main
from examples.ex_3_packages_comparison import main as packages_comparison_main
from examples.ex_4_extrapolation import main as extrapolation_main

SKIP_AZURE = pytest.mark.skipif(
    os.getenv("BENCHQ_TEST_AZURE") is None,
    reason="Azure tests can only run if BENCHQ_TEST_AZURE env variable is defined",
)

MAIN_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(MAIN_DIR))

print(sys.path)
print(MAIN_DIR)


@pytest.fixture(autouse=True)
def _clean_auto_generated_files():
    yield


# def test_orquestra_example():
#     """
#     Tests that SDK workflow example works properly at least in process
#     """

#     wf = hydrogen_workflow()
#     wf_run = wf.run("in_process")

#     loops = 0

#     while True:
#         status = wf_run.get_status()
#         if status not in {State.WAITING, State.RUNNING}:
#             break
#         if loops > 180:  # 3 minutes should be enough to finish workflow.
#             pytest.fail("WF didn't finish in 150 secs.")

#         time.sleep(1)
#         loops += 1

#     wf_run.get_results()  # this will throw an exception on failed workflow


# @pytest.mark.skip(reason="Temporary skip to facilitate development")
def test_from_qasm_example():
    file_path = os.path.join("examples", "data", "example_circuit.qasm")
    from_qasm_main(file_path)


def test_time_evolution_example():
    time_evolution_main()


@SKIP_AZURE
def test_packages_comparison_example():
    packages_comparison_main()


# @pytest.mark.skip(reason="Temporary skip to facilitate development")
def test_extrapolation_example():
    extrapolation_main(use_hydrogen=False)


# def test_advanced_estimates():
#     advanced_estimates_main()
