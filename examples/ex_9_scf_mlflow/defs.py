"""
Workflow & task defs.

To run this on Orquestra see the ``run.py`` script in the same directory.
"""
from orquestra import sdk

from benchq.problem_ingestion.molecule_instance_generation import generate_hydrogen_chain_instance

task_deps = [
    sdk.PythonImports("pyscf==2.2.0", "openfermionpyscf==0.5", "scipy<1.11.0",),
    sdk.GithubImport("zapatacomputing/benchq", git_ref="ZQS-1365-Create-user-accessible-mlflow-for-scf-tooling"),
]
standard_task = sdk.task(
    source_import=sdk.InlineImport(),
    dependency_imports=task_deps,
    resources=sdk.Resources(memory="4Gi"),
)

@standard_task
def testing_get_active_space_meanfield_object(number_of_hydrogens):
    instance = generate_hydrogen_chain_instance(number_of_hydrogens=number_of_hydrogens)
    instance.avas_atomic_orbitals = ["H 1s", "H 2s"]
    instance.avas_minao = "sto-3g"
    mean_field_object = instance.get_active_space_meanfield_object()
    #     mlflow_experiment_name=f"chain of {number_of_hydrogens} hydrogens"
    # )
    is_sane = mean_field_object.check_sanity()
    return is_sane


@sdk.workflow
def scf_mlflow_workflow():
    results = []
    for n in [2, 3, 4]:
        mean_field_object = testing_get_active_space_meanfield_object(n)
        results.append(mean_field_object)
    return mean_field_object

