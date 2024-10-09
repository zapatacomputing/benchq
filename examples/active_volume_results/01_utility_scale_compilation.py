from openfermion.transforms import get_fermion_operator, jordan_wigner

from pyscf.tools import fcidump
from pyscf import ao2mo
import numpy as np
from openfermion import InteractionOperator
from openfermion.resource_estimates.molecule.pyscf_utils import cas_to_pyscf

from pyLIQTR.ProblemInstances.getInstance import *
from pyLIQTR.BlockEncodings.getEncoding import *
from pyLIQTR.utils.resource_analysis import estimate_resources
from pyLIQTR.utils.circuit_decomposition import circuit_decompose_multi
from pyLIQTR.qubitization.phase_estimation import QubitizedPhaseEstimation
from pyLIQTR.qubitization.qubitized_gates import QubitizedWalkOperator
from pyLIQTR.utils.printing import openqasm
from pyLIQTR.utils.resource_analysis import (
    estimate_resources,
    count_t_gates,
    t_complexity_from_circuit,
)

import cirq
import dill as pickle
from time import time

start_time = time()


def get_circuit(file_name):

    fci_data = fcidump.read(file_name)  # microsoft azure system
    fci_data.keys()  # should be self-explanatory; MS2 = 2S

    print(f"Active space contains {fci_data['NELEC']} electrons")
    print(f"Active space contains {fci_data['NORB']} orbitals")

    eri = ao2mo.restore("s1", fci_data["H2"], fci_data["NORB"])

    n_alpha = (fci_data["NELEC"] + fci_data["MS2"]) // 2
    n_beta = (fci_data["NELEC"] - fci_data["MS2"]) // 2
    pyscf_mol, pyscf_mf = cas_to_pyscf(
        h1=fci_data["H1"],
        eri=eri,
        ecore=fci_data["ECORE"],
        num_alpha=n_alpha,
        num_beta=n_beta,
    )

    # Example calculation
    from pyscf.mcscf import CASCI

    fci = CASCI(pyscf_mf, ncas=fci_data["NORB"], nelecas=fci_data["NELEC"])
    # fci.kernel()

    # Helper functions
    def integrals2intop(h1, eri, ecore):
        norb = h1.shape[0]
        h2_so = np.zeros((2 * norb, 2 * norb, 2 * norb, 2 * norb))
        h1_so = np.zeros((2 * norb, 2 * norb))

        # Populate h1_so
        h1_so[:norb, :norb] = h1
        h1_so[norb:, norb:] = h1_so[:norb, :norb]

        # Populate h2_so
        h2_so[0::2, 0::2, 0::2, 0::2] = eri
        h2_so[1::2, 1::2, 0::2, 0::2] = eri
        h2_so[0::2, 0::2, 1::2, 1::2] = eri
        h2_so[1::2, 1::2, 1::2, 1::2] = eri

        # Transpose from 1122 to 1221
        h2_so = np.transpose(h2_so, (1, 2, 3, 0))

        return InteractionOperator(
            constant=ecore, one_body_tensor=h1_so, two_body_tensor=h2_so
        )

    interaction_operator = integrals2intop(
        h1=fci_data["H1"], eri=eri, ecore=fci_data["ECORE"]
    )

    mol_instance = getInstance(
        "ChemicalHamiltonian", mol_ham=interaction_operator, mol_name="system"
    )
    print(mol_instance)

    br = 1
    df_error_threshold = 1e-3
    sf_error_threshold = 1e-3
    energy_error = 1e-3  # same as delta_e 

    df_encoding = getEncoding(
        instance=mol_instance,
        encoding=VALID_ENCODINGS.DoubleFactorized,
        df_error_threshold=df_error_threshold,
        sf_error_threshold=sf_error_threshold,
        br=br,
        energy_error=energy_error,
        rotation_allowed=False,
    )

    get_estimates = estimate_resources(df_encoding.circuit)
    print(get_estimates)

    lam = mol_instance.get_alpha(
        encoding="DF",
        df_error_threshold=df_error_threshold,
        sf_error_threshold=sf_error_threshold,
    )
    print("lambda", lam)
    delta_e = 0.001  # same as in Azure

    print("qpe_precision", delta_e)

    # get precision qubits m
    m_base = (np.sqrt(2) * np.pi * lam) / (2 * delta_e)
    m = int(np.ceil(np.log(m_base)))
    print("num_bits_qpe_precision", m)

    return df_encoding.circuit, m


file_name = "fcidump.H2_sto-3g"  # 2 orbitals
block_encoding, m = get_circuit(file_name)

from benchq.algorithms.data_structures import ErrorBudget, AlgorithmImplementation
from benchq.problem_embeddings import QuantumProgram
from benchq.quantum_hardware_modeling import DETAILED_ION_TRAP_ARCHITECTURE_MODEL
from benchq.resource_estimators.graph_estimator import GraphResourceEstimator

from benchq.compilation.graph_states.circuit_compilers import (
    get_ruby_slippers_circuit_compiler,
    default_ruby_slippers_circuit_compiler,
)

from benchq.compilation.graph_states.implementation_compiler import (
    get_implementation_compiler,
)

from benchq.conversions import import_circuit
from qiskit.circuit import QuantumCircuit

from benchq.magic_state_distillation.autoccz_factories import iter_auto_ccz_factories

from benchq.magic_state_distillation.litinski_factories import iter_litinski_factories

import pprint

from benchq.logical_architecture_modeling.graph_based_logical_architectures import (
    TwoRowBusArchitectureModel,
    ActiveVolumeArchitectureModel,
)


def perform_compilation(block_encoding, m):

    error_budget = ErrorBudget.from_even_split(total_failure_tolerance=1e-2)
    print(error_budget)

    n_block_encodings = 2**m

    context = cirq.DecompositionContext(cirq.SimpleQubitManager())
    qasm = openqasm(
        block_encoding,
        rotation_allowed=True,
        context=context,
        circuit_precision=0.01 / 3,  # error budget in Azure paper is 0.01
    )

    def simple_steps(n_steps):
        return [0] * n_steps

    qasm_circuit = [line for line in qasm]
    qasm_string = "".join(qasm_circuit)

    orq_circuit = import_circuit(QuantumCircuit.from_qasm_str(qasm_string))

    print(orq_circuit.n_qubits)

    quantum_program = QuantumProgram([orq_circuit], n_block_encodings, simple_steps)
    quantum_program = quantum_program.split_into_smaller_subroutines(10000)

    algorithm_implementation = AlgorithmImplementation(quantum_program, error_budget, 1)

    # # Here we run the resource estimation pipeline:
    # # Architecture model is used to define the hardware model.
    ion_trap_hw_model = DETAILED_ION_TRAP_ARCHITECTURE_MODEL

    # logical_architecture = "two_row_bus"
    # architecture = TwoRowBusArchitectureModel()

    logical_architecture = "active_volume"
    architecture = ActiveVolumeArchitectureModel()

    # Create the estimator object, we can optimize for "Time" or "Space"
    graph_estimator = GraphResourceEstimator(optimization="Time", verbose=True)

    circuit_compiler = get_ruby_slippers_circuit_compiler(
        teleportation_threshold=100,
        min_neighbor_degree=4,
        max_num_neighbors_to_search=int(1e6),
        use_fully_optimized_dag=True,
        teleportation_distance=2,
    )

    
    # estimator = GraphResourceEstimator(optimization="Space", verbose=True)

    # circuit_compiler = get_ruby_slippers_circuit_compiler(
    #     teleportation_threshold=30,
    #     min_neighbor_degree=4,
    #     max_num_neighbors_to_search=int(1e6),
    #     teleportation_distance=2,
    # )


    compiler = get_implementation_compiler(
        circuit_compiler=circuit_compiler, destination="single-thread"
    )

    compiled_implementation = compiler(
        algorithm_implementation,
        logical_architecture,
        graph_estimator.optimization,
        graph_estimator.verbose,
    )

    compiled_implementation.error_budget = error_budget

    with open("10_33orb_graph_estimator_time_active.pkl", "wb") as f:
        pickle.dump(graph_estimator, f)

    with open("10_33orb_compiled_implementation_time_active.pkl", "wb") as f:
        pickle.dump(compiled_implementation, f)

    graph_resource_info_ion = (
        graph_estimator.estimate_resources_from_compiled_implementation(
            compiled_implementation,
            architecture,
            ion_trap_hw_model,
            magic_state_factory_iterator=iter_litinski_factories(ion_trap_hw_model),
        )
    )

    print("Resource estimation results for ions:")
    pprint.pprint(graph_resource_info_ion)

    graph_resource_info_ion.logical_architecture_resource_info.qec_cycle_allocation.plot()

    print(
        "Graph state cycles",
        graph_resource_info_ion.logical_architecture_resource_info.qec_cycle_allocation.inclusive(
            "graph state prep"
        ),
    )
    print(
        "Total cycles",
        graph_resource_info_ion.logical_architecture_resource_info.qec_cycle_allocation.total,
    )


perform_compilation(block_encoding, m)

end_time = time()

print("time to run", end_time - start_time)
