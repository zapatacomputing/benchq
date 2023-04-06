def run_resource_estimation_pipeline(
    program,
    error_budget,
    estimator,
    transformers,
):
    for transformer in transformers:
        program = transformer(program)
    return estimator.estimate(program, error_budget)
