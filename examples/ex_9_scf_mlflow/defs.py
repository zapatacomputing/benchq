"""
Workflow & task defs.

To run this on Orquestra see the ``run.py`` script in the same directory.
"""
from orquestra import sdk

from benchq.problem_ingestion.molecule_instance_generation import (
    generate_hydrogen_chain_instance,
)


@sdk.task(
    source_import=sdk.InlineImport(),
    dependency_imports=[
        sdk.PythonImports(
            "pyscf==2.2.0",
            "openfermionpyscf==0.5",
            "scipy<1.11.0",
        ),
        sdk.GithubImport(
            "zapatacomputing/benchq",
            git_ref="ZQS-1365-Create-user-accessible-mlflow-for-scf-tooling",
        ),
    ],
)
def testing_get_active_space_meanfield_object(number_of_hydrogens):
    instance = generate_hydrogen_chain_instance(
        number_of_hydrogens=number_of_hydrogens,
        mlflow_experiment_name=f"chain of {number_of_hydrogens} hydrogens",
        orq_workspace_id="mlflow-benchq-testing-dd0cb1",
        avas_atomic_orbitals=["H 1s", "H 2s"],
        avas_minao="sto-3g",
    )
    mean_field_object = instance.get_active_space_meanfield_object()
    hamiltonian = instance.get_active_space_hamiltonian()
    return (mean_field_object.converged, hamiltonian)


@sdk.workflow
def scf_mlflow_workflow():
    results = []
    for n in [2, 3, 4]:
        mfo, ham = testing_get_active_space_meanfield_object(n)
        results.append(mfo)
        print(ham)
    return results
