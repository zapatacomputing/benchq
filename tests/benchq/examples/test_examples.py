################################################################################
# © Copyright 2022-2023 Zapata Computing Inc.
################################################################################
import os
import sys
import time

import pytest
from orquestra.sdk.schema.workflow_run import State

# from examples.advanced_estimates import main as advanced_estimates_main
from examples.h_chain_trotter import main as h_chain_main

# from examples.orquestra.hydrogen_demo.defs import hydrogen_workflow
from examples.re_from_operator import main as re_from_operator
from examples.re_from_qasm import main as h_chain_from_qasm_main

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


@pytest.mark.skip(reason="Temporary skip to facilitate development")
def test_h_chain_example():
    h_chain_main()


# @pytest.mark.skip(reason="Temporary skip to facilitate development")
def test_h_chain_from_qasm_example():
    file_path = os.path.join("examples", "circuits", "h_chain_circuit.qasm")
    h_chain_from_qasm_main(file_path)


@pytest.mark.skip(reason="Temporary skip to facilitate development")
def test_re_from_operator():
    re_from_operator()


# def test_advanced_estimates():
#     advanced_estimates_main()
