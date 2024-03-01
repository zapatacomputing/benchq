from typing import Callable

from ...algorithms.data_structures import GraphPartition
from ...compilation import (
    compile_circuit_using_ruby_slippers,
)
from ...problem_embeddings.quantum_program import (
    QuantumProgram,
)
from orquestra import sdk
from .compiled_data_structures import CompiledQuantumProgram
from ..circuits.compile_to_native_gates import compile_to_native_gates


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
def distributed_graph_creation(circuit, circuit_compiler):
    circuit = compile_to_native_gates(circuit)
    return circuit_compiler(circuit)


def get_quantum_program_compiler(
    circuit_compiler=compile_circuit_using_ruby_slippers,
    destination="single-thread",
    num_cores=3,
    config_name="darpa-ta1",
    workspace_id="darpa-phase-ii-gsc-resource-estimates-8a7c3b",
    project_id="migration",
) -> Callable[[QuantumProgram], GraphPartition]:

    @sdk.workflow(resources=sdk.Resources(cpu=str(num_cores), memory="16Gi"))
    def program_compilation_wf(program: QuantumProgram) -> GraphPartition:
        graph_data_list = [circuit_compiler(circuit) for circuit in program.subroutines]

        return CompiledQuantumProgram.from_program(program, graph_data_list)

    def parallelized_compiler(program: QuantumProgram) -> GraphPartition:
        print("Beginning compilation...")
        if destination == "single-thread":
            wf_run = program_compilation_wf(program).run("in_process")
        elif destination == "local":
            wf_run = program_compilation_wf(program).run("ray")
        elif destination == "remote":
            wf_run = program_compilation_wf(program).run(
                config_name,
                workspace_id=workspace_id,
                project_id=project_id,
            )
        compiled_program = wf_run.get_results(wait=True)
        print("Compilation complete.")

        return compiled_program

    return parallelized_compiler
