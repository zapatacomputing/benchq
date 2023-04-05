"""
Prerequisites:
1. Log in to the remote Orquestra cluster with ``orq login -s https://prod-d.orquestra.io``

Running:
1. Comment/uncomment "in_process"/"prod-d" lines to select the runtime to use.
2. ``cd`` to the repo root.
3. Run ``python -m examples.orquestra.hydrogen_demo.run``. This ensures that relative
   imports work correctly.
"""
import time

from orquestra.sdk.schema.workflow_run import State

from .defs import hydrogen_workflow
from .estimates_ms import ms_estimates


def main():
    # uncomment which workflow do you want to run:
    wf = hydrogen_workflow()  # general hydrogen workflow to calculate estimates
    # wf = ms_estimates()  # calculate resource estimates using MS tool

    # Run locally, sequentially, in a single Python process. Useful for debugging, but
    # doesn't use Orquestra to its full potential.
    wf_run = wf.run("in_process")

    # Run remotely on Orquestra Platform.
    # wf_run = wf.run("prod-d")

    print(f"Workflow {wf_run.run_id} submitted!")

    while True:
        status = wf_run.get_status()
        print(f"Status: {status}")

        if status not in {State.WAITING, State.RUNNING}:
            break

        time.sleep(1)

    print(wf_run.get_results())


if __name__ == "__main__":
    main()
