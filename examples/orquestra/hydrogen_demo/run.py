"""
To run this script:
1. Go to the repo root
2. Run ``python -m examples.orquestra.hydrogen_demo.run``. This ensures that relative
   imports work correctly.
"""
from .defs import hydrogen_workflow


def main():
    wf = hydrogen_workflow()
    wf_run = wf.run("in_process")
    print("all done!")


if __name__ == "__main__":
    main()
