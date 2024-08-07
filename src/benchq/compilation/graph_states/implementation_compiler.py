from typing import Callable, List

from orquestra import sdk
from orquestra.quantum.circuits import Circuit

from ...algorithms.data_structures import AlgorithmImplementation
from ..circuits.compile_to_native_gates import compile_to_native_gates
from .circuit_compilers import default_ruby_slippers_circuit_compiler
from .compiled_data_structures import (
    CompiledAlgorithmImplementation,
    CompiledQuantumProgram,
    GSCInfo,
)


@sdk.task(
    source_import=sdk.GithubImport(
        "zapatacomputing/benchq",
        git_ref="ac/DTA2-270-implement-pauli-tracker",
    ),
    custom_image="hub.stage.nexus.orquestra.io/"
    "zapatacomputing/benchq-ce:3eec2c8-sdk0.62.0",
)
def distributed_graph_creation(
    circuit: Circuit,
    logical_architecture: str,
    optimization: str,
    verbose: bool,
    circuit_compiler,
    circuit_num: int,
    n_subroutines: int,
) -> GSCInfo:
    if verbose:
        print(f"\nCompiling subroutine {circuit_num+1} of {n_subroutines}...")
    circuit = compile_to_native_gates(circuit, verbose)
    if verbose:
        print("Transferring Data to Julia...")
    return circuit_compiler(circuit, logical_architecture, optimization, verbose)

def get_implementation_compiler(
    circuit_compiler=default_ruby_slippers_circuit_compiler,
    max_subroutine_size: int = int(1e6),
    destination: str = "single-thread",
    num_cores: int = 3,
    config_name: str = "darpa-ta1",
    workspace_id: str = "darpa-phase-ii-gsc-resource-estimates-8a7c3b",
    project_id: str = "migration",
) -> Callable[[AlgorithmImplementation, str, bool], CompiledAlgorithmImplementation]:
    @sdk.workflow(resources=sdk.Resources(cpu=str(num_cores), memory="16Gi"))
    def get_program_compilation_wf(
        algorithm_implementation: AlgorithmImplementation,
        logical_architecture: str = "two_row",
        optimization: str = "Space",
        verbose: bool = False,
    ) -> List[sdk.ArtifactFuture[GSCInfo]]:
        compiled_subroutine_list = []
        program = algorithm_implementation.program
        program = program.split_into_smaller_subroutines(max_subroutine_size)
        for circuit_num, circuit in enumerate(program.subroutines):
            compiled_subroutine_list.append(
                distributed_graph_creation(
                    circuit,
                    logical_architecture,
                    optimization,
                    verbose,
                    circuit_compiler,
                    circuit_num,
                    len(algorithm_implementation.program.subroutines),
                )
            )

        return compiled_subroutine_list

    def parallelized_compiler(
        algorithm_implementation: AlgorithmImplementation,
        logical_architecture: str = "two_row",
        optimization: str = "Space",
        verbose: bool = False,
    ) -> CompiledAlgorithmImplementation:
        if verbose:
            print("Beginning compilation...")
        program_compilation_wf = get_program_compilation_wf(
            algorithm_implementation,
            logical_architecture,
            optimization,
            verbose,
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
            algorithm_implementation.program,
            compiled_subroutine_list,  # type: ignore
        )

        return CompiledAlgorithmImplementation(
            compiled_program, algorithm_implementation
        )

    return parallelized_compiler
