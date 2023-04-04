from .transformers import synthesize_clifford_t


def run_resource_estimation_pipeline(
    program_or_circuit,
    error_budget,
    estimator,
    transformer=synthesize_clifford_t,
):
    transformed = transformer(program_or_circuit, error_budget)
    return estimator.estimate(transformed, error_budget)
