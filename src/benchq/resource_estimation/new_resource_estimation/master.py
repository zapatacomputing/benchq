import numpy as np


class GraphResourceEstimator:
    def __init__(self, hw_model, error_budget, specs):
        self.hw_model = hw_model
        self.error_budget = error_budget
        self.specs = specs

    def _synthesis_multiplier(self):
        return (
            12
            * np.log2(
                1
                / (
                    self.error_budget["total_budget"]
                    * self.error_budget["synthesis_accuracy"]
                )
            )
            if self.specs["gate_synthesis"]
            else 1
        )

    def _ec_multiplier(self, distance, n_measurements):
        return 240 * distance * n_measurements

    def get_logical_st_volume(self, n_nodes):
        return 12 * n_nodes * 240 * n_nodes

    # We called it "base cell failure rate" before.
    # New name makes more sense to us, but perhaps we've been misguided
    def logical_operation_error_rate(self, distance):
        # Will be updated through Alexandru and Joe's work
        return (
            distance
            * 0.3
            * (70 * self.hw_model.physical_gate_error_rate) ** ((distance + 1) / 2)
        )

    def calculate_total_logical_error_rate(self, distance, n_nodes):
        return self.logical_operation_error_rate(distance) * self.get_logical_st_volume(
            n_nodes
        )

    def calculate_wall_time(self, distance: float, n_measurements: int) -> float:
        # This formula is probably wrong, check it!
        return (
            self._synthesis_multiplier()
            * self._ec_multiplier(distance, n_measurements)
            * n_measurements
        )

    def find_min_viable_distance(
        self,
        n_nodes,
        min_d=4,
        max_d=100,
    ):
        min_viable_distance = None
        target_error_rate = (
            self.error_budget["total_error"] * self.error_budget["ec_error_rate"]
        )
        for distance in range(min_d, max_d):
            logical_error_rate = self.calculate_total_logical_error_rate(
                distance,
                n_nodes,
            )

            if logical_error_rate < target_error_rate and min_viable_distance is None:
                min_viable_distance = distance

            if logical_error_rate < target_error_rate:
                return min_viable_distance

        raise RuntimeError(f"Not found good error rates under distance code: {max_d}.")

    def _get_n_measurements(self, graph) -> int:
        scheduler_only_compiler = substrate_scheduler(graph)
        return len(scheduler_only_compiler.measurement_steps)

    def _get_n_physical_qubits(self, max_graph_degree, distance):
        return 12 * max_graph_degree * 2 * distance**2

    def get_resource_estimates(self, distance, n_nodes):
        results_dict = {
            "logical_error_rate": self.calculate_total_logical_error_rate(
                distance, n_nodes
            ),
            "total_time": self.calculate_wall_time(distance, n_measurements),
            "physical_qubit_count": physical_qubit_count,
            "min_viable_distance": min_viable_distance,
            "logical_st_volume": logical_st_volume,
            "n_measurement_steps": n_measurements_steps,
            "max_graph_degree": max_graph_degree,
            "n_nodes": n_nodes,
        }


def _transform_all_circuits(program, error_budget, specs):
    graph_list = []
    for circuit in program.subroutines:

        # TODO: This should be simply "process_circuit(circuit, error_budget, specs)"
        if specs["gate_synthesis"]:
            processed_circuit = pyliqtr_transpile_to_clifford_t(
                circuit, synthesis_accuracy=error_budget.gate_synthesis
            )
        else:
            processed_circuit = simplify_rotations(circuit_with_rotations)

        graph_list.append(get_algorithmic_graph(processed_circuit))
    # TODO: potentially include some other data in the return,
    # like data_qubits or sth like that.
    return graph_list


def re_for_circuit(circuit, error_budget, hardware_model, decoder_model, specs):
    # Make a program out of a circuit
    # Run re_with_full_graph
    pass


def resource_estimator(program, error_budget, hardware_model, decoder_model, specs):
    # transform all the circuits
    graph_list = _transform_all_circuits(program, error_budget, specs)

    # create graphs for all the circuits
    if specs["stitching_method"] == "exact":
        graph = combine_subcomponent_graphs(graph_list, program.multiplicities)
    elif specs["stitching_method"] == "naive":
        graph = combine_graphs_naively(graph_list, program.multiplicities)
    # in future:
    # different levels of graph stitching possible?

    # get error correction parameters
    resource_estimator = ResourceEstimator(whatever, specs)

    # get resource estimations
    return resource_estimator.estimate_from_graph(graph)


def re_with_subgraphs(program, error_budget, hardware_model, decoder_model, specs):
    # transform all the circuits
    graph_list = _transform_all_circuits(program, error_budget, specs)

    # create graphs for all the circuits
    # in future – possible exact stitching of smaller parts

    # get error correction parameters – with subgraphs will be different

    # get resource estimations – with subgraphs will be different
    return resource_estimator.estimate_from_subgraphs(graph)
