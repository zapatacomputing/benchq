"""Script for running estimation workflow.

Synopsis:
usage: run.py [-h] target

positional arguments:
  target      where to run the workflow (e.g. in_process or name of the orquestra
              cluster). This argument is passed to Workflow.run method.

options:
  -h, --help  show this help message and exit

This file uses relative imports, and hence has to be launched as module from outside
of its parent directory. For intsance, to launch it from benchq main directory, run:

python -m examples.ex_6_orquestra_customized.run in_process
"""
import argparse
from time import sleep

from orquestra.sdk.schema.workflow_run import State

from .defs import estimation_workflow


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "target",
        help=(
            "where to run the workflow (e.g. in_process or name of the orquestra "
            "cluster). This argument is passed to Workflow.run method."
        ),
        type=str,
    )

    args = parser.parse_args()

    wf = estimation_workflow()

    wf_run = wf.run(args.target)
    print(f"Workflow {wf_run.run_id} submitted!")

    wf_run.wait_until_finished()

    print(wf_run.get_results())


if __name__ == "__main__":
    main()
