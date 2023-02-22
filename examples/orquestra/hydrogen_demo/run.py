"""
To run this script:
1. Go to the repo root
2. Run ``python -m examples.orquestra.hydrogen_demo.run``. This ensures that relative
   imports work correctly.
"""
import time

from orquestra.sdk.schema.workflow_run import State

from .defs import hydrogen_workflow


def main():
    wf = hydrogen_workflow()

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


if __name__ == "__main__":
    main()
