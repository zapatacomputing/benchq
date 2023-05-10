from ...data_structures import AlgorithmImplementation, QuantumProgram
from .graph_estimator import GraphData, GraphResourceEstimator, ResourceInfo


class SubroutineInfo:
    def __init__(self, n_qubits: int):
        self.n_edges_in_active_nodes = [0] * n_qubits
        self.highest_degree_in_inactive_nodes = 0
        self.is_reset = [False] * n_qubits
        self.n_edges_added_before_reset = [0] * n_qubits


class FootprintResourceEstimator(GraphResourceEstimator):
    def estimate(
        self,
        algorithm_implementation: AlgorithmImplementation,
    ) -> ResourceInfo:
        assert isinstance(algorithm_implementation.program, QuantumProgram)

        estimated_max_graph_degree = self.estimate_max_graph_degree(
            algorithm_implementation.program
        )

        # simulate graph data
        simulated_graph_data = GraphData(
            max_graph_degree=estimated_max_graph_degree,
            n_nodes=algorithm_implementation.program.n_nodes,
            n_t_gates=algorithm_implementation.program.n_t_gates,
            n_rotation_gates=algorithm_implementation.program.n_rotation_gates,
            n_measurement_steps=algorithm_implementation.program.n_nodes,
        )

        return self.estimate_resources_from_graph_data(
            simulated_graph_data,
            algorithm_implementation,
        )

    def estimate_max_graph_degree(self, program: QuantumProgram) -> int:
        # identify which gates change the graph structure
        node_creation_gates = ["T", "Tdag", "RX", "RY", "RZ"]
        edge_gates = ["CX", "CZ", "CNOT"]
        n_program_qubits = program.subroutines[0].n_qubits

        all_subroutine_info = []
        for i, subrountine in enumerate(program.subroutines):
            this_info = SubroutineInfo(n_program_qubits)
            for op in subrountine.operations:
                if op.gate.name in node_creation_gates:
                    this_info.highest_degree_in_inactive_nodes = max(
                        this_info.highest_degree_in_inactive_nodes,
                        this_info.n_edges_in_active_nodes[op.qubit_indices[0]] + 1,
                    )
                    if not this_info.is_reset[op.qubit_indices[0]]:
                        this_info.n_edges_added_before_reset[
                            op.qubit_indices[0]
                        ] = this_info.n_edges_in_active_nodes[op.qubit_indices[0]]

                    this_info.n_edges_in_active_nodes[op.qubit_indices[0]] = 1
                    this_info.is_reset[op.qubit_indices[0]] = True
                elif op.gate.name in edge_gates:
                    # assume all edge gates result in a new edge
                    this_info.n_edges_in_active_nodes[op.qubit_indices[0]] += 1
                    this_info.n_edges_in_active_nodes[op.qubit_indices[1]] += 1
            all_subroutine_info.append(this_info)

        curr_degree = [0] * n_program_qubits
        curr_highest_degree = 0
        for subroutine_idx in program.subroutine_sequence:
            this_info = all_subroutine_info[subroutine_idx]
            for i in range(n_program_qubits):
                if this_info.is_reset[i]:
                    curr_highest_degree = max(
                        curr_highest_degree,
                        curr_degree[i] + this_info.n_edges_added_before_reset[i],
                    )
                    curr_degree[i] = this_info.n_edges_in_active_nodes[i]
                else:
                    curr_degree[i] += this_info.n_edges_in_active_nodes[i]
            curr_highest_degree = max(
                curr_highest_degree, this_info.highest_degree_in_inactive_nodes
            )
        curr_highest_degree = max([curr_highest_degree, *curr_degree])

        return curr_highest_degree
