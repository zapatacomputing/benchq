"""
Here we provide code showing how to leverege the orquestra platform
in order to produce resource estimates for a qsp algorithm.

Prerequisites:
1. Login to the remote Orquestra cluster with
   ``orq login -s https://prod-d.orquestra.io``

Running:
1. Comment/uncomment "in_process"/"prod-d" lines to select the runtime to use.
2. ``cd`` to the repo root.
3. Run ``python -m examples.ex_5_orquestra.run``. This ensures that relative
   imports work correctly.
"""

from .defs import example_workflow


def main():
    # example workflow which roughly reproduces ex_3_packages_comparison
    wf = example_workflow()

    # Run locally, sequentially, in a single Python process. Useful for debugging, but
    # doesn't use Orquestra to its full potential.
    # wf_run = wf.run("in_process")

    # Run remotely on Orquestra Platform.
    wf_run = wf.run(
        "darpa-benchmarking",
        workspace_id="mlflow-benchq-testing-dd0cb1",
        project_id="benchq-mlflow-testing-1bbe36",
    )

    print(f"Workflow {wf_run.run_id} submitted!")

    wf_run.wait_until_finished()

    print(wf_run.get_results())


if __name__ == "__main__":
    main()
