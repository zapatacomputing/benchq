from benchq.algorithms.time_evolution import get_qsp_time_evolution_program
from benchq.problem_ingestion import (
    generate_jw_qubit_hamiltonian_from_mol_data,
    get_vlasov_hamiltonian,
)
from benchq.problem_ingestion.molecule_instance_generation import (
    generate_hydrogen_chain_instance,
)


def main():
    dt = 0.5
    tmax = 5
    sclf = 1
    required_precision = 1e-3 / 2

    get_qsp_time_evolution_program(
        generate_jw_qubit_hamiltonian_from_mol_data(
            generate_hydrogen_chain_instance(3)
        ),
        required_precision,
        dt,
        tmax,
        sclf
    )

if __name__ == "__main__":
    main()
