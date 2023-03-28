import numpy as np

from .transformers import default_transformer




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


### Idea:
### Use this function that sort of puts the whole pipeline together
### If we later think that it is too complicate for scientists to use,
### we will provide a topl level function with more familiar arguments
### i.e.
### def get_resource_estimation(quantum_program, arch_model, use_full_graph):
###     ...
def run_resource_estimation_pipeline(
    program_or_circuit,
    error_budget,
    use_full_program,
    estimator,
    transformer=default_transformer,
):
    transformed = transformer(program_or_circuit, error_budget)
    return estimator.estimate(transformed, error_budget, use_full_program)
