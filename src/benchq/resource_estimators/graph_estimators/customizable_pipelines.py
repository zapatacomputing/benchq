from dataclasses import replace

from ...algorithms.data_structures.algorithm_implementation import (
    AlgorithmImplementation,
)


def get_custom_resource_estimation(
    algorithm_implementation: AlgorithmImplementation,
    estimator,
    transformers,
):
    for transformer in transformers:
        algorithm_implementation = replace(
            algorithm_implementation,
            program=transformer(algorithm_implementation.program),
        )

    return estimator.estimate(algorithm_implementation)


# 1. Compile to native gates
# 2. Transpile to Clifford+T (Optional)
# 4. Get Graph Data
#   a. From full circuit
#   b. From stitching subroutines
# 5. Estimate resources

# Both
# optimization: str = "Space",
# verbose: bool = True,

# Estimation:
# qecc_model: Optional[QECCModel] = None,
# hw_model: BasicArchitectureModel,
# decoder_model: Optional[DecoderModel] = None,
# error_budget: Optional[ErrorBudget] = None,
# n_shots: int = 1,
# magic_state_factory_iterator: Optional[Iterable[MagicStateFactory]] = None,

# Compiler:
# use_stitching = true,
# substrate_scheduler_preset: str = "fast",
# destination="single-thread",
# config_name="darpa-ta1",
# workspace_id="darpa-phase-ii-gsc-resource-estimates-8a7c3b",
# project_id="migration",
# num_cores=3,
# takes_graph_input: bool = True,
# gives_graph_output: bool = True,
# max_num_qubits: int = 1,
# teleportation_threshold: int = 40,
# teleportation_distance: int = 4,
# min_neighbor_degree: int = 6,
# max_num_neighbors_to_search: int = int(1e5),
# decomposition_strategy: int = 0,
# max_graph_size: int = 1e7,
