from typing import Callable

from ...algorithms.data_structures import GraphPartition
from .circuit_compilers import (
    default_ruby_slippers_circuit_compiler,
)
from ...problem_embeddings.quantum_program import (
    QuantumProgram,
)
from orquestra import sdk
from .compiled_data_structures import (
    CompiledQuantumProgram,
    CompiledAlgorithmImplementation,
)
from ..circuits.compile_to_native_gates import compile_to_native_gates
from ...algorithms.data_structures import AlgorithmImplementation
from orquestra.quantum.circuits import Circuit


# @sdk.task(
#     dependency_imports=[sdk.PythonImports("benchq[dev]")],
#     custom_image="hub.stage.nexus.orquestra.io/zapatacomputing/benchq-ce:3eec2c8-sdk0.60.0",
# )
@sdk.task(
    source_import=sdk.GithubImport(
        "zapatacomputing/benchq",
        git_ref="faster-kahns-algo",
    ),
    custom_image="hub.nexus.orquestra.io/zapatacomputing/benchq-ce:3eec2c8-sdk0.60.0",
)
def distributed_graph_creation(
    circuit: Circuit,
    optimization: str,
    verbose: bool,
    circuit_compiler,
    circuit_num: int,
):
    if verbose:
        print(f"\nCompiling subroutine {circuit_num+1}...")
    circuit = compile_to_native_gates(circuit, verbose)
    if verbose:
        print("Initializing graph state compilation...")
    return circuit_compiler(circuit, optimization, verbose)


def get_implementation_compiler(
    circuit_compiler=default_ruby_slippers_circuit_compiler,
    destination: str = "single-thread",
    num_cores: int = 3,
    config_name: str = "darpa-ta1",
    workspace_id: str = "darpa-phase-ii-gsc-resource-estimates-8a7c3b",
    project_id: str = "migration",
) -> Callable[[QuantumProgram], GraphPartition]:

    @sdk.workflow(resources=sdk.Resources(cpu=str(num_cores), memory="16Gi"))
    def get_program_compilation_wf(
        algorithm_implementation: AlgorithmImplementation,
        optimization: str = "Space",
        verbose: bool = False,
    ) -> GraphPartition:
        compiled_subroutine_list = []
        for circuit_num, circuit in enumerate(
            algorithm_implementation.program.subroutines
        ):
            compiled_subroutine_list.append(
                distributed_graph_creation(
                    circuit, optimization, verbose, circuit_compiler, circuit_num
                )
            )

        return compiled_subroutine_list

    def parallelized_compiler(
        algorithm_implementation: AlgorithmImplementation,
        optimization: str = "Space",
        verbose: bool = False,
    ) -> GraphPartition:
        if verbose:
            print("Beginning compilation...")
        program_compilation_wf = get_program_compilation_wf(
            algorithm_implementation, optimization, verbose
        )
        if destination == "single-thread":
            wf_run = program_compilation_wf.run("in_process")
        elif destination == "local":
            wf_run = program_compilation_wf.run("ray")
        elif destination == "remote":
            wf_run = program_compilation_wf.run(
                config_name,
                workspace_id=workspace_id,
                project_id=project_id,
            )
        compiled_subroutine_list = wf_run.get_results(wait=True)
        # Hack to ensure that workflow always returns a list
        if not isinstance(compiled_subroutine_list, tuple):
            compiled_subroutine_list = [compiled_subroutine_list]

        if verbose:
            print("Compilation complete.")

        compiled_program = CompiledQuantumProgram.from_program(
            algorithm_implementation.program, compiled_subroutine_list
        )

        return CompiledAlgorithmImplementation(
            compiled_program, algorithm_implementation
        )

    return parallelized_compiler
